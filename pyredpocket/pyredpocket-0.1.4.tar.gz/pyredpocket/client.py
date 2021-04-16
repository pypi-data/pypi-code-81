
import re

import requests

from pyredpocket.details import AccountDetails, LineDetails

BASE_URL = 'https://www.redpocket.com/'
URL_LOGIN = BASE_URL + 'login'
URL_POST_LOGIN = BASE_URL + 'my-lines'
URL_GET_OTHER_LINES = BASE_URL + 'account/get-other-lines'
URL_GET_DETAILS = BASE_URL + 'account/get-details?id={}&type=api'


class RedPocketLoginError(Exception):
    pass


class RedPocket(object):

    def __init__(self, username, password, auto=True, hashes=[]):
        self._client = requests.Session()
        self._logged_in = False
        self._username = username
        self._password = password

        self.hashes = hashes
        self.details = []

        if auto:
            self.process()

    def _extract_csrf(self, text):
        return re.findall(r'name="csrf" value="([\w|-]+)"', text)[0]

    def process(self):
        if not self._logged_in:
            self._login()

        if self.hashes == []:
            self.hashes = self._get_hashes()

        for has in self.hashes:
            self.details.append(self._get_details(has))

    def _login(self):

        #
        req = self._client.get(URL_LOGIN)
        req.raise_for_status()
        data = {
            'mdn': self._username,
            'password': self._password,
            'csrf': self._extract_csrf(req.text),
        }

        req = self._client.post(URL_LOGIN, data=data)
        req.raise_for_status()

        if req.url == URL_POST_LOGIN:
            self._loggedIn = True
        else:
            raise RedPocketLoginError

    def _get_hashes(self):
        if not self._logged_in:
            self._login()

        req = self._client.get(URL_GET_OTHER_LINES)
        req.raise_for_status()

        processed_details = AccountDetails.from_dict(**req.json())
        return [i.hash for i in processed_details.confirmed_lines]

    def _get_details(self, hashId):
        req = self._client.get(URL_GET_DETAILS.format(hashId))
        req.raise_for_status()

        return LineDetails.from_dict(**req.json())
