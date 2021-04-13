# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 hcyjs.com, Inc. All Rights Reserved

"""
    @Time : 2021-02-02 17:38
    @Author : Yin Jian
    @Version：V 0.1
    @File : middleware.py
    @desc :
"""
import json

import pandas as pd

import numpy as np

from datavita.core.transport.http import Response, Request
from datavita.core.utils import log


class Middleware:
    """
        统一请求,返回,异常格式
    """

    def __init__(self, msg: str = None):
        self.logger = log.default_logger
        self.msg = msg

    def logged_request_handler(self, req: Request):
        """
        统一请求格式
        :param req: 请求
        :return:
        """
        request_name = req.request_name
        self.logger.info("[request] {}".format(request_name))
        return req

    def logged_response_df_handler(self, auth, resp: Response, msg):
        """
        统一返回格式
        :param auth: 权限类
        :param resp: 返回
        :param msg:  信息
        :return:
        """
        lst = resp.content
        keys = [str(x) for x in np.arange(len(lst))]
        list_json = dict(zip(keys, lst))
        str_json = json.dumps(list_json, indent=2, ensure_ascii=False)
        json_data = json.loads(str_json)
        temp_df = pd.DataFrame(json_data)
        temp_df = temp_df.T
        if temp_df.empty:
            self.logger.warn("[数据集] {} 未获取到数据".format(msg))
        return temp_df

    def logged_exception_handler(self, e):
        """
        统一异常格式
        :param e:
        :return:
        """
        self.logger.error(e)
