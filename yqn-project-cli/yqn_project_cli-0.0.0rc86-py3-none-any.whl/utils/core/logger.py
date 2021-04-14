# -*- coding: utf-8 -*-
# Author: ZKH
# Date：2021/2/24
import logging
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime
import json
from pathlib import Path


class LogFormatter(logging.Formatter):
    converter = datetime.fromtimestamp

    def __init__(self, app_name, app_id, log_type="Default"):
        self.app_name = app_name
        self.app_id = app_id
        self.log_type = log_type
        super().__init__()

    def format(self, record: logging.LogRecord):
        """
        {"log_timestamp": "2020/11/11 15:11:09",
         "trace_id": "",
         "remote_app_id": "unknownApp",
         "log_level": "info",
         "app_name": "appName",
         "thread_id": "13621",
         "log_type": "BIZ",
         "caller_id": "",
         "server_ip": "192.168.14.218",
         "client_ip": "0.0.0.0",
         "log_message": "TextPositionList END, UUID:92841272-82e3-4530-beef-bc822c4eb845 ,fileId:26472159",
         "exp": "",
         "app_id": "50010"}
        :param record:
        :return:
        """
        ct = self.converter(record.created)
        time_str = ct.strftime("%Y/%m/%d %H:%M:%S")
        log_dict = dict()
        log_dict['log_timestamp'] = time_str
        log_dict['trace_id'] = ''
        log_dict['remote_app_id'] = ''
        log_dict['log_level'] = record.levelname
        log_dict['app_name'] = self.app_name
        log_dict['thread_id'] = record.thread
        log_dict['log_type'] = self.log_type
        log_dict['caller_id'] = ''
        if 'SERVER_IP' in os.environ:
            log_dict['server_ip'] = os.environ['SERVER_IP']
        else:
            log_dict['server_ip'] = ''
        log_dict['client_ip'] = ''
        log_dict['log_message'] = record.msg
        log_dict['exp'] = ''
        log_dict['path_name'] = record.pathname
        log_dict['line_no'] = record.lineno
        log_dict['app_id'] = self.app_id
        return json.dumps(log_dict, ensure_ascii=False)


def get_logger(app_name, app_id, log_path, log_type='Default'):
    logger = logging.getLogger(app_name + "_" + log_type)
    logger.setLevel(logging.INFO)
    formatter = LogFormatter(app_name, app_id, log_type.upper())
    root_path = log_path
    Path(root_path).mkdir(parents=True, exist_ok=True)

    file_handler = logging.FileHandler(root_path + log_type.lower() + ".txt")
    # file_handler = TimedRotatingFileHandler(root_path + log_type.lower() + ".txt", when="D", backupCount=14)

    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.handlers = []
    logger.addHandler(file_handler)
    return logger


class Logger:
    def __init__(self, logger_config=None, log_type='Default'):
        assert isinstance(log_type, str), 'log type needs set to be str'

        self.logger_config = logger_config

        if self.logger_config is None:
            self.loggers = {}

        else:
            self.loggers = {log_type.lower(): get_logger(self.logger_config.app_name,
                                                         self.logger_config.app_id,
                                                         self.logger_config.log_path,
                                                         log_type)}

    def __call__(self, log_type: str):
        assert isinstance(log_type, str), 'log type needs set to be str'
        assert self.logger_config is not None, 'log must be init from config'

        if log_type.lower() not in self.loggers:
            self.loggers[log_type.lower()] = get_logger(
                self.logger_config.app_name,
                self.logger_config.app_id,
                self.logger_config.log_path,
                log_type)

        return self.loggers[log_type.lower()]
