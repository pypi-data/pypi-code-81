import unittest

import logging
import responses
import json

# import client library
from arthurai import ArthurAI

class BaseTest(unittest.TestCase):

    _base_url = 'http://mock'
    _content_type_json = 'application/json'

    @classmethod
    def setUpClass(cls):
        logging.info("Base Set up")

        cls.access_key = "FAKE_ACCESS_KEY"

        config = {
            'access_key': cls.access_key,
            'url': BaseTest._base_url,
            'offline': True
        }
        cls.arthur = ArthurAI(config)

    @classmethod
    def tearDownClass(cls):
        logging.info("Base Tear down")
        pass


    def mockPost(self, append_url, dict_to_return, request_type=responses.POST, status=200):
        '''
        Adds a mock 200 response

        :param append_url: the url to the base url
        :param dict_to_return: the dictionary to return as json
        :return: None
        '''

        responses.add(request_type, BaseTest._base_url + append_url,
                      json.dumps(dict_to_return), status=status,
                      content_type=self._content_type_json)

    def mockPost500(self, append_url, request_type=responses.POST):
        responses.add(request_type, BaseTest._base_url + append_url,
                      json.dumps({"Message": "There has been a server side exception"}), status=500,
                      content_type=self._content_type_json)


