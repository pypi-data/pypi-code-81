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
import uuid
import importlib
from urllib.error import HTTPError

import requests

from digital_hydrant import logging
from digital_hydrant.collector_queue import CollectorQueue
import digital_hydrant.config


def get_mac_address():
    return ":".join(re.findall("..", "%012x" % uuid.getnode()))


class Uploader:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.mac_addr = get_mac_address()
        self.queue = CollectorQueue()

        self.api_token = digital_hydrant.config.config.get("api", "token")
        self.api_url = digital_hydrant.config.config.get("api", "url")

    def __upload__(self):
        while True:
            importlib.reload(digital_hydrant.config)
            self.logger.setLevel(
                digital_hydrant.config.config.get("logging", "level", fallback="INFO")
            )
            self.queue.set_log_level(
                digital_hydrant.config.config.get("logging", "level", fallback="INFO")
            )

            # select all un-uploaded data entries and add to queue
            self.logger.debug("Scanning database for unprocessed entries")
            entry = self.queue.peak()

            if entry is None:
                time.sleep(5)
            else:
                (id, type, payload, timestamp) = entry
                try:
                    data = {
                        "source": str(self.mac_addr),
                        "timestamp": timestamp,
                        "type": type,
                        "payload": payload,
                    }
                    headers = {"Authorization": f"Bearer {self.api_token}"}
                    response = requests.post(self.api_url, headers=headers, json=data)
                    self.logger.info(f"Upload collector {type} at {timestamp}")
                    response.raise_for_status()

                    output = response.json()

                    self.queue.remove(id)
                except requests.exceptions.ConnectionError:
                    self.logger.error("Network error, will retry in 30 seconds")
                    time.sleep(30)

                except requests.exceptions.HTTPError as e:
                    self.logger.error(f"Failed to upload data: {e}")
                    self.queue.fail(id)
