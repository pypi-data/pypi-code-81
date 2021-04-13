#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 hcyjs.com, Inc. All Rights Reserved

"""
    @Time : 2021-02-02 15:20
    @Author : Yin Jian
    @Version：V 0.1
    @File : comrequests.py
    @desc :
"""
import json
import time
import typing

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from datavita.core import exc
from datavita.core.auth import Auth
from datavita.core.transport import http
from datavita.core.transport.http import Request, Response
from datavita.core.utils.middleware import Middleware


class CommonRequests(http.AbsCommonRequest):
    """
        统一request
    """

    def __init__(
            self,
            auth: typing.Optional[Auth],
            max_retries: int = 3,
            timeout: int = 2,
            backoff_factor: float = 0.3,
            status_forcelist: typing.Tuple[int] = (500, 502, 504),
    ):
        self.max_retries = max_retries
        self.timeout = timeout
        self.auth = auth
        self.backoff_factor = backoff_factor
        self.status_forcelist = status_forcelist
        self._adapter = self._load_adapter(max_retries)
        self._middleware = Middleware()

    def send(self, req) -> http.Response:
        """
            发送请求
        :param req:
        :return:
        """
        resp = self._send(req, self.max_retries, self.timeout)
        return resp

    @property
    def middleware(self) -> Middleware:
        """
                生成统一格式类
        :return:
        """
        return self._middleware

    def _send(self, req: Request, max_retries, timeout) -> Response:

        try:
            session = requests.Session()
            adapter = self._load_adapter(max_retries)
            session.mount("http://", adapter=adapter)
            session.mount("https://", adapter=adapter)
            req.request_time = time.time()
            session_resp = session.request(
                method=req.method.upper(),
                url=req.url,
                json=req.json,
                data=None if json.dumps(req.data, ensure_ascii=False) == 'null' else json.dumps(req.data,
                                                                                                ensure_ascii=False).encode(),
                params=req.params,
                headers=req.headers,
                timeout=timeout,
            )
            resp = self.convert_response(session_resp)
            resp.request = req
            resp.response_time = time.time()
            if resp.status_code >= 400:
                raise exc.CommonException(status_code=resp.status_code)
            return resp
        except Exception as e:
            self._middleware.logged_exception_handler(e)
            raise e

    def _load_adapter(
            self, max_retries: typing.Optional[int] = None
    ) -> HTTPAdapter:
        if max_retries is None or max_retries > 3 and self._adapter is not None:
            return self._adapter

        max_retries = max_retries or 0
        adapter = HTTPAdapter()
        adapter.max_retries = Retry(
            total=max_retries,
            read=max_retries,
            connect=max_retries,
            backoff_factor=self.backoff_factor,
            status_forcelist=self.status_forcelist,
        )
        return adapter

    @staticmethod
    def convert_response(r: requests.Response) -> Response:
        """
            转换成包装过的response
        :param r: 请求结果
        :return:
        """
        content = json.loads(r.text)['result']
        status_code = json.loads(r.text)['code']
        return Response(
            url=r.url,
            method=r.request.method,
            status_code=status_code,
            reason=r.reason,
            content=content,
            encoding=r.encoding or r.apparent_encoding,
        )
