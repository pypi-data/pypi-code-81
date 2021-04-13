# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 hcyjs.com, Inc. All Rights Reserved

"""
    @Time : 2021-02-02 17:38
    @Author : Yin Jian
    @Version：V 0.1
    @File : http.py
    @desc :
"""
import json as json_mod
import logging
import typing

from datavita.core.exc import exception
from datavita.core.transport import utils
from datavita.core.utils.compat import str

logger = logging.getLogger(__name__)


class Request:
    """
        包装request对象
    """

    def __init__(
            self,
            request_name: str,
            url: str,
            method: str = "GET",
            params: str = None,
            data: dict = None,
            json: dict = None,
            headers: dict = None,
            **kwargs
    ):
        self.request_name = request_name
        self.url = url
        self.method = method
        self.params = params
        self.data = data
        self.json = json
        self.headers = headers
        self.request_time = 0


REQUEST_UUID_HEADER_KEY = "DV-REQUEST-UUID"


class Response:
    """
        包装返回类
    """
    def __init__(
            self,
            url: str,
            method: str,
            request: Request = None,
            status_code: int = None,
            reason: str = None,
            headers: dict = None,
            content: str = None,
            encoding: str = None,
            **kwargs
    ):
        self.url = url
        self.method = method
        self.request = request
        self.status_code = status_code
        self.reason = reason
        self.content = content
        self.encoding = encoding
        self.response_time = 0
        self.headers = headers or {}
        self.request_uuid = REQUEST_UUID_HEADER_KEY

    def json(self, **kwargs) -> typing.Optional[dict]:
        """json will return the bytes of content"""
        if not self.content:
            return None

        try:
            return self._decode_json(**kwargs)
        except Exception as e:
            raise exception.InvalidResponseException(
                self.content, str(e), request_uuid=self.request_uuid
            )

    @property
    def text(self):
        """text will return the unicode string of content,
        see `requests.Response.text`
        """
        if not self.content:
            return str("")

        # Decode unicode from given encoding.
        try:
            content = str(self.content, self.encoding, errors="replace")
        except (LookupError, TypeError):
            content = str(self.content, errors="replace")
        return content

    def _decode_json(self, **kwargs):
        encoding = utils.guess_json_utf(self.content)
        if encoding is not None:
            try:
                return json_mod.loads(self.content.decode(encoding), **kwargs)
            except UnicodeDecodeError:
                pass
        return json_mod.loads(self.text, **kwargs)


class AbsCommonRequest:
    """ 抽象请求动作 """

    def send(self, req: Request):
        raise NotImplementedError
