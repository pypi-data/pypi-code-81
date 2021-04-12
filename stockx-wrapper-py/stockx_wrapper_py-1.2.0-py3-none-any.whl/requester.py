import json
import requests

from stockx_wrapper.settings import ALGOLIA_HEADERS


class Requester:
    def __init__(self):

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0',
            'sec-fetch-dest': 'none',
            'accept': '*/*',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'cors',
            'accept-language': 'en-US'
        }

    def get(self, url, params=None):
        """
        Perform a http get request.

        :param url: str
        :param params: dict, optional

        :return: dict
            Json format
        """
        response = requests.get(url, headers=self.headers, params=params)
        data = json.loads(response.content)
        return data

    def post(self, url, params=None, body=None):
        """
        Perform a http post request.

        :param url: str
        :param params: dict, optional
        :param body: dict, optional

        :return:
        """

        _headers = {**self.headers, **ALGOLIA_HEADERS}

        response = requests.post(url, headers=_headers, params=params, json=body)
        data = json.loads(response.content)
        return data


requester = Requester()
