# -*- coding: utf-8 -*-
# Copyright (c) 2016 - 2020 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
""" Falcon Web Framework Adapter
"""
import logging

from ....rules_callbacks import BindingAccessorProvideData
from ..transports.framework import FrameworkTransportCallback

LOGGER = logging.getLogger(__name__)


class FalconFrameworkAdapter(object):

    def instrumentation_callbacks(self, runner, storage):
        return [
            FrameworkTransportCallback.from_rule_dict({
                "name": "ecosystem_falcon_transport",
                "rulespack_id": "ecosystem/transport",
                "block": False,
                "test": False,
                "hookpoint": {
                    "klass": "falcon::API",
                    "method": "__call__",
                    "strategy": "wsgi",
                },
                "callbacks": {},
                "priority": 90,
            }, runner, storage),
            BindingAccessorProvideData.from_rule_dict({
                "name": "ecosystem_falcon_request_provide_data",
                "rulespack_id": "ecosystem/framework",
                "data": {
                    "values": [
                        ["post", [
                            ["server.request.client_ip", "#.client_ip"],
                            ["server.request.method", "#.method"],
                            ["server.request.uri.raw", "#.request_uri"],
                            ["server.request.headers.no_cookies", "#.headers_no_cookies"],
                            ["server.request.cookies", "#.cookies_params"],
                            ["server.request.query", "#.query_params"],
                            ["server.request.body", "#.body_params"],
                            ["server.request.body.raw", "#.body"],
                            ["server.request.path_params", "#.rv[1]"],
                        ]]
                    ]
                },
                "block": True,
                "hookpoint": {
                    "klass": "falcon::API",
                    "method": "_get_responder",
                },
                "priority": 80,
            }, runner, storage),
            BindingAccessorProvideData.from_rule_dict({
                "name": "ecosystem_falcon_response_provide_data",
                "rulespack_id": "ecosystem/framework",
                "conditions": {
                    "post": {
                        "%and": [
                            "#.response",
                        ]
                    },
                },
                "data": {
                    "values": [
                        ["post", [
                            ["server.response.status", "#.response.status_code"],
                            ["server.response.headers.no_cookies", "#.response.headers_no_cookies"],
                            ["server.response.body.raw", "#.response.body"],
                        ]]
                    ]
                },
                "block": True,
                "hookpoint": {
                    "klass": "falcon::API",
                    "method": "__call__",
                    "strategy": "wsgi",
                },
                "priority": 80,
            }, runner, storage)
        ]
