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

from datetime import datetime
import json
import time

# import collector module from parent directory
from digital_hydrant.collectors.collector import Collector


class Lldp(Collector):
    def __init__(self, name):
        super(Lldp, self).__init__(name)

    def run(self):
        command = "lldpctl -f json"
        self.logger.debug(f"Command: {command}")
        output = self.execute(command)
        timestamp = datetime.timestamp(datetime.now()) * 1000
        payload = self.__parse_output__(output)

        self.queue.put(
            **{"type": self.name, "payload": payload, "timestamp": timestamp}
        )

    def __parse_output__(self, output):
        output = json.loads(output)
        try:
            for i in output["lldp"]["interface"]:  # iterate per interface
                parsed_output = {}

                # SysName
                sysname = list(output["lldp"]["interface"][i]["chassis"].keys())[0]
                parsed_output["system_name"] = sysname

                # SysDescr
                sysdescr = output["lldp"]["interface"][i]["chassis"][sysname][
                    "descr"
                ].replace("\n", " ")
                parsed_output["system_description"] = sysdescr

                # PortID
                portid = output["lldp"]["interface"][i]["port"]["id"]["type"]
                portid += " " + output["lldp"]["interface"][i]["port"]["id"]["value"]
                parsed_output["port_id"] = portid

                # MgmtIP
                mgmtip = output["lldp"]["interface"][i]["chassis"][sysname]["mgmt-ip"]
                parsed_output["management_ip"] = mgmtip

                # vlan-id
                vlanid = int(output["lldp"]["interface"][i]["vlan"]["vlan-id"])
                parsed_output["vlan_id"] = vlanid

                return parsed_output

        except KeyError as err:
            self.logger.error(f"No interface found, with error {err}")
