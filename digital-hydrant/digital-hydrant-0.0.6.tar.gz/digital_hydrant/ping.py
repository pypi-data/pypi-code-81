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
from os import path

import requests

from digital_hydrant import logging
import digital_hydrant.config
from digital_hydrant.server_data_processor import Processor


class Ping:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.mac_addr = ":".join(re.findall("..", "%012x" % uuid.getnode()))
        self.processor = Processor()

    def __exec__(self):
        while True:
            importlib.reload(digital_hydrant.config)
            self.api_token = digital_hydrant.config.config.get("api", "token")
            self.api_url = digital_hydrant.config.config.get("api", "url")
            self.wait = digital_hydrant.config.config.getint(
                "ping", "wait", fallback=180
            )
            self.logger.setLevel(
                digital_hydrant.config.config.get("logging", "level", fallback="INFO")
            )

            self.logger.info("Ping server")

            try:
                headers = {"Authorization": f"Bearer {self.api_token}"}
                response = requests.get(f"{self.api_url}/ping", headers=headers)
                response.raise_for_status()

                response_data = response.json()

                # handle new data from the server
                if "data" in response_data.keys() and isinstance(
                    response_data["data"], dict
                ):
                    self.processor.process_server_data(response_data["data"])

                params = None
                # handle new config from the server
                if "config" in response_data.keys() and isinstance(
                    response_data["config"], dict
                ):
                    params = digital_hydrant.config.update_config(
                        response_data["config"]
                    )
                else:
                    params = {}
                    for section in digital_hydrant.config.config.sections():
                        temp_dict = {}
                        for option in digital_hydrant.config.config.options(section):
                            temp_dict[option] = digital_hydrant.config.config.get(
                                section, option
                            )

                        params[section] = temp_dict

                requests.put(
                    f"{self.api_url}/ping/complete", json=params, headers=headers
                )
            except requests.exceptions.ConnectionError:
                self.logger.error("Network error on ping")

            except HTTPError as e:
                self.logger.error(f"Failed to ping server\n\n{e}")
            time.sleep(self.wait)
