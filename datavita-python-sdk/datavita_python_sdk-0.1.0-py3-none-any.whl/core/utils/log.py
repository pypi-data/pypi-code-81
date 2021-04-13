# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 hcyjs.com, Inc. All Rights Reserved

"""
    @Time : 2021-02-02 17:38
    @Author : Yin Jian
    @Version：V 0.1
    @File : log.py
    @desc :
"""
import logging

DEFAULT_LOGGER_NAME = "dataVita"
DEFAULT_FORMAT = "%(asctime)s [%(levelname)s] %(message)s (%(filename)s:%(lineno)s %(name)s)"
DEFAULT_LEVEL = logging.INFO


def init_default_logger():
    """初始化默认日志格式
    """
    logger = logging.getLogger(DEFAULT_LOGGER_NAME)
    logger.setLevel(DEFAULT_LEVEL)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(DEFAULT_LEVEL)

    # create formatter
    formatter = logging.Formatter(DEFAULT_FORMAT)

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.removeHandler(ch)
    logger.addHandler(ch)

    return logger


default_logger = init_default_logger()
