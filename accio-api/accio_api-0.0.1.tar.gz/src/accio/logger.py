#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : logger.py
@Time    : 2020/12/29 9:42
@Author  : Yu Tao
@Software: PyCharm
"""
import os
import time
import logging
import inspect
from logging.handlers import RotatingFileHandler

class MyLog(object):
    def create_handlers(self, path):
        dir_log = path
        dir_time = time.strftime('%Y-%m-%d', time.localtime())
        handlers = {logging.NOTSET: os.path.join(dir_log, 'notset_%s.log' % dir_time),

                    logging.DEBUG: os.path.join(dir_log, 'debug_%s.log' % dir_time),

                    logging.INFO: os.path.join(dir_log, 'info_%s.log' % dir_time),

                    logging.WARNING: os.path.join(dir_log, 'warning_%s.log' % dir_time),

                    logging.ERROR: os.path.join(dir_log, 'error_%s.log' % dir_time),

                    logging.CRITICAL: os.path.join(dir_log, 'critical_%s.log' % dir_time),
                    }
        log_levels = handlers.keys()

        for level in log_levels:
            path = os.path.abspath(handlers[level])
            handlers[level] = RotatingFileHandler(path, maxBytes=10000, backupCount=2, encoding='utf-8')
        return handlers

    def get_now(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    def __init__(self,path = os.path.join(os.path.join(os.getcwd(), os.path.pardir, 'Log')), level=logging.NOTSET):
        handlers = self.create_handlers(path)
        self.__loggers = {}
        log_levels = handlers.keys()
        for level in log_levels:
            logger = logging.getLogger(str(level))
            logger.addHandler(handlers[level])
            logger.setLevel(level)
            self.__loggers.update({level: logger})

    def get_log_message(self, level, message):
        frame, filename, lineNo, functionName, code, unknowField = inspect.stack()[2]
        '''日志格式：[时间] [类型] [记录代码] 信息'''
        return "[%s] [%s] [%s - %s - %s] %s" % (self.get_now(), level, filename, lineNo, functionName, message)

    def info(self, message):
        message = self.get_log_message("info", message)
        self.__loggers[logging.INFO].info(message)

    def error(self, message):
        message = self.get_log_message("error", message)
        self.__loggers[logging.ERROR].error(message)

    def warning(self, message):
        message = self.get_log_message("warning", message)
        self.__loggers[logging.WARNING].warning(message)

    def debug(self, message):
        message = self.get_log_message("debug", message)
        self.__loggers[logging.DEBUG].debug(message)

    def critical(self, message):
        message = self.get_log_message("critical", message)
        self.__loggers[logging.CRITICAL].critical(message)


if __name__ == "__main__":
    logger = MyLog()
    logger.info("info")
