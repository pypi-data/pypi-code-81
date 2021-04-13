#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 hcyjs.com, Inc. All Rights Reserved

"""
    @Time : 2021-02-02 17:38
    @Author : Yin Jian
    @Version：V 0.1
    @File : andes_data.py
    @desc :
"""
import datetime
import hashlib
import json
import random
import time
import typing
import pandas as pd

from datavita.andes.andes_apis import andes_apis_dict
from datavita.core.auth import Auth
from datavita.core.common import contants
from datavita.core.transport.comrequests import CommonRequests
from datavita.core.transport.http import Request
from datavita.core.utils import log
from datavita.core.utils.middleware import Middleware


def tid_mak():
    uuid_str = '{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now()) + ''.join(
        [str(random.randint(1, 10)) for i in range(5)])
    return uuid_str


class AndesData(object):
    """
        中台数据
        初始化固定参数 auth 超时 最大重试次数
    """

    def __init__(
            self,
            auth: typing.Optional[Auth] = None,
            base_url: str = contants.BASE_URL,
            timeout: int = contants.SESSION_PERIOD_TIMEOUT,
            max_retries: int = contants.MAX_RETRIES,
    ):
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.auth = auth
        middleware = Middleware()
        self._middleware = middleware
        self.logger = log.default_logger

    def _send(self, api_name, action, api, params, max_retries, timeout):
        try:
            req = self._build_http_request(api_name, action, api, params=params)
            resp = CommonRequests(auth=self.auth, max_retries=max_retries, timeout=timeout).send(req=req)
        except Exception as e:
            return pd.DataFrame()
            raise e
        return self._middleware.logged_response_df_handler(self.auth, resp, resp.request.request_name)

    def _build_http_request(self, api_name, action, api, params) -> Request:
        nonce = tid_mak()
        timestamp = int(time.time())
        date_str = datetime.datetime.now()
        path_parm = api.replace(contants.BASE_URL, '')
        parm_md5 = hashlib.md5(str(json.dumps(params, ensure_ascii=False)).encode(encoding='UTF-8')).hexdigest()
        if action.upper() == 'GET':
            sign_str = f"""{action.upper()}\n*/*\n\n\n{date_str}\nx-datavita-nonce:{nonce}\nx-datavita-signature-method:HmacSHA1\n{path_parm}"""
        else:
            sign_str = f"""{action.upper()}\n*/*\n{parm_md5}\napplication/json\n{date_str}\nx-datavita-nonce:{nonce}\nx-datavita-signature-method:HmacSHA1\n{path_parm}"""
        signature = self.auth.make_authorization(sign_str)
        if action.upper() == 'GET':
            headers = {
                'Accept': '*/*',
                'x-datavita-key': '{}'.format(self.auth.access_id),
                'x-datavita-nonce': '{}'.format(nonce),
                'x-datavita-timestamp': '{}'.format(timestamp),
                'x-datavita-signature-method': 'HmacSHA1',
                'date': '{}'.format(date_str),
                'x-datavita-signature-headers': 'x-datavita-signature-method,x-datavita-nonce',
                'x-datavita-signature': '{}'.format(signature)
            }
        else:
            headers = {
                'Accept': '*/*',
                'Content-Type': 'application/json',
                'x-datavita-key': '{}'.format(self.auth.access_id),
                'x-datavita-nonce': '{}'.format(nonce),
                'x-datavita-timestamp': '{}'.format(timestamp),
                'x-datavita-signature-method': 'HmacSHA1',
                'date': '{}'.format(date_str),
                'x-datavita-signature-headers': 'x-datavita-signature-method,x-datavita-nonce',
                'x-datavita-signature': '{}'.format(signature)
            }
        return Request(
            request_name=api_name,
            url=api,
            method=action.upper(),
            data=params,
            headers=headers
        )

    def get_dataset_by_tagcode(self, tag_code: str = None) -> pd.DataFrame:
        """
        按标签获取表 get_dataset_by_tagcode()
        :param tag_code: 标签代码
        :return:
        """
        url = andes_apis_dict.get("get_dataset_by_tagcode").format(base_url=self.base_url, tag_code=str(tag_code))
        return self._send(api_name="按标签获取表", action='get', api=url, params=None, max_retries=self.max_retries,
                          timeout=self.timeout)

    def get_data_by_dataset_name(self, dataset_name: str = None, dataset_id: int = None) -> pd.DataFrame:
        """
            按表获取data_code信息（只有时序数据的schema调用）get_data_by_dataset_name()
        :param dataset_id: 数据集id
        :param dataset_name: 数据集名称
        :return:
        """
        url = andes_apis_dict.get("get_data_by_dataset_name").format(base_url=self.base_url)
        params = {
            "datasetName": dataset_name,
            "datasetId": dataset_id
        }
        return self._send(api_name="按表获取data_code信息", action='post', api=url, params=params,
                          max_retries=self.max_retries,
                          timeout=self.timeout)

    def get_data_by_industry(self, industry_name) -> pd.DataFrame:
        """
         按行业获取数据 get_data_by_industry()
        :param industry_name: 行业名称
        :return:
        """
        url = andes_apis_dict.get("get_data_by_industry").format(base_url=self.base_url,
                                                                 industry_name=industry_name)
        return self._send(api_name="按行业获取数据", action='get', api=url, params=None, max_retries=self.max_retries,
                          timeout=self.timeout)

    def get_data_by_datacode(self, data_code: str = None, start_day: int = None, end_day: int = None,
                             sort_field: str = None,
                             sort_order: str = None) -> pd.DataFrame:
        """
            按照data_code获取数据 get_data_by_datacode()
        :param sort_order: 排序规则 ASC DESC
        :param sort_field: 排序字段
        :param end_day: 结束时间
        :param start_day: 开始时间
        :param data_code: 数据代码
        :return:
        """
        url = andes_apis_dict.get('get_data_by_datacode').format(base_url=self.base_url)
        data_code = str(data_code).split(",")
        params = {
            "dataCode": data_code,
            "startDay": start_day, "endDay": end_day,
            "sortField": sort_field,
            "sortOrder": sort_order
        }
        return self._send(api_name="按照data_code获取数据", action='post', api=url, params=params,
                          max_retries=self.max_retries,
                          timeout=self.timeout)

    def get_untsd_data_by_dataset_id(self, dataset_id: str = None, sort_field: str = None,
                                     sort_order: str = None) -> pd.DataFrame:
        """
            按照dataset_id获取非时序数据 get_untsd_data_by_dataset_id()
        :param dataset_id: 数据集id
        :param sort_order: 排序规则
        :param sort_field: 排序字段
        :return:
        """
        url = andes_apis_dict.get('get_untsd_data_by_dataset_id').format(base_url=self.base_url)
        dataset_id = str(dataset_id).split(",")
        params = {
            "datasetId": dataset_id,
            "sortField": sort_field,
            "sortOrder": sort_order
        }
        return self._send(api_name="按照dataset_id获取非时序数据", action='post', api=url, params=params,
                          max_retries=self.max_retries,
                          timeout=self.timeout)

    def get_data_by_dataname(self, data_name: str = None, start_day: int = None, end_day: int = None,
                             sort_field: str = None,
                             sort_order: str = None) -> pd.DataFrame:
        """
            按照data_code获取数据 get_data_by_dataname()
        :param sort_order: 排序规则
        :param sort_field: 排序字段
        :param end_day: 结束时间
        :param start_day: 开始时间
        :param data_name: 数据集名称
        :return:
        """
        url = andes_apis_dict.get('get_data_by_dataname').format(base_url=self.base_url)
        data_name = str(data_name).split(",")
        params = {
            "dataName": data_name,
            "startDay": start_day, "endDay": end_day,
            "sortField": sort_field,
            "sortOrder": sort_order
        }
        return self._send(api_name="按照data_code获取数据", action='post', api=url, params=params,
                          max_retries=self.max_retries,
                          timeout=self.timeout)

    def get_data_by_wind_code(self, wind_code: str = None, start_day: int = None, end_day: int = None,
                              sort_field: str = None,
                              sort_order: str = None) -> pd.DataFrame:
        """
            按Wind代码获取数据 get_data_by_wind_code()
        :param wind_code: wind代码
        :param sort_order: 排序规则
        :param sort_field: 排序字段
        :param end_day: 结束时间
        :param start_day: 起始时间
        :return:
        """
        url = andes_apis_dict.get('get_data_by_wind_code').format(base_url=self.base_url)
        wind_code = str(wind_code).split(",")
        params = {
            "windCode": wind_code,
            "startDay": start_day, "endDay": end_day,
            "sortField": sort_field,
            "sortOrder": sort_order
        }
        return self._send(api_name="按Wind代码获取数据", action='post', api=url, params=params, max_retries=self.max_retries,
                          timeout=self.timeout)
