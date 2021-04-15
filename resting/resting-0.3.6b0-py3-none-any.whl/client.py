import requests
from requests import exceptions as requests_ex
import socket
from json.decoder import JSONDecodeError
from collections import OrderedDict
import json
import dicttoxml
import xmltodict

from .utils import DeferredService
from . import __version__
from . import exceptions, settings


__all__ = [
    'BaseClient',
    'JsonClient',
    'default_client'
]


class BaseClient:
    """
    This class actually handle all HTTP requests and responses
    """
    _session = None
    _user_agent = None
    auth = None

    def __init__(self, api_version=None, auth=None):
        self.auth = auth
        self.api_version = api_version or 1
        self._user_agent = settings.USER_AGENT or \
            'Resting/{version}'.format(version=__version__)

    def get_default_headers(self, headers):
        """
        Adds User-Agent header

        :param dict headers:
        :return dict:
        """
        headers['User-Agent'] = self._user_agent
        return headers

    @property
    def session(self):
        if not self._session:
            self._session = requests.Session()
        return self._session


class JsonClient(BaseClient):

    def get_default_headers(self, headers):
        """
        Adds Content-Type and Accept headers

        :param headers:
        :return:
        """
        if 'Accept' not in headers:
            headers['Accept'] = 'application/json'

        return super().get_default_headers(headers)

    def _process_response(self, response):
        """

        :param response:
        :return:
        """
        try:
            data = json.loads(response.text, object_pairs_hook=OrderedDict)
        except (ValueError, TypeError, JSONDecodeError):
            raise exceptions.ApiMalformedResponseError(
                "Could not decode json", response=response)
        return response, data

    def request(self, method, url, data=None,
                params=None, files=None,
                expected_codes=None, headers=None, auth=None):
        """
        Invoke HTTP request using requests lib. Raise APIException when
        something with connection went wrong or response status code wasn't
        in expected ones

        Usage::

        try:
            response,data = client.request(
                url=http://localhost:8080/api,
                method='patch',
                data={'foo': bar}
                )
        except api_exceptions.ValidationError as e:
            print(e.errors)
        except api_exceptions.ApiException:
            print("Something went terribly wrong")

        :param str method: HTTP method
        :param str url: Url to be invoked
        :param dict data: request data
        :param dict params: request query parameters
        :param dict files: request files
        :param list expected_codes: List of status codes which are
                                    expeected in response
        :param dict headers: Additional http headers
        :param AuthBase auth: requests.auth.AuthBase instance
        :return tuple: (request.Response, response data)
        """

        auth = auth or self.auth
        if not headers:
            headers = dict()
        headers = self.get_default_headers(headers)

        if data and 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/json'

        json_data = None
        if 'Content-Type' in headers and headers['Content-Type'].startswith('application/json'):
            json_data = data
            data = None
        try:
            r = self.session.request(
                method,
                data=data,
                url=url,
                json=json_data,
                params=params,
                auth=auth,
                headers=headers,
                files=files
            )
        except (requests_ex.ConnectTimeout, requests_ex.ReadTimeout,
                requests_ex.ConnectionError, socket.timeout) as e:
            raise exceptions.ApiConnectionError(original_exception=e)
        else:
            if expected_codes and r.status_code not in expected_codes:
                exceptions.handle(r)

        if r.status_code in [204]:
            return r, None

        return self._process_response(response=r)


class XMLClient(BaseClient):

    def get_default_headers(self, headers):

        if 'Accept' not in headers:
            headers['Accept'] = 'application/xml'

        return super().get_default_headers(headers)

    def _process_response(self, response):
        """

        :param response:
        :return:
        """
        try:
            data = xmltodict.parse(response.text)
        except (ValueError, TypeError):
            raise exceptions.ApiMalformedResponseError(
                "Could not decode xml", response=response)
        return response, data

    def request(self, method, url, data=None,
                params=None, files=None,
                expected_codes=None, headers=None, auth=None):

        auth = auth or self.auth
        if not headers:
            headers = dict()

        if data:

            if isinstance(data, (dict, list)):
                data = dicttoxml.dicttoxml(data)

            if 'Content-Type' not in headers:
                headers['Content-Type'] = 'application/xml'

        try:
            r = self.session.request(
                method,
                data=data,
                url=url,
                params=params,
                auth=auth,
                headers=headers,
                files=files
            )
        except (requests_ex.ConnectTimeout, requests_ex.ReadTimeout,
                requests_ex.ConnectionError, socket.timeout) as e:
            raise exceptions.ApiConnectionError(original_exception=e)
        else:
            if expected_codes and r.status_code not in expected_codes:
                exceptions.handle(r)

        if r.status_code in [204]:
            return r, None

        return self._process_response(response=r)


class DefaultClient(DeferredService):

    def _init(self):
        self._service = settings.CLIENT_CLASS(**settings.CLIENT_KWARGS)

default_client = DefaultClient()
