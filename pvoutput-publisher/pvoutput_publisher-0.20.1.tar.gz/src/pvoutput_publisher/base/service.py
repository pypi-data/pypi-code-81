from abc import abstractmethod, ABC

from requests import Response


class Service(ABC):

    def __init__(self):
        self._headers = {}
        self._data = {}
        self._url = None

    @property
    @abstractmethod
    def url(self):
        return self._url

    @url.setter
    def url(self, value: str):
        self._url = value

    @property
    def headers(self):
        return self._headers

    @property
    @abstractmethod
    def data(self):
        return self._data

    def set_system(self, system_id, secret_api_key):
        self._headers["X-Pvoutput-SystemId"] = system_id
        self._headers["X-Pvoutput-Apikey"] = secret_api_key


class ResponseDataHandler(ABC):
    def __init__(self):
        self._response = None

    @abstractmethod
    def handle(self, response: Response):
        _response = response

    @property
    def response(self):
        return self._response
