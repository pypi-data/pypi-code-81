from pydecidim.model.abstract_api_element import AbstractApiElement


class ParticipatorySpaceFilter(AbstractApiElement):
    """
    Represents a ParticipatorySpaceFilter from the Decidim API.
    """

    @property
    def published_before(self):
        return self.__published_before

    @property
    def published_since(self):
        return self.__published_since

    @property
    def hashtag(self):
        return self.__hashtag

    def __init__(self, published_before='', published_since='', hashtag='') -> None:
        self.__published_before: str = published_before
        self.__published_since: str = published_since
        self.__hashtag: str = hashtag

    def parse_arguments_to_gql(self) -> str:
        """
        Returns a string with the format of GraphQL arguments.
        :return: A string in GraphQL format.
        """

        super().parse_arguments_to_gql()
        response = ''
        if len(self.published_before) > 0:
            response += 'publishedBefore: "{}", '.format(self.published_before)
        if len(self.published_since) > 0:
            response += 'publishedSince: "{}", '.format(self.published_since)
        if len(self.hashtag) > 0:
            response += 'hashtag: "{}" '.format(self.hashtag)
        return response
