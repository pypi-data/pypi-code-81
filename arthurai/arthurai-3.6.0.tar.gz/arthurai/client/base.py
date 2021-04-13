import io
import json
import os
import platform
import requests
import concurrent.futures
import threading
import time
import logging
from urllib.parse import urlparse

from typing import Optional

from arthurai.common.exceptions import MissingParameterError, InternalValueError
from arthurai.version import __version__

logger = logging.getLogger(__name__)


class BaseApiClient(object):
    """docstring for BaseApiClient"""

    def __init__(self, access_key=None, url=None, base_path=None, thread_workers=10, verify_ssl=True, offline=False, **kwargs):
        """Client which maintains REST calls and connection to API

        :param access_key: API key
        :param url: URL of the api/arthur server
        :param thread_workers: the number of workers the client requires when uploading inferences
        """
        self.access_key = kwargs.get('access_key', access_key)
        url = kwargs.get('url', url)
        if self.access_key is None:
            self.access_key = os.getenv('ARTHUR_API_KEY')
        if url is None:
            url = os.getenv('ARTHUR_ENDPOINT_URL')

        if url is None or self.access_key is None:
            raise MissingParameterError("Please set api key and url either via environment variables "
                                        "(`ARTHUR_API_KEY` and `ARTHUR_ENDPOINT_URL`) or by passing parameters "
                                        "`access_key` and `url`.")

        self.pool = concurrent.futures.ThreadPoolExecutor(max_workers=thread_workers)
        self.base_path = base_path
        self.verify_ssl = verify_ssl
        self.user_agent = None

        parsed_url = urlparse(url)
        if parsed_url.netloc and parsed_url.path:
            logger.warning(f"Path of '{parsed_url.path}' is not needed and is omitted.") 
        if parsed_url.scheme and not parsed_url.netloc:
            raise InternalValueError("Please make sure your url has a valid netloc.")
        if parsed_url.query:
            logger.warning(f"Query params of '{parsed_url.query}' is not needed and is omitted.") 

        if parsed_url.scheme in ('http', 'https'):
            self.url = parsed_url.scheme + "://" + (parsed_url.netloc or parsed_url.path)
        else:
            logger.warning(f"Url scheme of '{parsed_url.scheme}' is incorrect or not provided. Defaulted to 'https'.") 
            self.url = "https://" + (parsed_url.netloc or parsed_url.path)

        if not offline:
            user_org = self._get_current_user_org()
            agent_info = f"arthur-sdk/{__version__} (system={platform.system()}, org={user_org})" if user_org \
                else f"arthur-sdk/{__version__} (system={platform.system()})"
            self.user_agent = agent_info

    def _get_current_user_org(self) -> Optional[str]:
        url = f"{self.base_path}/users/me"
        resp = self.get(url, return_raw_response=True)
        if resp.status_code == 200:
            response_body = resp.json()
            if "organization_id" in response_body:
                return response_body["organization_id"]
        else:
            logger.debug(f"Failed to get current user organization, received response code {resp.status_code} with body {resp.content}")
        return None

    def send(self, url, method='GET', data=None, files=None, params=None, headers=None, return_raw_response=False,
             retries=0):
        """Sends the specified data with headers to the given url with the given request type

        :param retries: Number of times to retry the request if it results in a 400 or higher response code
        :param return_raw_response: If true do not filter request response, return raw object
        :param url: url to send data to
        :param method: REST call type, POST, GET, PUT, DELETE
        :param data: the data to send
        :param headers: headers to use in the REST call
        :return: response of the REST call
        """
        if headers is None:
            headers = {}

        if self.user_agent is not None:
            headers['User-Agent'] = self.user_agent

        if not url.startswith(('http://', 'https://')):
            url = '{base}{endpoint}'.format(
                base=self.url,
                endpoint=url
            )
        else:
            url = url

        # append the authentication headers to all requests
        headers = headers.copy()
        if self.access_key:
            if self.base_path and 'v3' in self.base_path:
                headers['Authorization'] = self.access_key
            else:
                headers['X-API-KEY'] = self.access_key

        headers['Content-Type'] = headers.get('Content-Type', 'application/json')
        headers['Accept'] = headers.get('Accept', 'application/json')

        # convert JSON data to a string
        if headers.get('Content-Type') == 'multipart/form-data':
            pass

        elif data:
            data = json.dumps(data)

        # send request to the test client and return the response
        if headers.get('Content-Type') == 'multipart/form-data':
            headers.pop('Content-Type')
            multipart = True
            logger.debug("Sending multipart request: %s %s\nHeaders: %s", method, url, headers)
            rv = requests.request(method, url, data=data, files=files, headers=headers, verify=self.verify_ssl)
        else:
            multipart = False
            logger.debug("Sending request: %s %s\nHeaders: %s\nData: %s", method, url, headers, data)
            rv = requests.request(method, url, data=data, params=params, headers=headers, verify=self.verify_ssl)

        attempt_retries = 0
        while attempt_retries < retries and rv.status_code >= 400:
            time.sleep(0.05)
            logger.debug(f"Request failed with status {rv.status_code} auto retry {attempt_retries + 1}/{retries}")
            if multipart:
                for fkey in files:
                    try:
                        files[fkey].seek(0)
                    except AttributeError:
                        continue
                rv = requests.request(method, url, data=data, files=files, headers=headers, verify=self.verify_ssl)
            else:
                rv = requests.request(method, url, data=data, params=params, headers=headers, verify=self.verify_ssl)
            attempt_retries += 1

        logger.debug(f"[{threading.current_thread().getName()}] Rest Call Response Time: {rv.elapsed.total_seconds() * 1000} ms")
        logger.debug("Received response: %d %s\nHeaders: %s\nContent: %s", rv.status_code, rv.url, rv.headers, rv.content)
        if return_raw_response:
            return rv

        return self._response(rv)

    def _response(self, rv):
        """Depending on the type of response from the server, parses the response and returns

        :param rv: response from the REST call
        :return: parsed response
        """
        # return error codes as raw responses
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
        if rv.status_code >= 400:
            return rv.content
        if rv.request.headers.get('Accept') == 'application/octet-stream':
            return io.BytesIO(rv.content)
        # return the content if the the return type is an image
        if rv.headers.get('Content-Type') == 'image/jpeg' \
                or rv.headers.get('Content-Type') == 'text/csv' \
                or rv.headers.get('Content-Type') == 'avro/binary' \
                or rv.headers.get('Content-Type') == 'parquet/binary':
            return rv.content

        try:
            response = rv.json()
        except ValueError:
            response = rv.content

        return response

    def get(self, url, headers={}, params=None, return_raw_response=False, retries=0):
        """
        Sends a GET request to the given url with the given headers
        :param retries: Number of times to retry the request if it results in a 400 or higher response code
        :param return_raw_response: If true do not filter response, return raw object
        :param url: url to send request to
        :param headers: headers to use in the request
        :return: response of the rest call
        """
        return self.send(url, 'GET', headers=headers, params=params, return_raw_response=return_raw_response,
                         retries=retries)

    def post(self, url, data, files=None, headers={}, return_raw_response=False, retries=0):
        """Sends a POST request to the given url with the given headers

        :param return_raw_response: If true do not filter response, return raw object
        :param url: url to send request to
        :param headers: headers to use in the request
        :return: response of the rest call
        :param retries: Number of times to retry the request if it results in a 400 or higher response code
        """
        return self.send(url, 'POST', data, files=files, headers=headers, return_raw_response=return_raw_response,
                         retries=retries)

    def patch(self, url, data, files=None, headers={}, return_raw_response=False, retries=0):
        """Sends a PATCH request to the given url with the given headers

        :param return_raw_response: If true do not filter response, return raw object
        :param url: url to send request to
        :param headers: headers to use in the request
        :param retries: Number of times to retry the request if it results in a 400 or higher response code
        :return: response of the rest call
        """
        return self.send(url, 'PATCH', data, files=files, headers=headers, return_raw_response=return_raw_response,
                         retries=retries)

    def put(self, url, data, headers={}, return_raw_response=False, retries=0):
        """
        Sends a PUT request to the given url with the given headers
        :param return_raw_response: If true do not filter response, return raw object
        :param url: url to send request to
        :param headers: headers to use in the request
        :param retries: Number of times to retry the request if it results in a 400 or higher response code
        :return: response of the rest call
        """
        return self.send(url, 'PUT', data, headers=headers, return_raw_response=return_raw_response,
                         retries=retries)

    def delete(self, url, headers={}, return_raw_response=False, retries=0):
        """Sends a DELETE request to the given url with the given headers

        :param return_raw_response: If true do not filter response, return raw object
        :param url: url to send request to
        :param headers: headers to use in the request
        :param retries: Number of times to retry the request if it results in a 400 or higher response code
        :return: response of the rest call
        """
        return self.send(url, 'DELETE', headers=headers, return_raw_response=return_raw_response,
                         retries=retries)

    @staticmethod
    def async_call(rest_call, pool, *args, callback=None):
        """Starts a new process asynchronously

        :param rest_call: a pointer to the rest call which should be executed async
        :param pool: python process pool to take processes from
        :param callback: function which will get called given the response of the child thread
        :return: returns a python AsyncResult object
        """
        logger.debug(f"Current pool queue size: {pool._work_queue.qsize()}")

        future = pool.submit(rest_call, *args)
        if callback is not None:
            future.add_done_callback(callback)
        return future
