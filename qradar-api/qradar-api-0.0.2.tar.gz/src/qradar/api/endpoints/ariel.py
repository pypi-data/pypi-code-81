from urllib.parse import urljoin

from qradar.api.client import QRadarAPIClient
from qradar.api.client import header_vars as headers
from qradar.api.client import request_vars as params
from qradar.models import SavedSearchGroup


class Ariel(QRadarAPIClient):
    """
    The QRadar API endpoint group /ariel and its endpoints.
    """
    __baseurl = 'ariel/'

    def __init__(self, url, header, verify):
        super().__init__(urljoin(url, self.__baseurl),
                         header,
                         verify)

    @headers('Range')
    @params('filter', 'fields')
    def get_event_saved_search_groups(self, *, filter=None, fields=None, Range=None, **kwargs):
        """
        GET - /ariel/event_saved_search_groups
        Retrieves a list the event Ariel saved search groups
        """
        function_endpoint = urljoin(
            self._baseurl, 'event_saved_search_groups')
        return self._call('GET', function_endpoint, **kwargs)

    @headers('Range')
    @params('filter', 'fields')
    def get_flow_saved_search_groups(self, *, filter=None, fields=None, Range=None, **kwargs):
        """
        GET - /ariel/flow_saved_search_groups
        Retrieves a list the event Ariel saved search groups
        """
        function_endpoint = urljoin(
            self._baseurl, 'flow_saved_search_groups')
        return self._call('GET', function_endpoint, **kwargs)
