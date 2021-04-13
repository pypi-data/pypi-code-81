# -*- coding: utf-8 -*-
"""
------------------------------------------------------------------
    File Name:              logger
    Description:            
    Author:                 hzy
    date:                   2019/8/23
------------------------------------------------------------------
    Change Activity:
                            2019/8/23
------------------------------------------------------------------
"""
__author__ = 'hzy'

import time

import logging
import logging.handlers
from flask_templates.configs.template import LOG_CONFIG


def get_logger(logger_name, logger_level=logging.INFO):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logger_level)

    log_format = "%(name)s\t%(asctime)s\t%(pathname)s\t[line:%(lineno)d]\t %(levelname)s\t %(message)s"
    formater = logging.Formatter(log_format)

    # 存入文件的日志
    # handler = logging.handlers.TimedRotatingFileHandler(logger_location, "midnight", 1, days, encoding="utf-8")
    # handler.suffix = "%Y%m%d"
    # handler.setFormatter(formater)
    # logger.addHandler(handler)

    if LOG_CONFIG.get('enable_mail'):
        # 发邮件的日志
        mail_config = LOG_CONFIG.get('mail')
        sh = logging.handlers.SMTPHandler(mail_config['smtp_server'], mail_config['sender'], mail_config['receivers'],
                                          mail_config['subject'],
                                          credentials=(mail_config['user'], mail_config['password']), secure=())
        sh.setLevel(logging.ERROR)
        sh.setFormatter(formater)
        logger.addHandler(sh)

    return logger


logger = None
default_level = getattr(logging, LOG_CONFIG.get('level', "INFO"), logging.INFO)
try:
    from hzylog import logger_helper

    logger = logger_helper.get_logger(name='hzy', webhook=True)
except ModuleNotFoundError as e:

    logging.basicConfig(level=default_level,
                        format='%(asctime)s - %(name)s - %(filename)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s')
    # logger = logging.getLogger(__name__)
    logger = get_logger(__name__, logger_level=default_level)

    logger.warning("module %s can't import!", 'hzylog')


class PreLogger:
    logger_dict = {}


def apply_logger(logger_name=None):
    global logger
    logger_dict = logging.Logger.manager.loggerDict
    if logger_name:
        if logger_dict.get(logger_name):
            PreLogger.logger_dict.setdefault(logger_name, []).append(logger_dict.get(logger_name))
        logger_dict[logger_name] = logger
    else:
        for x in logger_dict:
            PreLogger.logger_dict.setdefault(x, []).append(logger_dict[x])
            logger_dict[x] = logger


def reset_logger(logger_name=None):
    logger_dict = logging.Logger.manager.loggerDict
    if logger_name:
        if PreLogger.logger_dict.get(logger_name):
            logger_dict[logger_name] = PreLogger.logger_dict.get(logger_name).pop(-1)
    else:
        for x in PreLogger.logger_dict:
            if PreLogger.logger_dict.get(x):
                logger_dict[x] = PreLogger.logger_dict.get(x).pop(-1)


if __name__ == "__main__":
    start_t = time.time()
    logger.error('123')

    pass

    print("use time: %s" % (time.time() - start_t))
