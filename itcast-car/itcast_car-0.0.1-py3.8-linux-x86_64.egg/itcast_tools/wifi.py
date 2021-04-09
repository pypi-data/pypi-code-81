import re
import platform
import subprocess
import json


def _ensure_str(output):
    try:
        output = output.decode("utf8",errors='ignore')
    except UnicodeDecodeError:
        output = output.decode("utf16",errors='ignore')
    except AttributeError:
        pass
    return output


def _rssi_to_quality(rssi):
    return 2 * (rssi + 100)


def _split_escaped(string, separator):
    """Split a string on separator, ignoring ones escaped by backslashes."""

    result = []
    current = ''
    escaped = False
    for char in string:
        if not escaped:
            if char == '\\':
                escaped = True
                continue
            elif char == separator:
                result.append(current)
                current = ''
                continue
        escaped = False
        current += char
    result.append(current)
    return result


class _AccessPoint(dict):

    def __init__(self, ssid, bssid, quality, security):
        dict.__init__(self, ssid=ssid, bssid=bssid, quality=quality, security=security)

    def __getattr__(self, attr):
        return self.get(attr)

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__ = d

    def __repr__(self):
        args = ", ".join(["{}={}".format(k, v) for k, v in self.items()])
        return "AccessPoint({})".format(args)


class _WifiScanner(object):

    def __init__(self, device=""):
        self.device = device
        self.cmd = self.get_cmd()

    def get_cmd(self):
        raise NotImplementedError

    def parse_output(self, output):
        raise NotImplementedError

    def get_access_points(self):
        out = self.call_subprocess(self.cmd)
        results = self.parse_output(_ensure_str(out))
        return results

    @staticmethod
    def call_subprocess(cmd):
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (out, _) = proc.communicate()
        return out


class _OSXWifiScanner(_WifiScanner):

    def get_cmd(self):
        path = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/"
        cmd = "airport -s"
        return path + cmd

    def parse_output(self, output):
        results = []
        # 5 times 2 "letters and/or digits" followed by ":"
        # Then one time only 2 "letters and/or digits"
        # Use non-capturing groups (?:...) to use {} for amount
        # One wrapping group (...) to capture the whole thing
        bbsid_re = re.compile("((?:[0-9a-zA-Z]{2}:){5}(?:[0-9a-zA-Z]){2})")
        security_start_index = False
        for line in output.split("\n"):
            if line.strip().startswith("SSID BSSID"):
                security_start_index = line.index("SECURITY")
            elif line and security_start_index and 'IBSS' not in line:
                try:
                    ssid = bbsid_re.split(line)[0].strip()
                    bssid = bbsid_re.findall(line)[0]
                    rssi = bbsid_re.split(line)[-1].strip().split()[0]
                    security = line[security_start_index:]
                    ap = _AccessPoint(ssid, bssid, _rssi_to_quality(int(rssi)), security)
                    results.append(ap)
                except Exception as e:
                    msg = "Please provide the output of the error below this line at {}"
                    print(msg.format("github.com/kootenpv/access_points/issues"))
                    print(e)
                    print("Line:")
                    print(line)
                    print("Output:")
                    print(output)
        return results


class _WindowsWifiScanner(_WifiScanner):

    def get_cmd(self):
        return "netsh wlan show networks mode=bssid"

    def parse_output(self, output):
        ssid = None
        ssid_line = -100
        bssid = None
        bssid_line = -100
        quality = None
        security = None
        results = []
        for num, line in enumerate(output.split("\n")):
            line = line.strip()
            if line.startswith("SSID"):
                ssid = " ".join(line.split()[3:]).strip()
                if ssid == '':
                    # truely empty SSID
                    ssid = ' '
                ssid_line = num
            elif num == ssid_line + 2:
                security = ":".join(line.split(":")[1:]).strip()
            elif line.startswith("BSSID"):
                bssid = ":".join(line.split(":")[1:]).strip()
                bssid_line = num
            elif num == bssid_line + 1:
                quality = int(":".join(line.split(":")[1:]).strip().replace("%", ""))
                if bssid is not None:
                    ap = _AccessPoint(ssid, bssid, quality, security)
                    results.append(ap)
        return results


class _NetworkManagerWifiScanner(_WifiScanner):
    """Get access points and signal strengths from NetworkManager."""

    def get_cmd(self):
        # note that this command requires some time in between / rescan
        return "nmcli -t -f ssid,bssid,signal,security device wifi list"

    def parse_output(self, output):
        results = []

        for line in output.strip().split('\n'):
            try:
                ssid, bssid, quality, security = _split_escaped(line, ':')
            except ValueError:
                continue
            access_point = _AccessPoint(ssid, bssid, int(quality), security)
            results.append(access_point)

        return results

    @classmethod
    def is_available(cls):
        """Whether NetworkManager is available on the system."""

        try:
            proc = subprocess.Popen(
                ['systemctl', 'status', 'NetworkManager'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            proc.communicate()
            return proc.returncode == 0
        except OSError:
            return False


class _IwlistWifiScanner(_WifiScanner):

    def get_cmd(self):
        return "sudo iwlist {} scanning 2>/dev/null".format(self.device)

    def parse_output(self, output):
        ssid = None
        bssid = None
        bssid_line = -1000000
        quality = None
        security = None
        security = []
        results = []
        for num, line in enumerate(output.split("\n")):
            line = line.strip()
            if line.startswith("Cell"):
                if bssid is not None:
                    ap = _AccessPoint(ssid, bssid, quality, security)
                    results.append(ap)
                    security = []
                bssid = ":".join(line.split(":")[1:]).strip()
                bssid_line = num
            elif line.startswith("ESSID"):
                ssid = ":".join(line.split(":")[1:]).strip().strip('"')
            elif num > bssid_line + 2 and re.search(r"\d/\d", line):
                quality = int(line.split("=")[1].split("/")[0])
                bssid_line = -1000000000
            elif line.startswith("IE:") and line.find('Unknown') == -1:
                security.append(line[4:])
        if bssid is not None:
            ap = _AccessPoint(ssid, bssid, quality, security)
            results.append(ap)
        return results


class _TermuxWifiScanner(_WifiScanner):
    """Wifi scanning tool using Termux on Android"""
    def get_cmd(self):
        return 'termux-wifi-scaninfo'

    def parse_output(self, output):
        data = json.loads(output)
        if not isinstance(data, list):
            return []  # Happens when permission not granted
        return [
            _AccessPoint(i['ssid'], i['bssid'], _rssi_to_quality(i['rssi']), '')
            for i in data
        ]

    @staticmethod
    def is_available():
        cmd_code = subprocess.call(
            ['which', 'termux-wifi-scaninfo'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return cmd_code == 0


def _get_scanner(device=""):
    operating_system = platform.system()
    if operating_system == 'Darwin':
        return _OSXWifiScanner(device)
    elif operating_system == 'Linux':
        if _NetworkManagerWifiScanner.is_available():
            return _NetworkManagerWifiScanner(device)
        elif _TermuxWifiScanner.is_available():
            return _TermuxWifiScanner(device)
        else:
            return _IwlistWifiScanner(device)
    elif operating_system == 'Windows':
        return _WindowsWifiScanner()


def get_bssid(ssid):
    if ssid is None:
        raise RuntimeError('ssid can not none')

    wifi_scanner = _get_scanner()
    access_points = wifi_scanner.get_access_points()

    for ap in access_points:
        if ap.ssid == ssid:
            return ap.bssid

    raise RuntimeError('ssid [{}] is not exist'.format(ssid))
