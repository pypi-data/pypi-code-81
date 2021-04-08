"""
This file contains the definition of the abstract class ElementalTypeElement, which handles elemental Python types
such as int, str, bool.
"""
from pydecidim.model.abstract_api_element import AbstractApiElement


class ElementalTypeElement(AbstractApiElement):
    """
    The abstract class AbstractApiElement define methods to parse information from the GraphQL API.
    """

    @property
    def element(self):
        return self.__element

    def __init__(self, element) -> None:
        self.__element = element

    def parse_arguments_to_gql(self) -> str:
        """
        Returns a string with the format of GraphQL arguments.
        :return: A string in GraphQL format.
        """
        return str(self.element)
