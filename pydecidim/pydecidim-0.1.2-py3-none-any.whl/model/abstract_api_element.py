"""
This file contains the definition of the abstract class AbstractApiElement. Which is the common parent of
all othe classes from the model.
"""
from abc import ABC


class AbstractApiElement(ABC):
    """
    The abstract class AbstractApiElement define methods to parse information from the GraphQL API.
    """

    def parse_arguments_to_gql(self) -> str:
        """
        Returns a string with the format of GraphQL arguments.
        :return: A string in GraphQL format.
        """
        pass
