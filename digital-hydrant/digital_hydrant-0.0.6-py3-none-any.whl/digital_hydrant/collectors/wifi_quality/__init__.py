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

from digital_hydrant.collectors.collector import Collector
from digital_hydrant.config import config as conf
from digital_hydrant.collectors.wifi_quality.scan import Cell


class Wifi_quality(Collector):
    def __init__(self, name):
        super(Wifi_quality, self).__init__(name)

    def run(self):
        iface = conf.get(self.name, "interface", fallback="wlan0")

        timestamp = datetime.timestamp(datetime.now()) * 1000

        for cell in list(Cell.all(iface)):
            payload = self.__map_wifi__(cell)

            self.queue.put(
                **{
                    "type": self.name,
                    "payload": payload,
                    "timestamp": timestamp,
                }
            )

    def __map_wifi__(self, cell):
        cell_dict = {}
        cell_dict["ssid"] = cell.ssid
        cell_dict["signal"] = cell.signal
        cell_dict["quality"] = cell.quality
        cell_dict["frequency"] = cell.frequency
        cell_dict["bitrates"] = cell.bitrates
        cell_dict["encrypted"] = cell.encrypted
        cell_dict["channel"] = cell.channel
        cell_dict["channel"] = cell.channel
        cell_dict["address"] = cell.address
        cell_dict["mode"] = cell.mode

        if cell.encrypted:
            cell_dict["encryption_type"] = cell.encryption_type

        return cell_dict
