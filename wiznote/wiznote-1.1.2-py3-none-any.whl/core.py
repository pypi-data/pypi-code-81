# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021/3/15 22:33
# @Author  : https://github.com/536
import abc

import requests

from .error import WizError


class API(metaclass=abc.ABCMeta):
    AS_URL = 'https://as.wiz.cn'

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

        self.session = requests.Session()
        self.session.hooks = dict(response=self.process_response)

        self.base_info = {}

    def url(self, url: str, **kwargs):
        return url.format(AS_URL=self.AS_URL,
                          kbServer=self.kbServer,
                          kbGuid=self.kbGuid,
                          **kwargs)

    def process_response(self, r, *args, **kwargs):
        r.raise_for_status()

        if 'json' not in r.headers.get('Content-Type'):
            return r

        r_json = r.json()
        returnCode = r_json.get('returnCode')  # NOQA
        if returnCode == 200:
            if not r.request.headers.get('X-Wiz-Token'):
                self.base_info = r_json.get('result', {})
                self.session.headers.update({'X-Wiz-Token': self.token})
            return r
        else:
            returnMessage = r_json.get('returnMessage')  # NOQA
            raise WizError(returnCode, returnMessage, *args, **kwargs, response=r)

    @property
    def token(self):
        return self.base_info.get('token')

    @property
    def userId(self):  # NOQA
        return self.base_info.get('userId')

    @property
    def userGuid(self):  # NOQA
        return self.base_info.get('userGuid')

    @property
    def displayName(self):  # NOQA
        return self.base_info.get('displayName')

    @property
    def kbType(self):  # NOQA
        return self.base_info.get('kbType')

    @property
    def kbServer(self):  # NOQA
        return self.base_info.get('kbServer')

    @property
    def kbXmlRpcServer(self):  # NOQA
        return self.base_info.get('kbXmlRpcServer')

    @property
    def kbGuid(self):  # NOQA
        return self.base_info.get('kbGuid')

    @property
    def mobile(self):
        return self.base_info.get('mobile')

    @property
    def email(self):
        return self.base_info.get('email')

    @property
    def mywizEmail(self):  # NOQA
        return self.base_info.get('mywizEmail')
