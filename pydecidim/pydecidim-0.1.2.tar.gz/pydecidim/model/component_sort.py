from pydecidim.model.abstract_api_element import AbstractApiElement


class ComponentSort(AbstractApiElement):

    @property
    def locale(self):
        return self.__locale

    @property
    def id(self):
        return self.__id

    @property
    def weight(self):
        return self.__weight

    @property
    def type(self):
        return self.__type

    @property
    def name(self):
        return self.__name

    def __init__(self, locale='', id='', weight='', filter_type='', name='') -> None:
        self.__locale: str = locale
        self.__id: str = id
        self.__weight: str = weight
        self.__type: str = filter_type
        self.__name: str = name

    def parse_arguments_to_gql(self) -> str:
        """
        Returns a string with the format of GraphQL arguments.
        :return: A string in GraphQL format.
        """

        super().parse_arguments_to_gql()
        response = ''
        if len(self.locale) > 0:
            response += 'locale: "{}", '.format(self.locale)
        if len(self.id) > 0:
            response += 'id: "{}", '.format(self.id)
        if len(self.weight) > 0:
            response += 'weight: "{}", '.format(self.weight)
        if len(self.type) > 0:
            response += 'type: "{}", '.format(self.type)
        if len(self.name) > 0:
            response += 'name: "{}"'.format(self.name)
        return response


