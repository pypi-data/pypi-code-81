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

import re
import time
import importlib
from datetime import datetime, timedelta
import pkg_resources

from digital_hydrant.collectors.collector import Collector
import digital_hydrant.config

from netifaces import AF_INET, ifaddresses
import sqlite3

PORTS = {"ssh": "22", "snmp": "161"}


class Hydra(Collector):
    def __init__(self, name):
        super(Hydra, self).__init__(name)
        self.table_name = "unique_ips"

        try:
            self.conn = sqlite3.connect(digital_hydrant.config.db_path)
            self.cursor = self.conn.cursor()
        except Exception as err:
            self.logger.critical(f"Failed to connect to the database: {err}")
            exit(1)

        self.ssh_enabled = digital_hydrant.config.config.getboolean(
            self.name, "enable_ssh", fallback=True
        )
        self.snmp_enabled = digital_hydrant.config.config.getboolean(
            self.name, "enable_snmp", fallback=True
        )
        self.iface = digital_hydrant.config.config.get(self.name, "interface")

        self.wordlist_path = pkg_resources.resource_filename(
            "digital_hydrant", "config/hydra/wordlist.txt"
        )
        self.userlist_path = pkg_resources.resource_filename(
            "digital_hydrant", "config/hydra/userlist.txt"
        )
        self.snmp_wordlist_path = pkg_resources.resource_filename(
            "digital_hydrant", "config/hydra/snmp_wordlist.txt"
        )

    def run(self):
        week_ago = datetime.timestamp(datetime.now() - timedelta(weeks=1)) * 1000
        where = ""
        order_by = ""
        for type, port in PORTS.items():
            if getattr(self, f"{type}_enabled"):
                if len(where) > 0:
                    where += " OR "
                where += f"(open_ports like '%{port}%' AND  ({type}_last_tested IS NULL OR {type}_last_tested < {week_ago}))"
                order_by += (
                    f"{type}_last_tested"
                    if len(order_by) == 0
                    else f", {type}_last_tested"
                )

        self.cursor.execute(
            f"SELECT ip, open_ports FROM {self.table_name} WHERE {where} ORDER BY {order_by} ASC"
        )

        records = self.cursor.fetchall()
        self.logger.debug(f"Processing {len(records)} IP addresses")
        for record in records:
            self.logger.debug(f"Processing IP address: {record[0]}")
            self.__hydra__(record)

    def __hydra__(self, record):
        ip = record[0]
        ports = record[1]

        # connect to subnet, use X.X.X.227 because it is rarely used
        my_subnet_ip = "{}.227".format(re.sub(r"\.\d+$", "", ip))
        self.logger.debug(f"Joining {ip} network, with IP {my_subnet_ip}")
        self.execute(f"ifconfig {self.iface}:1 {my_subnet_ip}")

        parsed_output = {}
        parsed_output["target"] = ip

        ssh_output = ""
        snmp_output = ""

        run_ssh = self.ssh_enabled and PORTS["ssh"] in ports
        if run_ssh:
            ssh_command = f"hydra -I -L {self.userlist_path} -P {self.wordlist_path} {ip} ssh 2>&1"
            ssh_output = self.execute(ssh_command)

            parsed_output["ssh"] = self.parse_output(ssh_output)
            parsed_output["ssh_output_log"] = ssh_output

        run_snmp = self.snmp_enabled and PORTS["snmp"] in ports
        if run_snmp:
            parsed_output["snmp"] = self.parse_output(snmp_output)
            parsed_output["snmp_output_log"] = snmp_output

        parsed_output["vulnerable"] = (
            "ssh" in parsed_output and parsed_output["ssh"]["vulnerable"]
        ) or ("snmp" in parsed_output and parsed_output["snmp"]["vulnerable"])

        timestamp = datetime.timestamp(datetime.now()) * 1000

        self.queue.put(
            **{"type": self.name, "payload": parsed_output, "timestamp": timestamp}
        )

        # disconnect from subnet
        self.logger.debug(f"Disconnecting from {ip}")
        self.execute(f"ifconfig {self.iface}:1 down")

        try:
            set = ""
            if run_ssh:
                set += f"ssh_last_tested={timestamp}"

            if run_snmp:
                set += (
                    f"snmp_last_tested={timestamp}"
                    if len(set) == 0
                    else f", snmp_last_tested={timestamp}"
                )

            if set:
                self.cursor.execute(
                    f"UPDATE {self.table_name} SET {set} WHERE ip='{ip}'"
                )
        except sqlite3.Error as e:
            self.logger.error(f"Failed to update last_tested for {ip}: {e}")
        finally:
            self.conn.commit()

    def parse_output(self, output):
        data = {}
        results = []
        for line in output.split("\n"):
            if not line.strip():
                continue

            if line.startswith("[DATA]"):
                for part in line.split(","):
                    if "login tries" in part:
                        temp = re.findall(r"\d+", part)
                        res = list(map(int, temp))
                        data["login_tries"] = res[0]
                        data["usernames_tested"] = res[1]
                        data["passwords_tested"] = res[2]
            elif line.startswith("1 of 1"):
                for part in line.split(","):
                    if "valid password" in part:
                        temp = re.findall(r"\d+", part)
                        res = list(map(int, temp))
                        data["successful_logins"] = res[0]
            elif line.startswith("[22][ssh]") or line.startswith("[161][snmp]"):
                parts = line.split()
                result = {}
                for i in range(1, len(parts), 2):
                    result[parts[i].replace(":", "")] = parts[i + 1]
                results.append(result)

        data["results"] = results
        data["vulnerable"] = len(results) > 0

        return data
