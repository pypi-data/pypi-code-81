"""Get information from GCE Ecodevices RT2."""
import requests

__author__ = """Pierre COURBIN"""
__email__ = 'pierre.courbin@gmail.com'
__version__ = '1.0.2'


class EcoDevicesRT2:
    """Class representing the Ecodevices RT2 and its API"""

    def __init__(self, host, port=80, apikey="", timeout=3):
        self._host = host
        self._port = port
        self._apikey = apikey
        self._apiurl = "http://%s:%s/api/xdevices.json?key=%s" % (str(host), str(port), str(apikey))
        self._timeout = timeout

    @property
    def host(self):
        """Return the hostname."""
        return self._host

    @property
    def apikey(self):
        """Return the apikey."""
        return self._apikey

    @property
    def apiurl(self):
        """Return the default apiurl."""
        return self._apiurl

    def _request(self, params):
        r = requests.get(
            self._apiurl,
            params=params,
            timeout=self._timeout)
        r.raise_for_status()
        content = r.json()
        product = content.get("product", None)
        if product == "EcoDevices_RT":
            return content
        else:
            raise Exception(
                "Ecodevices RT2 API request error, url: %s`r%s", r.request.url, content,
            )

    def ping(self) -> bool:
        try:
            return self._request({"Index": "All"})['status'] == 'Success'
        except:
            pass
        return False

    def get(self, command, command_value, command_entry=None) -> int:
        """Get value from api : http://{host}:{port}/api/xdevices.json?key={apikey}&{command}={command_value},
        then get value {command_entry} in JSON response."""
        response = self._request({command: command_value})
        if command_entry is not None:
            response = response.get(command_entry)
