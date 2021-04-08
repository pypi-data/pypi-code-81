from pydecidim.model.abstract_api_element import AbstractApiElement


class ComponentFilter(AbstractApiElement):
    """
    Represents a Component filter from the Decidim API.
    """

    @property
    def published_before(self):
        return self.__published_before

    @property
    def published_since(self):
        return self.__published_since

    @property
    def locale(self):
        return self.__locale

    @property
    def type(self):
        return self.__type

    @property
    def name(self):
        return self.__name

    @property
    def with_geolocation_enabled(self):
        return self.__with_geolocation_enabled

    @property
    def with_comments_enabled(self):
        return self.__with_comments_enabled

    def __init__(self, published_before='', published_since='', locale='', filter_type='',
                 name='', with_geolocation_enabled=False, with_comments_enabled=False) -> None:
        self.__published_before: str = published_before
        self.__published_since: str = published_since
        self.__locale: str = locale
        self.__type: str = filter_type
        self.__name: str = name
        self.__with_geolocation_enabled: bool = with_geolocation_enabled
        self.__with_comments_enabled: bool = with_comments_enabled

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
        if len(self.locale) > 0:
            response += 'locale: "{}", '.format(self.locale)
        if len(self.type) > 0:
            response += 'type: "{}", '.format(self.type)
        if len(self.name) > 0:
            response += 'name: "{}", '.format(self.name)
        if self.with_geolocation_enabled:
            response += 'withGeolocationEnabled: "{}", '.format(self.with_geolocation_enabled)
        if self.with_comments_enabled:
            response += 'withCommentsEnabled: "{}"'.format(self.with_comments_enabled)
        return response
