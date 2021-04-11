# -*- coding: utf-8 -*-
import functools
import logging
import time

import requests
from requests.exceptions import ConnectionError

logger = logging.getLogger(__name__)


def retry(loop=3, delay=5):
    def trace(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(1, loop + 1):
                logger.debug(f'第{i}次請求 {args} {kwargs}')
                try:
                    return func(*args, **kwargs)
                except ConnectionError as e:
                    logger.warning(f'超時 重試第{i}次 {e}')
                    time.sleep(delay)

        return wrapper

    return trace


class HTTP:
    API_URL = "https://api.cloudflare.com/client/v4/"

    def __init__(self, AuthKey, AuthMail):
        self.AuthKey = AuthKey
        self.AuthMail = AuthMail

    @retry()
    def request(self, method, uri, **kwargs) -> dict:
        headers = {
            'X-Auth-Email': self.AuthMail,
            'X-Auth-Key': self.AuthKey,
            'Content-Type': 'application/json',
        }

        req = requests.api.request(method=method, url=f"{self.API_URL}{uri}", timeout=300, headers=headers, **kwargs)
        return req.json()

    def get(self, url, params=None, **kwargs) -> dict:
        r"""Sends a GET request.

        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary, list of tuples or bytes to send
            in the query string for the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        return self.request('get', url, params=params, **kwargs)

    def post(self, url=None, data=None, json=None, **kwargs) -> dict:
        r"""Sends a POST request.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json data to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        return self.request('post', url, data=data, json=json, **kwargs)

    def put(self, url=None, data=None, **kwargs) -> dict:
        r"""Sends a PUT request.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json data to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        return self.request('put', url, data=data, **kwargs)

    def delete(self, url=None, **kwargs):
        r"""Sends a DELETE request.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        return self.request('delete', url, **kwargs)
