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

import importlib
import subprocess
import time
from abc import ABC, abstractmethod

import digital_hydrant.config
from digital_hydrant import logging
from digital_hydrant.collector_queue import CollectorQueue

# Digital Hydrant 2020
# Collector object class definition
# contains all the base functions needed for interfacing with the Digital Hydrant system
# used for reducing code repetitiveness and consolidating code
# all scraping and data processing will be done in the collector's "main.py"
# will handle loading configuration data from the collector's "config.yml"
# will handle logging information, printing colored output, and saving to file


class Collector(ABC):
    def __init__(self, name):
        # create all variables
        self.name = str(name)
        self.logger = logging.getLogger(f"digital_hydrant.{self.name}")
        self.queue = CollectorQueue()

    @abstractmethod
    def run(self):
        pass

    def run_collection(self):
        self.update_config()
        self.logger.info(f"Collecting {self.name} data")
        self.run()

    def execute(self, cmd):
        command = str(cmd)
        self.logger.debug(f"Executing command: {command}")
        output = subprocess.run(
            command, shell=True, stdout=subprocess.PIPE
        ).stdout.decode("utf-8")

        return output

    def update_config(self):
        importlib.reload(digital_hydrant.config)
        self.exec_duration = digital_hydrant.config.config.getint(
            self.name, "exec_duration", fallback=0
        )
        self.exec_time = digital_hydrant.config.config.getint(
            self.name, "exec_time", fallback=2
        )
        self.logger.setLevel(
            digital_hydrant.config.config.get("logging", "level", fallback="INFO")
        )
        self.queue.set_log_level(
            digital_hydrant.config.config.get("logging", "level", fallback="INFO")
        )
