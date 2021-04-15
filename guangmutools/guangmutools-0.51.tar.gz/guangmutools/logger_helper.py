# -*- encoding: utf-8 -*-
'''
@文件    :logger_helper.py
@说明    :日志处理辅助类，基于时间维度做自动切分
@时间    :2021/03/08 13:52:22
@作者    :caimiao@kingsoft.com
@版本    :0.1
'''

import logging
import logging.handlers
import os

class LoggerTimedRotating(object):
    _instances = {}

    @classmethod
    def getInstance(cls, when:str='d', interval:int=1, backupCount:int=30, logger:str='daily_log', level:int=logging.DEBUG, log_dir:str='logs') -> logging.Logger:
        if logger not in cls._instances:
            _log_path = os.path.join(os.getcwd(), log_dir)
            if not os.path.isdir(_log_path):
                os.mkdir(_log_path)
            if os.path.isdir(_log_path):
                gen_logger = logging.getLogger(logger)
                gen_logger.setLevel(level)

                rf_handler = logging.handlers.TimedRotatingFileHandler(filename=os.path.join(_log_path, logger), when=when, interval=interval,
                                                                       backupCount=backupCount)
                rf_handler.setFormatter(
                    logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))

                # 在控制台打印日志
                handler = logging.StreamHandler()
                handler.setLevel(level)
                handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

                gen_logger.addHandler(rf_handler)
                gen_logger.addHandler(handler)

                cls._instances.setdefault(logger, gen_logger)
            else:
                raise IOError("logger file not exists")
        return cls._instances.get(logger)
