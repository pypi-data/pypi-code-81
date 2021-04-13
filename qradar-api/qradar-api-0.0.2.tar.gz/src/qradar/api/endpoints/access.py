from typing import List
from urllib.parse import urljoin

from qradar.api.client import QRadarAPIClient
from qradar.api.client import header_vars as headers
from qradar.api.client import request_vars as params
from qradar.models import LoginAttempt


class Access(QRadarAPIClient):
    """
    The QRadar API endpoint group /access and its endpoints.
    """
    __baseurl = 'access/'

    def __init__(self, url, header, verify):
        super().__init__(urljoin(url, self.__baseurl),
                         header,
                         verify)

    @headers('Range')
    @params('filter', 'fields')
    def get_login_attempts(self, *, filter=None, fields=None, Range=None, **kwargs) -> List[LoginAttempt]:
        """
        GET - /access/login_attempts
        Gets the list of login attempts
        """
        function_endpoint = urljoin(
            self._baseurl, 'login_attempts')
        return LoginAttempt.from_json(self._call('GET', function_endpoint, **kwargs))
