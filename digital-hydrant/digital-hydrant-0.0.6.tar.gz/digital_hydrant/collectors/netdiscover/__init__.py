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
import time
import re

from digital_hydrant.collectors.collector import Collector
from digital_hydrant.config import config


class Netdiscover(Collector):
    def __init__(self, name):
        super(Netdiscover, self).__init__(name)

    def run(self):
        common_subnets = [
            "--localnet",
            "10.10.0.0",
            "192.168.0.0",
            "172.16.0.0",
            "172.26.0.0",
            "172.27.0.0",
            "172.17.0.0",
            "172.18.0.0",
            "172.19.0.0",
            "172.20.0.0",
            "172.21.0.0",
            "172.22.0.0",
            "172.23.0.0",
            "172.24.0.0",
            "172.25.0.0",
            "172.28.0.0",
            "172.29.0.0",
            "172.30.0.0",
            "172.31.0.0",
            "10.0.0.0",
        ]

        subnet_config = config.get("netdiscover", "subnet", fallback="/24")
        subnet_config = "/24" if subnet_config == "" else subnet_config

        for subnet in common_subnets:
            subnet = subnet + subnet_config if not "--" in subnet else subnet
            self.logger.debug(f"Scanning {subnet} with arp-scan")

            output = self.execute(f"arp-scan {subnet}")
            for line in output.split("\n"):
                self.parse_line(line)

    def parse_line(self, line):
        regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
        parsed_output = {}

        parts = line.split("\t")
        parts = list(filter(("").__ne__, parts))

        if (
            len(parts) < 3
            or not re.search(regex, parts[0])
            or parts[0].startswith("0.0.0")
        ):
            return

        # IP Address
        parsed_output["ip"] = parts[0]

        # MAC Address
        parsed_output["mac_address"] = parts[1]

        # Hostname
        name = ""
        max_index = len(parts)
        for ii in range(2, max_index):
            name += parts[ii] + " "
        if name != "":
            name = name[:-1]
        parsed_output["hostname"] = name

        if "DUP" in name:
            return

        timestamp = datetime.timestamp(datetime.now()) * 1000

        self.queue.put(
            **{"type": self.name, "payload": parsed_output, "timestamp": timestamp}
        )
