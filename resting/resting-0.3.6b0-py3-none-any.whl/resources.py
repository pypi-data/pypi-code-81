from math import ceil
from requests.auth import AuthBase

from .client import default_client, BaseClient
from . import settings, exceptions

__all__ = [
    'Resource',
    'Root',
    'ListResource'
]


class Resource:
    """
    Represents Rest api resource (endpoint)
    """
    _url = None
    _loaded = False
    _child_resources = None
    _client = None
    _auth = None
    data = None
    response = None

    """
    :var Client
    """
    METHOD_GET = 'GET'
    METHOD_POST = 'POST'

    def __init__(self, url, data=None, client_class=None):

        if client_class:
            self.client = client_class

        self._url = url
        if data:
            self.data = data
            self._loaded = True

    def __getattr__(self, item):
        if self.data and item in self.data:
            return self.data[item]
        return getattr(self, item)

    def __getitem__(self, item):
        if self.data and item in self.data:
            return self.data[item]

    def items(self):
        if self.data:
            return self.data.items()
        else:
            return dict().items()

    def keys(self):
        if self.data:
            return self.data.keys()
        else:
            return dict().items()

    @property
    def client(self):
        return self._client or default_client

    @client.setter
    def client(self, client_class):

        if isinstance(client_class, BaseClient):
            self._client = client_class
            return

        if not issubclass(client_class, BaseClient):
            raise RuntimeError("Param client_class must be subclass of "
                               "client.BaseClient")
        params = settings.CLIENT_KWARGS
        if self._auth:
            params['auth'] = self._auth

        self._client = client_class(**params)

    @property
    def url(self):
        return self._url

    def resource(self, name):
        """
        Return child resource by name if exists

        :param str name: resource name
        :return Resource: requested resource instance
        """
        if not self._child_resources:
            msg = "There are not child resources in here ({})".format(self)
            raise exceptions.ResourceNotFound(msg)
        if name not in self._child_resources:
            msg = "Resource '{}' was not found. Available are: {}".format(
                name, ', '.join(self._child_resources.keys()))
            raise exceptions.ResourceNotFound(msg)
        r = self._child_resources[name]

        if not isinstance(r, Resource):
            self._child_resources[name] = Resource(url=r)
        return self._child_resources[name]

    def resources(self):
        """
        Return list of child Resources

        :return list:
        """
        return self._child_resources

    @property
    def paginator(self):
        """
        Paginator hook. override this method to use custom
        paginator class for single Repository

        :return paginators.Paginator:
        """
        return settings.PAGINATOR_CLASS()

    @property
    def hateoas_parsers(self):
        return [parser() for parser in settings.HATEOAS_PARSERS]

    def _find_child_resources(self, data=None, response=None):
        for parser in self.hateoas_parsers:
            result = parser.process(data=data, response=response)
            if result:
                return result

    def _process_response(self, response, data):
        self._child_resources = self._find_child_resources(data, response)
        if 'Location ' in response.headers:
            self._url = response.headers['Location']
        self.response = response

    def get(self, expected_codes=None, headers=None, **kwargs):
        """
        Fetch resource detail

        :param list expected_codes: expected HTTP status codes
        :param dict headers: additional HTTP headers
        :return:
        """
        expected_codes = expected_codes or [200]

        response, data = self.client.request(
            Resource.METHOD_GET,
            self._url,
            expected_codes=expected_codes,
            headers=headers,
            **kwargs
        )
        self._process_response(response, data)
        self.data = data
        return self

    def list(self, params=None, expected_codes=None, headers=None, all=False, **kwargs):
        """
        Fetch resource and expect list as result

        :param dict params: request query params
        :param list expected_codes: expected HTTP status codes
        :param dict headers: additional HTTP headers
        :return PaginatedList:
        """
        expected_codes = expected_codes or [200]
        response, data = self.client.request(
            Resource.METHOD_GET,
            self._url,
            expected_codes=expected_codes,
            params=params,
            headers=headers
        )

        self._process_response(response, data)
        list_resource = ListResource(
            url=self._url,
            data=data,
            response=response,
            all=all,
            **kwargs
        )
        return list_resource

    def create(self, data=None, expected_codes=None, headers=None, files=None, **kwargs):
        """
        Create on current resource. If api call was successful,
        new resource will be returned

        :param dict data: request data
        :param list expected_codes: expected HTTP status codes
        :param dict headers: additional HTTP headers
        :return Resource: new Resource instance
        """
        expected_codes = expected_codes or [200, 201, 202]

        response, data = self.client.request(
            self.METHOD_POST,
            self._url,
            data=data,
            expected_codes=expected_codes,
            headers=headers,
            files=files,
            **kwargs
        )

        child_resources = self._find_child_resources(data, response)
        if 'Location' in response.headers:
            url = response.headers['Location']
        else:
            if 'self' not in child_resources:
                raise RuntimeError("Link to self not found")
            url = child_resources['self']

        resource = Resource(url=url, data=data)
        resource._child_resources = child_resources
        return resource

    def update(self, data, expected_codes=None, headers=None, files=None,
               **kwargs):
        """
        Update current resource using HTTP PUT method

        :param dict data: request data
        :param list expected_codes: expected HTTP status codes
        :param headers: additional HTTP headers
        :return Resource: return itself
        """
        expected_codes = expected_codes or [200, 201]
        response, data = self.client.request(
            'PUT',
            self._url,
            data=data,
            expected_codes=expected_codes,
            headers=headers,
            files=files,
            **kwargs
        )

        self._process_response(response, data)
        self.data = data
        return self

    def patch(self, data, expected_codes=None, headers=None,
              files=None, **kwargs):
        """
        Resource partial update

        :param dict data: request data
        :param list expected_codes: expected HTTP status codes
        :param dict headers: additional HTTP headers
        :return Resource: return itself
        """
        expected_codes = expected_codes or [200]
        response, data = self.client.request(
            'PATCH',
            self._url,
            data=data,
            expected_codes=expected_codes,
            headers=headers,
            files=files,
            **kwargs
        )
        self._process_response(response, data)
        self.data = data
        return self

    def delete(self, data=None, expected_codes=None, headers=None, **kwargs):
        """
        Delete current resource

        :param dict data: request data
        :param list expected_codes: expected HTTP status codes
        :param dict headers: additional HTTP headers
        :return Resource:
        """
        expected_codes = expected_codes or [200, 204]
        response, data = self.client.request(
            'DELETE',
            self._url,
            data=data,
            expected_codes=expected_codes,
            headers=headers,
            **kwargs
        )

        if data:
            self.data = data
        return self

    def head(self, expected_codes=None, headers=None):
        """
        Fetch resource headers

        :param list expected_codes: expected HTTP status codes
        :param dict headers: additional HTTP headers
        :return dict: response headers dict
        """
        expected_codes = expected_codes or [200]
        response, _ = self.client.request(
            'HEAD',
            self._url,
            headers=headers,
            expected_codes=expected_codes
        )
        return response.headers

    def options(self, expected_codes=None, headers=None):
        """
        Fetch resource description

        :param list expected_codes: expected HTTP status codes
        :param dict headers: additional HTTP headers
        :return dict: response headers dict
        """
        expected_codes = expected_codes or None
        response, data = self.client.request(
            'OPTIONS',
            self._url,
            headers=headers,
            expected_codes=expected_codes)
        resource = Resource(url=self._url, data=data)
        resource.response = response
        return resource

    def __str__(self):
        return self._url

    def __repr__(self):
        return "<{}: {}>".format(self.__class__.__name__, self._url)


class Root(Resource):
    """
    Represent API root endpoint
    """

    api_version = None
    """
    API version to be use
    """
    client = None

    def __init__(self, url=None, **user_settings):

        if user_settings:
            settings.user_settings = user_settings

        self.client = default_client

        super().__init__(url=url)

    def authenticate(self, auth):
        """
        Pass authentication object to client

        :param requests.Auth.BaseAuth auth:
        :return:
        """
        assert isinstance(auth, AuthBase), \
            "Instance of request.auth.AuthBase expected but {} given".\
                format(type(auth))
        self._auth = auth
        self.client.auth = auth


class ListResource(Resource):
    """

    """
    total_count = None
    current_page = None
    next_page = None
    prev_page = None
    _resources = None
    page_size = None
    pages_count = None

    def __init__(self, response, data, **kwargs):
        self.infinite_loop = kwargs.pop('all', settings.LIST_ITER_ALL)
        super(ListResource, self).__init__(**kwargs)

        paginator = self.paginator.process(response, data)

        self.total_count = paginator.get('count', len(data))
        self.start = paginator.get('start', 0)
        self.end = paginator.get('end', len(data))

        if self.start and self.end:
            self.page_size = self.end = self.start

        if self.page_size and self.total_count:
            self.pages_count = int(ceil(self.total_count / self.page_size))
            self.current_page = 1
        if paginator and 'next' in paginator:
            self.next_page = Resource(url=paginator['next'])
        if paginator and 'prev' in paginator:
            self.prev_page = Resource(url=paginator['prev'])
        self._resources = []
        for row in data:
            self.append(data=row, response=response)

    def __iter__(self):
        """
        Iterate over fetched objects in list. If you have enabled INFINITE_LOOP
        setting or if passed all=True argument to list call all pages will be
        fetched.
        """
        i = self.start + 1
        for r in self._resources:
            if self.infinite_loop and i == self.end and self.total_count != i:
                self.load_more()
            i += 1
            yield r

    def __getitem__(self, index):
        """
        Get single resource (object) from current page (so far) by index.
        If not found raises IndexError

        :param int|slice index:
        :return:
        """
        if isinstance(index, int):
            if index > self.total_count:
                raise IndexError("Out of range")

            if not self.end or not self.start:
                return self._resources[index]
            elif index >= self.start and index <= self.end:
                return self._resources[index]
            elif index > self.total_count:
                msg = "Out of range. There are only {} objects in this " \
                      "resource"
                raise IndexError(msg.format(self.total_count))
        elif isinstance(index, slice):
            msg = "Slice is not supported yet"
            raise NotImplementedError(msg)
        else:
            msg = "Type {} is not supported for indexing"
            raise TypeError(msg.format(type(index)))

    def append(self, data, response):
        """
        Adds new resource to collection out of data and response

        :param dict data:
        :param Response response: requests.Response instance
        :return:
        """
        urls = self._find_child_resources(data=data, response=response)
        resource = Resource(urls.get('self'), data=data)
        resource._child_resources = urls
        self._resources.append(resource)

    def load_more(self):
        response, data = self.client.request('GET', url=self.next_page._url)
        for row in data:
            self.append(data=row, response=response)
        paginator = self.paginator.process(response, data)
        self.end = paginator.get('end')
        self.total_count = paginator.get('total_count')
        if paginator and 'next' in paginator:
            self.next_page = Resource(url=paginator['next'])
        if paginator and 'prev' in paginator:
            self.prev_page = Resource(url=paginator['prev'])

    @property
    def data(self):
        return self._resources

    def __len__(self):
        if not self._resources:
            return 0
        return len(self._resources)
