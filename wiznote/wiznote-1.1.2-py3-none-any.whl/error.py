# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021/3/15 22:34
# @Author  : https://github.com/536
from requests import RequestException


class WizError(RequestException):
    def __init__(self, code, message, *args, **kwargs):
        super(WizError, self).__init__(response=kwargs.get('response'))

        self.code = code
        self.message = message

    def __str__(self):
        return '[{}][{}][{}]'.format(self.code, self.message, self.request.url)
