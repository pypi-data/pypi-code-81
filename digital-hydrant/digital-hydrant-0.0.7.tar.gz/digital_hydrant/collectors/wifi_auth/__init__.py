# Copyright 2021 Outside Open
# This file is part of Digital-Hydrant.

# Digital-Hydrant is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Digital-Hydrant is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Digital-Hydrant.  If not, see https://www.gnu.org/licenses/.

import os
import time

from digital_hydrant.collectors.collector import Collector
from digital_hydrant.config import config as conf
from digital_hydrant.config import get_sections


class Wifi_auth(Collector):
    def __init__(self, name):
        super(Wifi_auth, self).__init__(name)

    def run(self):
        networks = get_sections("wifi_auth.network")
        for section in networks:
            essid = conf.get(section, "essid")
            passwd = conf.get(section, "passwd")

            # find name of wireless interface:
            output = self.execute("iw dev | grep Interface")
            output = output.split(" ")
            wireless_interface = output[1][:-1]
            self.logger.debug(f"Found wireless interface: {wireless_interface}")

            # generate wpa passphrase:
            wpa_pass = self.execute(
                f'wpa_passphrase "{essid}" "{passwd}" | tee digital_hydrant/collectors/wifi_auth/wpa_supplicant.conf'
            )

            # connect to wireless access point
            self.logger.debug(f"Attempting to connect to wireless access point {essid}")
            tic = time.perf_counter()
            wpa_supplicant = self.execute(
                f"wpa_supplicant -c digital_hydrant/collectors/wifi_auth/wpa_supplicant.conf -i {wireless_interface}"
            )
            auth_timeout = conf.getint(self.name, "exec_duration")
            auth_time = -1
            for line in wpa_supplicant.split("\n"):
                toc = time.perf_counter()
                auth_time = toc - tic
                if line.find("CTRL-EVENT-CONNECTED") != -1:
                    self.logger.debug("Wireless is connected")
                    break
                elif auth_time > auth_timeout:
                    self.logger.error("Authentication timeout reached, exiting")
                    auth_time = -1
                    break

            # parse connection details
            parsed_output = {}

            if auth_time != -1:
                parsed_output["AUTH_TIME"] = auth_time

                # check for inet6 IP address
                inet6_addr = ""
                output = self.execute("ifconfig")
                # split by empty line
                output = output.split("\n\n")
                line = None
                for interface in output:
                    if interface.find(wireless_interface) != -1:
                        line = interface
                        break
                if line is not None:
                    if line.find("inet6") != -1:
                        # find IP address
                        line = line.split("\n")
                        for group in line:
                            if group.find("inet6") != -1:
                                line = group
                                break
                        line = line.split()
                        inet6_addr = line[1]
                        self.logger.debug("Inet6 IP obtained")
                    else:
                        self.logger.error("No inet6 IP address found")
                else:
                    self.logger.error("No inet6 IP address found")
                parsed_output["INET6_ADDRESS"] = inet6_addr

                # check AP address, check link quality, check signal level, check frequency, check bit rate, check tx power
                AP_address = ""
                link_quality = ""
                signal_level = ""
                frequency = ""
                bit_rate = ""
                tx_power = ""
                loaded = False  # sometimes there will be an index out of range error because iwconfig hasn't loaded all variables by time of polling   # instead of waiting, poll again so it runs as fast as possible
                poll_counter = 0
                poll_max = 5  # limit number of times it can poll iwconfig
                while not loaded:
                    try:
                        output = self.execute(
                            "iwconfig 2>&1 | grep -v 'no wireless extensions'"
                        )
                        # split by empty line
                        output = output.split("\n\n")
                        # find entry for wireless interface in use
                        for interface in output:
                            if interface.find(wireless_interface) != -1:
                                line = interface
                                break

                        # process data
                        line = line.split("  ")

                        # check AP address
                        entry = ""
                        for group in line:
                            if group.find("Access Point") != -1:
                                entry = group
                                break
                        entry = entry.split()
                        AP_address = entry[2]

                        # check link quality
                        entry = ""
                        for group in line:
                            if group.find("Link Quality") != -1:
                                entry = group
                                break
                        entry = entry.split("=")
                        link_quality = entry[1]

                        # check signal level
                        entry = ""
                        for group in line:
                            if group.find("Signal level") != -1:
                                entry = group
                                break
                        entry = entry.split("=")
                        signal_level = entry[1]

                        # check frequency
                        entry = ""
                        for group in line:
                            if group.find("Frequency") != -1:
                                entry = group
                                break
                        entry = entry.split(":")
                        frequency = entry[1]

                        # check bit rate
                        entry = ""
                        for group in line:
                            if group.find("Bit Rate") != -1:
                                entry = group
                                break
                        entry = entry.split("=")
                        bit_rate = entry[1]

                        # check tx power
                        entry = ""
                        for group in line:
                            if group.find("Tx-Power") != -1:
                                entry = group
                                break
                        entry = entry.split("=")
                        tx_power = entry[1]

                        loaded = True

                    except Exception as err:
                        poll_counter += 1
                        if poll_counter > poll_max:
                            self.logger.error("Unable to scrap iwconfig")
                            break
                        self.logger.error(
                            f"Error scraping iwconfig, attempt {poll_counter}/{poll_max}, retrying"
                        )
                        loaded = False
                        time.sleep(0.2)

                parsed_output["AP_ADDRESS"] = AP_address
                parsed_output["LINK_QUALITY"] = link_quality
                parsed_output["SIGNAL_LEVEL"] = signal_level
                parsed_output["FREQUENCY"] = frequency
                parsed_output["BIT_RATE"] = bit_rate
                parsed_output["TX_POWER"] = tx_power

                parsed_output["ESSID"] = essid

                self.insert_database(parsed_output)

            # start DHClient to check IPv4 address
            # dhclient wlan0

            # bring wireless interface down and up again "reset it"
            os.system(f"ifconfig {wireless_interface} down")
            os.system(f"ifconfig {wireless_interface} up")

            # delete temp files
            # rm utils/temp/wpa_supplicant.conf
            os.remove("digital_hydrant/collectors/wifi_auth/wpa_supplicant.conf")
