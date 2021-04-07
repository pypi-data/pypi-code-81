#
# Copyright 2020 Thomas Bastian, Jeffrey Goff, Albert Pang
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

'''
#
# ContentProvider
#
# Provides some content through getContent()
#
# Authors: Thomas Bastian, Albert Pang
#
'''

import json
import jstyleson
import logging
import os
import requests
from .RedisStore import RedisStore
from yaml import load, dump, FullLoader
from yaml.parser import ParserError


# Logger
log = logging.getLogger(__name__)


class ContentProvider():
    def __init__(self):
        pass

    def __str__(self):
        return ""

    def getContent(self):
        return None

    def getContentData(self):
        ''' Attempt to decode the content read and returns a dictionary or a list.
        Will attempt to decode the content as JSON or YAML

        Parameter
        ---------
            None

        Returns
        -------
            dict or list : A dictionary if able to convert content as dict or list. None if unsuccessful
        '''
        content = self.getContent()

        try:
            d = jstyleson.loads(content)
            log.debug("Found JSON")
            return d
        except ValueError as e:
            try:
                d = load(content, Loader=FullLoader)
                log.debug("Found YAML")
                return d
            except ParserError:
                log.debug("Did not find JSON or YAML str")
                return None

    def reprJSON(self):
        data = {}
        data['ContentProvider'] = str(self)
        return data

    def getContentJSON(self):
        '''Attempt to return a JSON object from the content source.

        Parameters
        ----------
            None

        Returns
        -------
            str : A JSON object string. Returns None if unable to convert content to JSON object
        '''
        data = self.getContentData()

        if isinstance(data, dict) or isinstance(data, list):
            log.debug("Found dict or list")
            return json.dumps(data)
        else:
            return None

    def getContentYml(self):
        '''Attempt to return a YAML formatted string from the content source.

        Parameters
        ----------
            None

        Returns
        -------
            str : A string in YAML format. Returns None if unable to convert content to JSON object
        '''
        data = self.getContentData()

        if isinstance(data, dict) or isinstance(data, list):
            log.debug("Found dict or list")
            return dump(data)
        else:
            return None


    def __iter__(self):
        return None

    def _next(self):
        raise StopIteration

    def __next__(self):
        return self._next()

    def next(self):
        return self._next()


class FileContentProvider(ContentProvider):
    def __init__(self, filename):
        self.filename = filename

    def __str__(self):
        return "file://" + self.filename

    def getContent(self):
        fileHandle = open(self.filename, 'r')
        fileContent = fileHandle.read()
        fileHandle.close()
        return fileContent


class MultiFileContentProvider(ContentProvider):
    def __init__(self, dirname, endswith):
        self.dirname = dirname
        self.endswith = endswith
        self.fileIterator = None

    def __str__(self):
        return "dir://" + self.dirname + ", ending with: " + self.endswith

    def __repr__(self):
        return "dir://" + self.dirname + ", ending with: " + self.endswith

    def getContent(self):
        raise "unimplemented"

    def __iter__(self):
        self.fileIterator = iter(os.listdir(self.dirname))
        return self

    def _next(self):
        try:
            while True:
                filename = next(self.fileIterator)
                if filename.endswith(self.endswith):
                    break
            p = os.path.join(self.dirname, filename)
            return FileContentProvider(p)

        except StopIteration:
            raise StopIteration


class RedisStoreContentProvider(ContentProvider):
    def __init__(self, redisUrl, redisKey):
        self.redisUrl = redisUrl
        self.redisKey = redisKey

    def __str__(self):
        return self.redisUrl + "/" + self.redisKey

    def getContent(self):
        r = RedisStore(url=self.redisUrl)
        content = r.get(self.redisKey)
        return content


class MultiKeyRedisStoreContentProvider(ContentProvider):
    def __init__(self, redisUrl, redisKeysPatterns):
        self.redisUrl = redisUrl
        self.redisKeysPattern = redisKeysPatterns

    def __str__(self):
        return self.redisUrl + "/" + self.redisKeysPattern

    def __repr__(self):
        return self.redisUrl + "/" + self.redisKeysPattern

    def getContent(self):
        raise "unimplemented"

    def __iter__(self):
        r = RedisStore(url=self.redisUrl)
        redisKeys = r.keys(pattern=self.redisKeysPattern)
        self.fileIterator = iter(redisKeys)
        return self

    def _next(self):
        try:
            while True:
                redisKey = next(self.fileIterator)
                break
            return RedisStoreContentProvider(self.redisUrl, redisKey)

        except StopIteration:
            raise StopIteration


class  ApiContentProvider(ContentProvider):
    def __init__(self, apiUrl, endpoint, params=None, sip_mode=True):
        # TODO: refactor RR and ND scripts and change default to sip_mode=False
        self.apiUrl = apiUrl
        self.endpoint = endpoint
        self.params = params
        self.sip_mode = sip_mode

    def __str__(self):
        return self.apiUrl + "/" + self.endpoint

    def getContent(self):
        try:
            if self.params is not None:
                response = requests.request("GET", "{}/{}".format(self.apiUrl, self.endpoint), params=self.params)
            else:
                response = requests.request("GET", "{}/{}".format(self.apiUrl, self.endpoint))
            # NOTE: the 'msg' is for SIP backward-compatibility
            if self.sip_mode:
                return json.dumps(response.json()['msg'])
            else:
                return json.dumps(response.json())
        except Exception as e:
            log.error("Cannot retrieve content from {str(self)} ({e})")
            return ""

    def getContentByEndpointParam(self, param=None):
        '''
        Similar to getContent(), instead of passing the parameters in the form or URL query string
        such as:
            /url/endpint?key1=value1&key2=value2
        pass the single parameter as a suffix of the URL

            /url/endpoint/param
        '''
        try:
            if param:
                url = "{}/{}/{}".format(self.apiUrl, self.endpoint, param)
                response = requests.request("GET", url)
            else:
                response = requests.request("GET", "{}/{}".format(self.apiUrl, self.endpoint))
            # NOTE: the 'msg' is for SIP backward-compatibility
            if self.sip_mode:
                return json.dumps(response.json()['msg'])
            else:
                return json.dumps(response.json())
        except Exception:
            log.error("Cannot retrieve content from {str(self)} ({e})")
            return ""
