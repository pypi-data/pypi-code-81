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

from datetime import datetime, timedelta
import re
import time
import sqlite3
import nmap

from digital_hydrant.collectors.collector import Collector
from digital_hydrant.config import db_path, config


class Nmap(Collector):
    def __init__(self, name):
        super(Nmap, self).__init__(name)
        self.table_name = "unique_ips"

        try:
            self.conn = sqlite3.connect(db_path)
            self.cursor = self.conn.cursor()
        except Exception as err:
            self.logger.critical(f"Failed to connect to the database: {err}")
            exit(1)

        self.scan_type = config.get(self.name, "scan_type", fallback="-sSUV")

    def run(self):
        week_ago = datetime.timestamp(datetime.now() - timedelta(weeks=1)) * 1000
        self.cursor.execute(
            f"SELECT ip FROM {self.table_name} WHERE last_nmap_scan IS NULL or last_nmap_scan < {week_ago} ORDER BY last_nmap_scan ASC"
        )

        ips = self.cursor.fetchall()
        self.logger.debug(f"Processing {len(ips)} IP addresses")
        for ip in ips:
            self.logger.debug(f"Processing IP address: {ip[0]}")
            self.__nmap__(ip[0])

    def __nmap__(self, ip):
        data = {}
        nm = nmap.PortScanner()
        result = nm.scan(ip, arguments=self.scan_type)

        open_ports = []
        for host in nm.all_hosts():
            for proto in nm[host].all_protocols():
                lport = sorted(nm[host][proto])
                for port in lport:
                    if nm[host][proto][port]["state"] == "open":
                        open_ports.append(f"{port}/{proto}")

        data["ip"] = ip
        data["protocols"] = nm[ip].all_protocols() if ip in nm.all_hosts() else []
        data["open_ports"] = open_ports

        if "scan" in result and ip in result["scan"]:
            result["scan"] = result["scan"][ip]
        data["output_log"] = result

        timestamp = datetime.timestamp(datetime.now()) * 1000

        self.queue.put(**{"type": self.name, "payload": data, "timestamp": timestamp})

        try:
            open = (
                f"'{','.join(open_ports)}'"
                if len(open_ports) > 0
                else "open_ports=NULL"
            )
            self.cursor.execute(
                f"UPDATE {self.table_name} SET last_nmap_scan={timestamp}, open_ports={open} WHERE ip='{ip}'"
            )
        except sqlite3.Error as e:
            self.logger.error(f"Failed to update last_nmap_scan for {ip}: {e}")
        finally:
            self.conn.commit()
