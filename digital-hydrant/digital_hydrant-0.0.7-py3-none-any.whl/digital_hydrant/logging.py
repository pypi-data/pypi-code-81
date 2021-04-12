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

import logging

import colorlog
from enum import Enum
from digital_hydrant.config import config as conf


class LogLevel(Enum):
    CRITICAL = 50
    ERROR = 40
    WARNING = 30
    INFO = 20
    DEBUG = 10
    NOTSET = 0


def getLogger(module):
    handler = logging.StreamHandler()

    handler.setFormatter(
        colorlog.ColoredFormatter(
            "{log_color}{levelname:7} {purple}{asctime} {blue}{name}:{lineno}{reset}\n{message}",
            datefmt="%Y-%m-%d %H:%M:%S",
            reset=True,
            log_colors={
                "DEBUG": "cyan",
                "INFO": "blue",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
            style="{",
        )
    )

    logger = logging.getLogger(module)
    logger.addHandler(handler)
    logger.setLevel(conf.get("logging", "level", fallback="INFO"))

    return logger
