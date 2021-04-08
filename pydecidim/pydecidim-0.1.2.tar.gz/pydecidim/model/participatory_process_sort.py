from pydecidim.model.abstract_api_element import AbstractApiElement


class ParticipatorySpaceSort(AbstractApiElement):
    """
    Represents a ParticipatorySpaceSort from the Decidim API.
    """

    @property
    def published_at(self):
        return self.__published_at

    @property
    def id(self):
        return self.__id

    @property
    def start_date(self):
        return self.__start_date

    def __init__(self, published_at='', process_id='', start_date='') -> None:
        self.__published_at: str = published_at
        self.__id: str = process_id
        self.__start_date: str = start_date

    def parse_arguments_to_gql(self) -> str:
        """
        Returns a string with the format of GraphQL arguments.
        :return: A string in GraphQL format.
        """

        super().parse_arguments_to_gql()
        response = ''
        if len(self.published_at) > 0:
            response += 'publishedAt: "{}", '.format(self.published_at)
        if len(self.id) > 0:
            response += 'id: "{}", '.format(self.id)
        if len(self.start_date) > 0:
            response += 'startDate: "{}", '.format(self.start_date)
        return response
