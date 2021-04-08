from abc import ABC
from typing import Dict

from pydecidim.api.decidim_connector import DecidimConnector
from pydecidim.model.abstract_api_element import AbstractApiElement


class AbstractDecidimReader(ABC):

    @property
    def decidim_connector(self):
        return self.__decidim_connector

    @decidim_connector.setter
    def decidim_connector(self, decidim_connector: DecidimConnector):
        self.__decidim_connector = decidim_connector

    def __init__(self, decidim_connector: DecidimConnector, query_schema: str):
        self.__query_path = query_schema
        self.decidim_connector = decidim_connector

    def process_query_from_file(self, arguments: Dict[str, AbstractApiElement] = {}):
        return self.decidim_connector.execute_query_from_file(self.__query_path, arguments)

    def process_query(self, query: str, arguments: Dict[str, AbstractApiElement] = {}):
        return self.decidim_connector.execute_query(query)

    def execute(self, *args, **kwargs):
        pass
