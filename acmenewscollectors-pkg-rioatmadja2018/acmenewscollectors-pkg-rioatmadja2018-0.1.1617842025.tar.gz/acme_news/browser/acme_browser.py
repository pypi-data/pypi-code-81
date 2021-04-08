#!/usr/bin/env python
from selenium.webdriver import PhantomJS
from selenium.webdriver.phantomjs.webdriver import WebDriver
from pandas.io.json import json_normalize
from requests import request
from typing import Dict, List
import json

class ACMEBrowser(object):
    """
    NAME
        ACMEBrowser

    DESCRIPTION
    -----------
        This is a parent class for all the engines and a wrapper class that calls PhantomJS browser


    FUNCTIONS
        __init__
        __browser__
        browser
        fetch_api_request
        transform_requests

    """

    def __init__(self):
        self.url: str = ""
        self.driver = None
        self.headers: Dict = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'User-Agent': 'User-Agent: Mozilla/3.0 (X11; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0'

        }

    def __browser__(self, url: str):
        try:
            self.driver.get(url=url)
            return self.driver

        except ConnectionError as e:
            raise ConnectionError(f"Unable to connect to the following URLs {url}") from e

    def browser(self, url: str) -> WebDriver:
        if not url:
            raise ValueError(f"Please provide the right URL.")

        self.url = url
        try:
            self.driver = PhantomJS()

        except FileNotFoundError as e:
            raise FileNotFoundError(f"Unable to find phantomjs binary") from e

        else:
            return self.__browser__(url=self.url)

    def fetch_api_request(self, api_endpoint: str, method: str = 'GET', headers: Dict = {}) -> bytes:
        if not api_endpoint:
            raise ValueError(f"Please provide the right api endpoint {api_endpoint}.")

        if not headers:
            headers: Dict = self.headers

        try:
            api_response: bytes = request(method=method, url=api_endpoint, headers=headers).text.encode('utf-8')
            return api_response

        except ConnectionError as e:
            raise ConnectionError(f"Unable to connect to the following endpoint {api_endpoint}") from e


    def transform_requests(self, response: bytes) -> Dict:
        if not response:
            raise ValueError("Please the right HTTP response")

        if not isinstance(response, bytes):
            raise TypeError(f"Response must be Bytes types and not {type(response)} ")

        try:
            return json.loads(response)

        except TypeError as e:
            raise TypeError(f"Unable to transform the given response.") from e


    def normalize(self, response: List[Dict]) -> List[Dict]:
        if not isinstance(response, List) and not isinstance(response[0], Dict):
            raise TypeError("Response must be a Dict instance.")

        return json_normalize(response).to_dict(orient='record')
