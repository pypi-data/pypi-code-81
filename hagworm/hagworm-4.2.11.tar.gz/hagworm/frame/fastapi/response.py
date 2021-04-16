# -*- coding: utf-8 -*-

from fastapi.responses import UJSONResponse

from hagworm.extend.struct import Result


class Response(UJSONResponse):

    def render(self, content):
        return super().render(Result(data=content))


class ErrorResponse(Exception, UJSONResponse):

    def __init__(self, error_code, content=None, status_code=200, **kwargs):

        self.error_code = error_code

        Exception.__init__(self)
        UJSONResponse.__init__(self, content, status_code, **kwargs)

    def render(self, content):
        return super().render(Result(code=self.error_code, data=content))
