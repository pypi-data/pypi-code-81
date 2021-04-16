"""
This module provides a parser to transform an OpenAPI specification into an API
and related objects.
"""

from .core import *


class APIParser():
    """
    This class is used to parse an OpenAPI specification into an API objects, containing
    endpoints, mappings, etc.
    """

    def __init__(self) -> None:
        """
        Initialize the parser.
        """
        self.api = API()

    def parse(self, spec: dict) -> API:
        """
        Parse the given spec into an API object.
        """
        if spec.get('swagger') != '2.0':
            raise SyntaxError('spec must be swagger: 2.0')

        self.api = API()

        try:
            self.add_api_info(spec)
            self.add_paths(spec)
        except Exception as ex:
            raise SyntaxError('spec parser error: %s' % ex) from ex

        return self.api

    def add_api_info(self, spec: dict) -> APIInfo:
        """
        Parse the given spec for an APIInfo object.
        """
        data = spec.get('info', {})

        item = APIInfo(
            title=data.get('title'),
            version=data.get('version'),
            desc=data.get('description'),
            tos=data.get('termsOfService'),
        )
        self.api.add(item)

        return item

    def add_paths(self, spec: dict) -> typing.List[Endpoint]:
        """
        Parse the given spec for path mappings.
        """
        data = spec.get('paths', {})
        items = []

        for path_name, conf in data.items():
            for method_name, route in conf.items():
                endpoint = Endpoint()
                endpoint.add(Method(method_name))
                endpoint.add(Path(path_name))

                self.add_endpoint_info(endpoint, route)
                self.add_params(endpoint, route)
                self.add_responses(endpoint, route)

                self.api.add(endpoint)
                items.append(endpoint)

        return items

    def add_endpoint_info(self, endpoint: Endpoint, route: dict) -> EndpointInfo:
        """
        Parse the given route spec for endpoint info and add it to the endpoint.
        """
        item = EndpointInfo(
            desc=route.get('description'),
            tags=route.get('tags'),
        )
        endpoint.add(item)

    def add_params(self, endpoint: Endpoint, route: dict) \
            -> typing.List[typing.Union[Parameter, RequestMapping]]:
        """
        Parse the given route spec for parameters and add them to the endpoint.
        """
        data = route.get('parameters', [])
        items = []

        for param in data:
            if param['in'] == 'body':
                schema = param.get('schema')
                struct = self.map_schema_to_struct(schema) if schema else None

                item = RequestMapping(
                    struct=struct,
                    required=param.get('required', True),
                    desc=param.get('description'),
                    content_type=route.get('consumes', [None])[0],
                )
                endpoint.add(item)
                items.append(item)

            else:
                item_cls = {
                    'path': PathParameter,
                    'query': QueryParameter,
                    'header': HeaderParameter,
                }.get(param['in'], Parameter)

                data_type = self.map_schema_to_struct(param)
                item = item_cls(
                    name=param['name'],
                    data_type=data_type,
                    required=param.get('required', False),
                    where=param['in'],
                    desc=param.get('description'),
                )
                endpoint.add(item)
                items.append(item)

        return items

    def add_responses(self, endpoint: Endpoint, route: dict) -> typing.List[ResponseMapping]:
        """
        Parse the given route spec for response mappings and add them to the endpoint.
        """
        data = route.get('responses', [])
        items = []

        for status_code, conf in data.items():
            status_code = int(status_code)
            cls = ResponseMapping
            if status_code >= 400:
                cls = ResponseError

            schema = conf.get('schema')
            struct = self.map_schema_to_struct(conf['schema']) if schema else None

            item = cls(
                struct=struct,
                status_code=status_code,
                desc=conf.get('description'),
                content_type=route.get('produces', [None])[0],
            )
            endpoint.add(item)
            items.append(item)

        return items

    def map_schema_to_struct(self, schema: dict, name: str = None) -> typing.Union[Property, dict]:
        """
        Map a schema object to a struct or property object.
        """
        desc = schema.get('description')
        required = schema.get('required', True)
        data_type = None

        if schema['type'] == 'string':
            data_type = str
            if schema.get('format') == 'binary':
                data_type = bytes
        if schema['type'] == 'integer':
            data_type = int
        if schema['type'] == 'number':
            data_type = float

        if data_type:
            return Property(name, data_type, desc=desc, required=required)

        if schema['type'] != 'object':
            raise TypeError('unknown type: %s' % schema['type'])

        struct = {}
        for key, conf in schema.get('properties', {}).items():
            struct[key] = self.map_schema_to_struct(conf, key)

        return struct


# TODO: review
# TODO: models?
