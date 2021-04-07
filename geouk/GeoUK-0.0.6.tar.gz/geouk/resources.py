
# NOTE: The `Place` class provides a thin wrappers to data fetched from the
# API by the API client and should not be initialized directly.


class _BaseResource:
    """
    A base resource used to wrap documents fetched from the API with dot
    notation access to attributes and methods for access to related API
    endpoints.
    """

    def __init__(self, client, document):

        # The API client used to fetch the resource
        self._client = client

        # The document representing the resource's data
        self._document = document

    def __getattr__(self, name):

        if '_document' in self.__dict__:
            return self.__dict__['_document'].get(name, None)

        raise AttributeError(
            f"'{self.__class__.__name__}' has no attribute '{name}'"
        )

    def __getitem__(self, name):
        return self.__dict__['_document'][name]

    def __contains__(self, name):
        return name in self.__dict__['_document']

    def get(self, name, default=None):
        return self.__dict__['_document'].get(name, default)


class Place(_BaseResource):
    """
    A place within the UK or Republic of Ireland.
    """

    def __str__(self):
        return f'Place: {self.humanized_name}'

    @classmethod
    def random(cls, client, lat, lon, d):
        """
        Fetch a random place within the given distance of the center
        (lat, lon).
        """

        # Fetch the random place
        r = client(
            'get',
            'places/random',
            params={
                'lat': lat,
                'lon': lon,
                'd': d
            }
        )

        if r:
            return cls(client, r)

        return None

    @classmethod
    def search(cls, client, q, exclude_ireland=False):
        """
        Fetch a list of places that match the given query string.
        """

        params = {'q': q}
        if exclude_ireland:
            params['exclude_ireland'] = True

        # Fetch the matching places
        r = client(
            'get',
            'places/search',
            params=params
        )

        return [cls(client, p) for p in r]

    @classmethod
    def typeahead(cls, client, q, exclude_ireland=False):
        """
        Return a list of place names and postcodes starting with the query
        string's first 2 characters
        """

        params = {'q': q}
        if exclude_ireland:
            params['exclude_ireland'] = True

        # Fetch the typeahead results
        r = client(
            'get',
            'places/typeahead',
            params=params
        )

        return r


class Source(_BaseResource):
    """
    A source for the data store against a place which provides attribution for
    the data.
    """

    def __str__(self):
        return f'Source: {self.name}'

    @classmethod
    def all(cls, client):
        """Fetch a list of all sources"""
        return [cls(client, s) for s in client('get', 'sources')]

    @classmethod
    def one(cls, client, ref):
        """Return a source matching the given reference"""
        return cls(client, client('get', f'sources/{ref}'))
