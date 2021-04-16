"""
This module contains the interfaces used to integrate portable APIs within
Flask web applications.
"""

import typing
import inspect
import re
import base64
import flask

from .core import API
from .core import IEndpointAnnotation
from .core import Endpoint
from .core import EndpointInfo
from .core import Path
from .core import Parameter
from .core import PathParameter
from .core import Method
from .core import Model
from .utils import extract_summary_from_string


class Response(flask.Response):
    """
    Flask response wrapper object, used for autocompletion.
    """

    def __class_getitem__(cls, args: typing.List[IEndpointAnnotation]) -> Endpoint:
        """
        Annotate a Flask endpoint using its return value annotation.
        """
        args = args if isinstance(args, tuple) else [args]
        args = list(args)
        return Endpoint(*args)


class APIBuilder():
    """
    This class is used to generate API and related objects from Flask application
    objects.
    """

    def build_endpoints(self, app: flask.Flask) -> typing.List[Endpoint]:
        """
        Generate a list of endpoints based on Flask views annotations.
        """
        result = []

        for rule in app.url_map.iter_rules():
            func = app.view_functions[rule.endpoint]

            endpoint = func.__annotations__.get('return', Endpoint())
            if not isinstance(endpoint, Endpoint):
                endpoint = Endpoint()
            result.append(endpoint)

            url = re.sub(r'<([^>]+)>', r'{\1}', rule.rule)

            try:
                flask_type = re.match(r'{([^:]+):[^}]+}', url).groups()[0]
            except AttributeError:
                flask_type = 'string'

            default_type = str
            if flask_type == 'int':
                default_type = int
            if flask_type == 'float':
                default_type = float

            url = re.sub(r'{[^:]+:([^}]+)}', r'{\1}', url)

            endpoint.add(Path(url))

            for method in rule.methods:
                if method in ['HEAD', 'OPTIONS']:
                    continue
                endpoint.add(Method(method.upper()))

            for arg in inspect.signature(func).parameters.keys():
                if arg not in func.__annotations__:
                    endpoint.add(PathParameter(arg, default_type))

            for arg, hint in func.__annotations__.items():
                if arg == 'return':
                    continue
                if isinstance(hint, Parameter):
                    hint.name = arg
                    endpoint.add(hint)
                else:
                    endpoint.add(PathParameter(arg, hint))

            info = endpoint.get(EndpointInfo) or EndpointInfo()
            if not info.desc:
                info.desc = extract_summary_from_string(func.__doc__)
            if not info.name:
                info.name = '{}.{}'.format(func.__module__, func.__name__)
            if not info.tags:
                parts = rule.endpoint.split('.')
                if len(parts) > 1:
                    info.tags = parts[:-1]
            endpoint.add(info)

        return result

    def build(self, app: flask.Flask) -> API:
        """
        Generate an API object from a Flask application object.
        """
        endpoints = self.build_endpoints(app)
        api = API(*endpoints)
        return api


T = typing.TypeVar('T')


def parse_request(T: typing.Type[T]) -> T:
    """
    Parse a flask request.
    """
    base_model = Model(T)

    def create_object_model(data, data_type):
        """ Create an object model recursively. """
        # FIXME: move to model class
        model = Model(data_type)
        result = data_type.__new__(data_type)

        for key, value in data.items():
            if key not in model.struct:
                raise KeyError('extra key supplied in request: %s.%s' % (model.name, key))

            model_key = model.struct[key]
            if isinstance(model_key.struct, dict):
                value = create_object_model(value, model_key.classref)

            if model.struct is bytes:
                value = base64.b64decode(value)

            result.__dict__[key] = value

        return result

    # FIXME: also www-urlencoded
    # FIXME: binary types, etc.
    # TODO: validation

    if base_model.get_content_type() == 'application/json':
        input_data = flask.request.json

    if isinstance(input_data, list):
        # TODO: validate origin/args
        return [create_object_model(x, T.__args__[0]) for x in input_data]

    if isinstance(input_data, dict):
        return create_object_model(input_data, T)


# TODO: responses
