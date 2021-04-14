# -*- coding: utf-8 -*-
# Author: ZKH
# Date：2021/2/24
import json
from werkzeug.exceptions import HTTPException
from flask import request


class BasicException(BaseException):
    """for apollo exceptions"""

    def __init__(self, msg: str):
        self._msg = msg
        print(msg)

    def __str__(self):
        return "%s: %s" % (self.__name__, self._msg)


class NameSpaceNotFoundException(BasicException):
    """for apollo exceptions"""


class ServerNotResponseException(BasicException):
    """for apollo exceptions"""


# class _Exception(HTTPException):
#     errmsg = None
#     errcode = None
#     data = None
#     code = None
#
#     def __init__(self, errmsg=None, errcode=None, data=None, code=None):
#         super(_Exception, self).__init__(errmsg, None)
#
#         if errmsg is not None:
#             self.errmsg = errmsg
#
#         if errcode is not None:
#             self.errcode = errcode
#
#         if data is not None:
#             self.data = data
#
#         if code is not None:
#             self.code = code
#
#     def get_body(self, environ=None):
#         body = dict(
#             errcode=self.errcode,
#             errmsg=self.errmsg,
#             data=self.data
#         )
#         text = json.dumps(body, sort_keys=False, ensure_ascii=False)
#
#         return text
#
#     def get_headers(self, environ=None):
#         return [('Content-Type', 'application/json')]
#
#
# class APIException(_Exception):
#     code = 400
#     errmsg = 'sorry, request error'
#     errcode = "-1"
#
#
# class PortalException(_Exception):
#     code = 500
#     errmsg = 'sorry, internal error'
#     errcode = "-1"

class _Exception(HTTPException):
    data = None
    bizExtMap = None
    code = None
    header = {}
    headers = {}
    msg = ""
    msgCode = ""
    msgDetail = ""
    success = False

    def __init__(self, msgDetail="", data=None, bizExtMap=None, code=None, header=None,
                 headers=None, msg="", msgCode="", success=False, **kwargs):

        super(_Exception, self).__init__(msgDetail, None)

        self.data = data
        self.bizExtMap = bizExtMap

        if code is not None:
            self.code = code

        if header is None:
            req_data = request.json

            if isinstance(req_data, dict) and 'header' in req_data and isinstance(req_data['header'], dict):
                self.header = {
                    "xAppId": req_data['header'].get("xAppId", ""),
                    "xTraceId": req_data['header'].get("xTraceId", "")
                }
        else:
            self.header = header

        self.headers = headers
        self.msg = msg
        self.msgCode = msgCode
        self.msgDetail = msgDetail
        self.success = success
        self.kwargs = kwargs

    def get_body(self, environ=None):
        body = {
            "data": self.data,
            "bizExtMap": self.bizExtMap,
            "code": self.code,
            "header": self.header,
            "headers": self.headers,
            "msg": self.msg,
            "msgDetail": self.msgDetail,
            "msgCode": self.msgCode,
            "success": self.success,
            **self.kwargs,
        }

        text = json.dumps(body, sort_keys=False, ensure_ascii=False)

        return text

    def get_headers(self, environ=None):
        return [('Content-Type', 'application/json')]


class APIException(_Exception):
    code = 400
    msgDetail = 'sorry, request error'
    msgCode = "-1"


class PortalException(_Exception):
    code = 500
    msgDetail = 'sorry, internal error'
    msgCode = "-1"
