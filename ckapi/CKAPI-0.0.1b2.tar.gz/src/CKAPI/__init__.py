# encoding: utf-8
import os
import json
import requests
import logging
from robot.api.deco import keyword

dir_file = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')

class CKAPI(object):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = 0.1

    def __init__(self):
        logging.basicConfig()
        logging.getLogger().setLevel(logging.INFO)
        logger = logging.getLogger(__name__)

    @keyword('GET API')
    def getAPI(self, url, parameters={}):
        """
        Examples:
        | ${Return} | `GET API` | https://reqres.in/api/users?page=2  |                                                 | 
        | ${Return} | `GET API` | https://reqres.in/api/users?page=2  | parameters={"name": "morpheus","job": "leader"} |
        """
        return_api = requests.get(url, params=parameters)
        return return_api

    @keyword('POST API')
    def postAPI(self, url, body, headers={}):
        """
        Examples:
        | ${Return} | `POST API` | https://reqres.in/api/users?page=2  | body={"name": "morpheus","job": "leader"} |                                                |
        | ${Return} | `POST API` | https://reqres.in/api/users?page=2  | body={"name": "morpheus","job": "leader"} | headers={"Content-Type": "application/json"}   |
        """
        return_api = requests.post(url, data=body, headers=headers, allow_redirects=False)
        return return_api

    @keyword('Format JSON')
    def jprint(self, obj):
        """
        create a formatted string of the Python JSON object

        Examples:
        | ${Return} | `Format JSON` | obj={"name": "morpheus","job": "leader"} |   
        """
        text = json.dumps(obj, sort_keys=False, indent=4)
        return text