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

from digital_hydrant.collectors.collector import Collector


class Dhcp(Collector):
    def __init__(self, name):
        super(Dhcp, self).__init__(name)

    def run(self):
        timestamp = datetime.timestamp(datetime.now()) * 1000
        command = "dhcpcd -T 2> /dev/null | tr '\n' ' '"
        output = self.execute(command)
        payload = {"dhcp_log": output}
        self.queue.put(
            **{"type": self.name, "payload": payload, "timestamp": timestamp}
        )
