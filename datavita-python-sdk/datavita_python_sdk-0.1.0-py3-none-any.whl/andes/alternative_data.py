# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : alternative_data.py
# Time       ：2021/4/6 2:48 下午
# Author     ：Yin Jian
# Description：
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


class AlternativeData(object):
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

    def realtime_news(self, query: str = None, start_date: str = None, end_date: str = None,
                      page_num: int = 1, ) -> pd.DataFrame:
        """
            根据关键词,获取当前热门新闻资讯
       :param query: 搜索关键词
       :param start_date: 开始日期，不设置获取最新资讯
       :param end_date: 结束日期
       :param page_num: 分页编码，默认第一页
       :return: DataFrame: 新闻数据集
       """
        url = andes_apis_dict.get('realtime_news').format(base_url=self.base_url)
        params = {
            "query": query,
            "startDate": start_date, "endDate": end_date,
            "pageNum": page_num
        }
        return self._send(api_name="实时获取当前热门新闻资讯", action='post', api=url, params=params, max_retries=self.max_retries,
                          timeout=self.timeout)
