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

from digital_hydrant.collectors.collector import Collector

import speedtest


class Speedtest(Collector):
    def __init__(self, name):
        super(Speedtest, self).__init__(name)

    def run(self):
        s = speedtest.Speedtest()
        s.get_best_server()
        s.download()
        s.upload()
        payload = s.results.dict()

        timestamp = datetime.timestamp(datetime.now()) * 1000

        self.queue.put(
            **{"type": self.name, "payload": payload, "timestamp": timestamp}
        )
