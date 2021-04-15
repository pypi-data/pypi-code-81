# The MIT License (MIT)
#
# Copyright (c) 2016 Piper Merriam
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import itertools
import logging
import os
from web3 import HTTPProvider
from web3.utils.request import make_post_request
from klaytnetl.providers.request import make_post_request as make_kas_post_request
from klaytnetl.providers.retry_middleware import exception_retry_middleware, http_retry_request_middleware
from klaytnetl.providers.middlewares import combine_middlewares
from web3.utils.encoding import (
    FriendlyJsonSerde,
)
from eth_utils import (
    to_bytes,
    to_text,
    to_dict,
)

from web3.datastructures import (
    NamedElementOnion,
)

# Mostly copied from web3.py/providers/rpc.py. Supports batch requests.
# Will be removed once batch feature is added to web3.py https://github.com/ethereum/web3.py/issues/832
class BatchHTTPProvider(HTTPProvider):

    def make_batch_request(self, text):
        self.logger.debug("Making request HTTP. URI: %s, Request: %s",
                          self.endpoint_uri, text)
        request_data = text.encode('utf-8')
        raw_response = make_post_request(
            self.endpoint_uri,
            request_data,
            **self.get_request_kwargs()
        )
        response = self.decode_rpc_response(raw_response)
        self.logger.debug("Getting response HTTP. URI: %s, "
                          "Request: %s, Response: %s",
                          self.endpoint_uri, text, response)
        return response

def get_default_kas_endpoint():
    return "https://node-api.klaytnapi.com/v1/klaytn"

class KasBatchHTTPProvider:
    logger = logging.getLogger("klaytnetl.providers.KASBatchHTTPProvider")
    endpoint_uri = None
    _request_kwargs = None
    _headers = None
    _middlewares = NamedElementOnion([
        (http_retry_request_middleware, 'http_retry_request')
    ])
    _request_func_cache = (None, None)  # a tuple of (all_middlewares, request_func)

    @property
    def middlewares(self):
        return self._middlewares

    @middlewares.setter
    def middlewares(self, values):
        self._middlewares = tuple(values)

    def __init__(self, endpoint_uri=None, request_kwargs=None, credentials=None):
        if endpoint_uri is None:
            self.endpoint_uri = get_default_kas_endpoint()
        else:
            self.endpoint_uri = endpoint_uri

        self._request_kwargs = request_kwargs or {}
        self.request_counter = itertools.count()

    @to_dict
    def get_request_kwargs(self):
        if 'headers' not in self._request_kwargs:
            yield 'headers', self.get_request_headers()
        for key, value in self._request_kwargs.items():
            yield key, value

    def get_request_headers(self):
        return {
            'Content-Type': 'application/json',
            "x-chain-id": "8217"
        }

    def make_batch_request(self, json_dict):
        self.logger.debug("Making request HTTP. URI: %s, Request: %s",
                          self.endpoint_uri, json_dict)
        # TODO:
        # request_data = text.encode()
        raw_response = make_kas_post_request(
            self.endpoint_uri,
            json_dict,
            **self.get_request_kwargs()
        )

        response = self.decode_rpc_response(raw_response)
        self.logger.debug("Getting response HTTP. URI: %s, "
                          "Request: %s, Response: %s",
                          self.endpoint_uri, json_dict, response)
        return response

    def request_func(self, outer_middlewares):

        all_middlewares = tuple(outer_middlewares) + tuple(self.middlewares)

        cache_key = self._request_func_cache[0]

        if cache_key is None or cache_key != all_middlewares:
            self._request_func_cache = (
                all_middlewares,
                self._generate_request_func(midllewares=all_middlewares)
            )
        return self._request_func_cache[-1]


    def _generate_request_func(self, middlewares):
        return combine_middlewares(
            middlewares=middlewares,
            provider_request_fn=self.make_request)


    def make_request(self, method, params):
        self.logger.debug("Making request HTTP. URI: %s, Method: %s",
                          self.endpoint_uri, method)
        request_data = self.encode_rpc_request(method, params)
        raw_response = make_kas_post_request(
            self.endpoint_uri,
            request_data,
            **self.get_request_kwargs()
        )
        response = self.decode_rpc_response(raw_response)
        self.logger.debug("Getting response HTTP. URI: %s, "
                          "Method: %s, Response: %s",
                          self.endpoint_uri, method, response)
        return response


    def decode_rpc_response(self, response):
        text_response = to_text(response)
        return FriendlyJsonSerde().json_decode(text_response)

    def encode_rpc_request(self, method, params):
        rpc_dict = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or [],
            "id": next(self.request_counter),
        }
        return rpc_dict

    def isConnected(self):
        # FIXME: replace with a proper API
        return True