# pylint: disable=no-self-use
# pylint: disable=dangerous-default-value

import json
import urllib.parse
import requests

from joinnector.helper.constant_helper import ConstantHelper


class RequestClient(object):
    '''
    key - api key
    secret - api secret
    '''

    def __init__(self, key, secret, mode):
        self.key = key
        self.secret = secret
        self.mode = mode

    def change_mode(self):
        self.mode="prod"

    def process_axios_get(self, url, headers, params={}):
        headers = {**headers,  **
                   ConstantHelper.get_setting_constant().API_BASE_HEADER}

        if headers["content-type"] is "application/x-www-form-urlencoded":
            headers.update(
                {"content-type": "application/x-www-form-urlencoded"})

        params = urllib.parse.urlencode(params, doseq=True)

        return requests.get(url, headers=headers, params=params)

    def process_axios_put(self, url, headers, params={}, data={}):
        headers = {**headers,  **
                   ConstantHelper.get_setting_constant().API_BASE_HEADER}

        if headers["content-type"] is "application/x-www-form-urlencoded":
            headers.update(
                {"content-type": "application/x-www-form-urlencoded"})

        params = urllib.parse.urlencode(params, doseq=True)

        return requests.put(url, headers=headers, params=params, data=json.dumps(data))

    def process_axios_delete(self, url, headers, params={}):
        headers = {**headers,  **
                   ConstantHelper.get_setting_constant().API_BASE_HEADER}

        if headers["content-type"] is "application/x-www-form-urlencoded":
            headers.update(
                {"content-type": "application/x-www-form-urlencoded"})

        params = urllib.parse.urlencode(params, doseq=True)

        return requests.delete(url, headers=headers, params=params)

    def process_axios_post(self, url, headers, params={}, data={}):
        headers = {**headers,  **
                   ConstantHelper.get_setting_constant().API_BASE_HEADER}

        if headers["content-type"] is "application/x-www-form-urlencoded":
            headers.update(
                {"content-type": "application/x-www-form-urlencoded"})

        params = urllib.parse.urlencode(params, doseq=True)

        print(headers)

        return requests.post(url, headers=headers, params=params, data=json.dumps(data))
