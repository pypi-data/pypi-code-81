# -*- coding: utf-8 -*-
# Author: ZKH
# Date：2021/2/24
import json
from werkzeug.exceptions import HTTPException


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


class _Exception(HTTPException):
    errmsg = None
    errcode = None
    data = None
    code = None

    def __init__(self, errmsg=None, errcode=None, data=None, code=None):
        super(_Exception, self).__init__(errmsg, None)

        if errmsg is not None:
            self.errmsg = errmsg

        if errcode is not None:
            self.errcode = errcode

        if data is not None:
            self.data = data

        if code is not None:
            self.code = code

    def get_body(self, environ=None):
        body = dict(
            errcode=self.errcode,
            errmsg=self.errmsg,
            data=self.data
        )
        text = json.dumps(body, sort_keys=False, ensure_ascii=False)

        return text

    def get_headers(self, environ=None):
        return [('Content-Type', 'application/json')]


class APIException(_Exception):
    code = 400
    errmsg = 'sorry, request error'
    errcode = "-1"


class PortalException(_Exception):
    code = 500
    errmsg = 'sorry, internal error'
    errcode = "-1"
