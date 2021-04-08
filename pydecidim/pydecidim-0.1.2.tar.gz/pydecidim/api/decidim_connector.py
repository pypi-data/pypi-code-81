"""
This file contains the definition of class DecidimConnector, which is responsible of reading from
the Decidim API.
"""
from pathlib import Path
from typing import Dict

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from graphql import DocumentNode

from pydecidim.model.abstract_api_element import AbstractApiElement


class DecidimConnector:
    """
    This class provides functionality to connect a Decidim API endpoint and execute queries.
    """

    def __init__(self, decidim_api_url: str):
        """
        Constructor, this class connects to the Decidim API endpoint.

        :param decidim_api_url: The url of the API endpoint.
        """
        transport = AIOHTTPTransport(url=decidim_api_url, timeout=60)
        self.__client = Client(transport=transport, fetch_schema_from_transport=True, execute_timeout=60)

    def execute_query(self, query: str) -> dict:
        """
        This method execute a query and returns a dictionary with the response.
        :param query: The query to be executed.
        :return: A dictionary with the response given by the API.
        """
        query: DocumentNode = gql(query)
        return self.__client.execute(query)

    def execute_query_from_file(self, query_path: str, arguments: Dict[str, AbstractApiElement] = {}) -> dict:
        """
        This method executes a query from a file. And returns the response.

        This method removes all parameters tags symbols ({}) inside the schema file.

        :param query_path: The path to the file which contains the query.
        :param arguments: A dictionary of AbstractApiElement
        :return: A dictionary with the response given by the API.
        """

        file_content: str = Path(query_path).read_text()
        for argument, parameters in arguments.items():
            file_content = file_content.replace("%" + argument.upper() + "%", parameters.parse_arguments_to_gql())
        return self.execute_query(file_content)
