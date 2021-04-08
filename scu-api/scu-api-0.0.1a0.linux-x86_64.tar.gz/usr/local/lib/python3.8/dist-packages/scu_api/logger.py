# -*- coding: utf-8 -*-

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s -%(name)s - %(levelname)s - %(message)s"
)


def get_mylogger(name: str):
    return logging.getLogger(name)
