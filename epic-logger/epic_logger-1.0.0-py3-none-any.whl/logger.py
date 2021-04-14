# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------------
# Author:       ZERONE40
# Date:         2021-04-14 18:16
# Description:  不同模块使用Logger打印日志并输出到控制台

# -------------------------------------------------------------------------------


import logging
from logging import handlers

import os


class Logger:

    def __init__(self, unique_name, log_save, level=None, when='M', backup_count=6):
        """
        日志打印到不同的日志文件
        :param unique_name: 来自子类。一个唯一的标识，以__name__+子类日志级别区分不同的Logger，避免RootLogger被使用引发的重复打印日志问题。
        :param log_save: 日志保存路径及文件名。
        :param level: 来自子类。不同子类传递的level是不同的，以区分不同级别的日志输出。
        """
        self._logger = logging.getLogger(unique_name)
        self._logger.setLevel(level)

        file_path, file_name = os.path.split(log_save)
        if not os.path.exists(file_path):
            os.mkdir(file_path)

        time_formatter = "%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s"

        formatter = logging.Formatter(time_formatter)
        file_handler = handlers.TimedRotatingFileHandler(
            filename=log_save, when=when, backupCount=backup_count, encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self._logger.addHandler(stream_handler)


class DebugLogger(Logger):
    def __init__(self, unique_name, log_file_path, level=logging.DEBUG, when='D', backup_count=6):
        super().__init__(unique_name + "DEBUG", log_file_path, level, when, backup_count)
        self.log = self._logger.debug


class InfoLogger(Logger):
    def __init__(self, unique_name, log_file_path, level=logging.INFO, when='D', backup_count=6):
        super().__init__(unique_name + "INFO", log_file_path, level, when, backup_count)
        self.log = self._logger.info


class WarningLogger(Logger):
    def __init__(self, unique_name, log_file_path, level=logging.WARNING, when='D', backup_count=6):
        super().__init__(unique_name + "WARNING", log_file_path, level, when, backup_count)
        self.log = self._logger.warning


class ErrorLogger(Logger):
    def __init__(self, unique_name, log_file_path, level=logging.ERROR, when='D', backup_count=6):
        super().__init__(unique_name + "ERROR", log_file_path, level, when, backup_count)
        self.log = self._logger.error


class CriticalLogger(Logger):
    def __init__(self, unique_name, log_file_path, level=logging.CRITICAL, when='D', backup_count=6):
        super().__init__(unique_name + "CRITICAL", log_file_path, level, when, backup_count)
        self.log = self._logger.critical
