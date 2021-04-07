# -*- coding: utf-8 -*-

"""package benutils
author    Benoit Dubois
copyright FEMTO ENGINEERING, 2021
license   GPL v3+
bref      Define logger class for app.
detail    Class can be instanciated from init/configure file:

logger = logger.Logger('my_logger_name', my_log_filename)
logger.set_console_level(ccst.CONSOLE_LOG_LEVEL)
logger.set_file_level(ccst.FILE_LOG_LEVEL)

          Then logger object is used in project file for logging usage:

from inifile import logger
logger.logging.error("My error")
"""

import logging
import logging.handlers as lh


CONSOLE_LOG_LEVEL = logging.INFO
FILE_LOG_LEVEL = logging.ERROR


class Logger:

    def __init__(self, name, filename):
        log_abs_filename = filename
        log_file_format = "%(asctime)s %(levelname) -8s %(filename)s " + \
            "%(funcName)s (%(lineno)d): %(message)s"
        file_formatter = logging.Formatter(log_file_format)

        log_console_format = "%(asctime)s [%(threadName)-12.12s]" + \
            "[%(levelname)-6.6s] %(filename)s %(funcName)s (%(lineno)d): " + \
            "%(message)s"
        console_formatter = logging.Formatter(log_console_format)

        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.DEBUG)

        self._file_handler = lh.TimedRotatingFileHandler(log_abs_filename,
                                                         when='W0')
        self._file_handler.setLevel(FILE_LOG_LEVEL)
        self._file_handler.setFormatter(file_formatter)
        self._logger.addHandler(self._file_handler)

        self._console_handler = logging.StreamHandler()
        self._console_handler.setLevel(CONSOLE_LOG_LEVEL)
        self._console_handler.setFormatter(console_formatter)
        self._logger.addHandler(self._console_handler)

        self._logger.propagate = False

    def set_file_level(self, value):
        self._file_handler.setLevel(value)

    def set_console_level(self, value):
        self._console_handler.setLevel(value)

    @property
    def logging(self):
        return self._logger
