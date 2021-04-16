from typing import List

from applipy_http.path import PathFormatter
from applipy_http.endpoint import Endpoint
from applipy_http.route import Route
from applipy_http.wrapper import EndpointWrapper


class Api:

    HTTP_METHODS = ('GET', 'HEAD', 'POST', 'PUT', 'DELETE',
                    'CONNECT', 'OPTIONS', 'TRACE', 'PATCH')

    _path_formatter: PathFormatter
    _endpoints: List[Endpoint]
    _wrappers: List[EndpointWrapper]

    def __init__(self, path_formatter: PathFormatter,
                 endpoints: List[Endpoint],
                 wrappers: List[EndpointWrapper]) -> None:
        self._path_formatter = path_formatter
        self._endpoints = endpoints
        self._wrappers = wrappers

    def get_routes(self) -> List[Route]:
        routes = []

        for endpoint in self._endpoints:
            formatted_path = self._path_formatter.format(endpoint.path())
            for method in self.HTTP_METHODS:
                handler = getattr(endpoint, method.lower())
                if not getattr(handler, '_endpoint_method_disabled', False):
                    cors_config = getattr(handler,
                                          '_cors_config',
                                          endpoint.global_cors_config)

                    for wrapper in sorted(self._wrappers, key=lambda x: x.priority()):
                        handler = wrapper.wrap(method, formatted_path, handler)

                    routes.append(Route(method,
                                        formatted_path,
                                        handler,
                                        cors_config))

        return routes
