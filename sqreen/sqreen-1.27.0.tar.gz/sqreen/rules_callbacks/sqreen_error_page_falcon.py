# -*- coding: utf-8 -*-
# Copyright (c) 2016 - 2020 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
""" Custom error page for Falcon
"""
from .sqreen_error_page import HTTP_STATUS_CODE, BaseSqreenErrorPage


class SqreenErrorPageFalcon(BaseSqreenErrorPage):

    def pre(self, instance, args, kwargs, options):

        def _extract(req, resp, ex, params):
            return resp, ex

        resp, ex = _extract(*args, **kwargs)
        ret = self.handle_exception(ex)
        if ret is not None:
            status_code, body, headers = ret
            resp.body = body
            resp.headers.update(headers)
            resp.status = HTTP_STATUS_CODE.get(status_code) or "500 Internal Server Error"
            return {
                "status": "override",
                "new_return_value": True
            }
