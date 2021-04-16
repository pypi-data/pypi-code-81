# -*- coding: utf-8 -*-
"""
Description:
    This module contains all things logging for epython

Author:
    Ray Gomez

Date:
    3/16/21
"""

import logging

# Logging overrides (paramiko is noisy)
logging.getLogger("paramiko.transport").setLevel(logging.ERROR)


def setup_logging(name="epython", log_level=logging.INFO, log_file=None):
    """Get the basic root logger."""

    # Define the logging format
    formatter = logging.Formatter('%(asctime)s - [%(pathname)s:%(lineno)d]'
                                  ' - %(levelname)s - %(message)s')

    root = logging.getLogger(name)

    # User provided override for logging
    if isinstance(log_level, str):
        log_level = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warn": logging.WARN,
            "warning": logging.WARNING,
            "error": logging.ERROR,
            "critical": logging.CRITICAL
        }.get(log_level.lower(), None) or log_level

    # Set to default if nothing is set
    if not log_level:
        log_level = logging.INFO

    root.setLevel(log_level)

    # Establish a file to log to
    if log_file:
        file_handler = logging.FileHandler(log_file, mode="w", encoding=None, delay=False)
        file_handler.setFormatter(formatter)
        root.addHandler(file_handler)

    # Setup the stdout
    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(formatter)
    root.addHandler(stdout_handler)

    return root
