from typing import List
from urllib.parse import urljoin

from qradar.api.client import QRadarAPIClient
from qradar.api.client import header_vars as headers
from qradar.api.client import request_vars as params
from qradar.models import Logsource, LogsourceGroup, Domain, EventCollector, CustomProperty


class Config(QRadarAPIClient):
    """
    The QRadar API endpoint group /config and its endpoints.
    """
    __baseurl = 'config/'

    def __init__(self, url: str, header, verify: bool):
        super().__init__(urljoin(url, self.__baseurl),
                         header,
                         verify)

    @headers('Range')
    @params('filter', 'fields')
    def get_log_source_groups(self, *, filter: str = None, fields: str = None, Range: str = None, **kwargs) -> List[LogsourceGroup]:
        """
        GET - /config/event_sources/log_source_management/log_source_groups
        Retrieve a list of all log source groups
        """
        function_endpoint = urljoin(
            self._baseurl, 'event_sources/log_source_management/log_source_groups')
        return LogsourceGroup.from_json(self._call('GET', function_endpoint, **kwargs))

    @headers('Range')
    @params('filter', 'fields', 'sort')
    def get_log_sources(self, *, filter: str = None, fields: str = None, Range: str = None, **kwargs) -> List[Logsource]:
        """
        GET - /config/event_sources/log_source_management/log_sources
        Retrieves a list of log sources
        """
        function_endpoint = urljoin(
            self._baseurl, 'event_sources/log_source_management/log_sources')
        return Logsource.from_json(self._call('GET', function_endpoint, **kwargs))

    def update_log_sources(self, log_sources: List[Logsource], **kwargs) -> List[Logsource]:
        function_endpoint = urljoin(
            self._baseurl, 'event_sources/log_source_management/log_sources')
        return Logsource.from_json(self._call('PATCH', function_endpoint, **kwargs))

    @headers('Range')
    @params('filter', 'fields', 'sort')
    def get_domains(self, *, filter: str = None, fields: str = None, Range: str = None, **kwargs) -> List[Domain]:
        """
        GET - /config/domain_management/domains
        Gets the list of domains. You must have the System Administrator or Security Administrator permissions to call this endpoint if you are trying to retrieve the details of all domains.
        You can retrieve details of domains that are assigned to your Security Profile without having the System Administrator or Security Administrator permissions.
        If you do not have the System Administrator or Security Administrator permissions, then for each domain assigned to your security profile you can only view the values for the id and name fields. All other values return null.
        """
        function_endpoint = urljoin(
            self._baseurl, 'domain_management/domains')
        return Domain.from_json(self._call('GET', function_endpoint, **kwargs))

    @headers('Range')
    @params('filter', 'fields', 'sort')
    def get_event_collectors(self, *, filter: str = None, fields: str = None, Range: str = None, **kwargs) -> List[EventCollector]:
        function_endpoint = urljoin(
            self._baseurl, 'event_sources/event_collectors')
        return EventCollector.from_json(self._call('GET', function_endpoint, **kwargs))

    @headers('Range')
    @params('filter', 'fields', 'sort')
    def get_custom_properties(self, *, filter: str = None, fields: str = None, Range: str = None, **kwargs) -> List[CustomProperty]:
        function_endpoint = urljoin(
            self._baseurl, 'event_sources/custom_properties/regex_properties')
        return CustomProperty.from_json(self._call('GET', function_endpoint, **kwargs))
