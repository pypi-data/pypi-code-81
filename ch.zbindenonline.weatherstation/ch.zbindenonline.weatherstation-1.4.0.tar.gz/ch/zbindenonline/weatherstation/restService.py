import datetime
import json
import logging
import re
import sys
from enum import Enum, unique
from pathlib import Path

import requests


class RestService:
    def __init__(self, url):
        self.url = url
        self.headers = {'User-Agent': 'python', 'Accept': 'application/json'}

    def login(self):
        pass

    def logout(self):
        pass


@unique
class Response(Enum):
    OK = 0
    DUPLICATE = 2


class RestServicePictures(RestService):
    def __init__(self, url, camera_id, client_id, client_secret, username, password):
        super().__init__(url)
        self.camera_id = camera_id
        self.auth = {'grant_type': 'password', 'client_id': client_id, 'client_secret': client_secret,
                     'username': username, 'password': password}

    def login(self):
        logging.debug("Try to login to " + self.url + '/oauth/token')
        # logging.debug(json.dumps(self.auth))
        try:
            login_headers = {'Content-Type': 'application/json'}
            response = requests.post(self.url + '/oauth/token', data=json.dumps(self.auth), headers=login_headers,
                                     timeout=20)
        except requests.exceptions.RequestException as e:
            logging.exception("RequestException occured: " + str(e))
            sys.exit(1)

        if not response.ok:
            response.raise_for_status()
        str_response = response.content.decode('utf-8')
        # logging.debug(str_response)
        if str_response:
            jwtdata = json.loads(str_response)
            jwt = jwtdata['access_token']
            logging.debug(jwt)
            self.headers['Accept'] = 'application/json'
            self.headers['Authorization'] = 'Bearer ' + jwt

    def logout(self):
        logging.debug("Logging out from " + self.url + '/oauth/token')
        response = requests.delete(self.url + '/oauth/token', headers=self.headers, timeout=15)
        logging.debug(response)

    def post_picture(self, picture):
        # logging.debug('Headers:')
        # logging.debug(self.headers)
        filename = Path(picture).with_suffix('').name
        if re.match(r'[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{6}', filename):
            taken_at = datetime.datetime.strptime(filename, '%Y-%m-%d_%H%M%S')
        elif re.match(r'[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{4}', filename):
            taken_at = datetime.datetime.strptime(filename, '%Y-%m-%d_%H%M')
        else:
            logging.warning('Unsupported file format ' + picture)
            return 1
        logging.debug(taken_at)
        picture_data = {'taken_at': taken_at.strftime("%Y-%m-%d %H:%M:%S")}
        logging.debug(picture_data)
        file = {'image': open(picture, 'rb')}
        response = requests.post(self.url + '/cameras/' + self.camera_id + '/pictures', files=file, data=picture_data,
                                 headers=self.headers, timeout=300)
        logging.debug(response)
        if response.ok:
            logging.info('Successfully posted picture ' + picture)
        elif response.status_code == 409:
            logging.info('Picture exists already: ' + picture)
            return Response.DUPLICATE
        else:
            logging.error('Posting picture ' + picture + ' had an error')
            logging.error('Raw error: ' + response.text)
            str_response = response.content.decode('utf-8')
            json_data = json.loads(str_response)
            logging.error('Json error: ' + json_data)
            response.raise_for_status()
        return Response.OK
