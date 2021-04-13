#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 hcyjs.com, Inc. All Rights Reserved

"""
    @Time : 2021-01-31 1:43
    @Author : Yin Jian
    @Version：V 0.1
    @File : exception.py
    @desc : 统一异常
"""
import collections

from datavita.core.utils import compat
from datavita.core.common.contants import EXCEPTION_DICT


class DVException(Exception):
    @property
    def retryable(self):
        """
            重试
        :return:
        """
        return False


MAX_COMMON_RET_CODE = 2000


class TransportException(DVException):
    pass


class HTTPStatusException(TransportException):
    """
        http异常
    """

    def __init__(self, status_code: int, url: str = None):
        self.status_code = status_code
        self.url = url

    @property
    def retryable(self):
        """
                重试标记
        :return:
        """
        return self.status_code in [429, 502, 503, 504]

    def __str__(self):
        return "[{status_code}] {url} http status error".format(
            status_code=self.status_code, url=self.url
        )


class CommonException(TransportException):
    """
        普通异常
    """

    def __init__(self, status_code: int):
        self.status_code = status_code

    @property
    def retryable(self):
        """
                重试标记
        :return:
        """
        return self.status_code in [429, 502, 503, 504]

    def __str__(self):
        msg = EXCEPTION_DICT.get(self.status_code, "未知错误")
        return "[{status_code}] {msg} ".format(
            status_code=self.status_code, msg=msg
        )


class InvalidResponseException(TransportException):
    def __init__(self, content: bytes, message: str, request_uuid: str = None):
        self.content = content
        self.message = message
        self.request_uuid = request_uuid

    @property
    def retryable(self):
        return False

    def __str__(self):
        return "[{uuid}] {self.message}: {self.content}".format(
            self=self, uuid=self.request_uuid or "*"
        )


class RetCodeException(DVException):
    def __init__(
            self, action: str, code: int, message: str, request_uuid: str = None
    ):
        self.action = action
        self.code = code
        self.message = message
        self.request_uuid = request_uuid

    @property
    def retryable(self):
        return self.code > MAX_COMMON_RET_CODE

    def __str__(self):
        return "[{uuid}] {self.action} - {self.code}: {self.message}".format(
            self=self, uuid=self.request_uuid or "*"
        )

    def json(self):
        return {
            "RetCode": self.code,
            "Message": self.message or "",
            "Action": self.action or "",
        }


class RetryTimeoutException(DVException):
    pass


class ValidationException(DVException):
    def __init__(self, e=None):
        if isinstance(e, compat.string_types):
            self.errors = [e]
        elif isinstance(e, collections.Iterable):
            self.errors = e or []
        else:
            self.errors = [e]

    @property
    def retryable(self):
        return False

    def __str__(self):
        return str([str(e) for e in self.errors])
