"""
This module contains the annotation types for specifying API endpoints.
"""

import typing
import abc
import warnings

from .types import IAnnotation
from .types import IAnnotatable
from .api import IAPIAnnotation


class IEndpointAnnotation(IAnnotation, metaclass=abc.ABCMeta):
    """
    Base class for endpoint annotations.
    """

    def __call__(self, func: typing.Callable) -> typing.Callable:
        """
        Decorator method that applies the annotation to the wrapped function.
        """
        if not isinstance(func.__annotations__.get('return'), Endpoint):
            func.__annotations__['return'] = Endpoint()
        func.__annotations__['return'].add(self)
        return func


class Path(IEndpointAnnotation):
    """
    Defines the path to an endpoint.
    """

    def __init__(self, path: str) -> None:
        """
        Initialize the endpoint path.
        """
        # FIXME: genericize (i.e.: __init__(spec), base annotation
        self.path = path

    def __repr__(self) -> str:
        """
        Get a human readable representation of the object.
        """
        return '{}<{}>'.format(self.__class__.__name__, self.path)

    def apply(self, spec: dict) -> None:
        """
        Override the parent method.
        """


class Method(IEndpointAnnotation):
    """
    Defines the method to an endpoint.
    """

    def __init__(self, method: str) -> None:
        """
        Initialize the endpoint method.
        """
        self.method = method.upper()

    def __repr__(self) -> str:
        """
        Get a human readable representation of the object.
        """
        return '{}<{}>'.format(self.__class__.__name__, self.method)

    def apply(self, spec: dict) -> None:
        """
        Override the parent method.
        """


class EndpointInfo(IEndpointAnnotation):
    """
    Defines the information (description, tags, etc.) for an endpoint.
    """

    # Disallow multiple definitions of this type
    allow_multi = False

    def __init__(self, desc: str = None, tags: typing.List[str] = None, name: str = None) -> None:
        """
        The *desc* argument is the description for the endpoint. The *tags* argument is a
        list of tags to apply to the endpoint definition.
        """
        self.desc = desc
        self.tags = tags or []
        self.name = name

    def __repr__(self) -> str:
        """
        Get a human readable representation of the object.
        """
        return '{}<{}>'.format(self.__class__.__name__, ', '.join(self.tags))

    def apply(self, spec: dict) -> None:
        """
        Apply the annotation to the OpenAPI specification.
        """
        if self.desc:
            spec['description'] = self.desc
        if self.tags:
            spec['tags'] = self.tags
        if self.name:
            spec['operationId'] = self.name
        # FIXME: summary?


class Endpoint(IAPIAnnotation, IAnnotatable[IEndpointAnnotation]):
    """
    The endpoint class encapsulates endpoint information such as parameters,
    request and response mappings and exception types.
    """

    def apply(self, spec: dict) -> None:
        """
        Apply the annotation to a specification.
        """
        paths = self.get(Path)
        methods = self.get(Method)

        for path in paths:
            if 'paths' not in spec:
                spec['paths'] = {}

            path_name = path.path
            if path_name not in spec['paths']:
                spec['paths'][path_name] = {}

            for method in methods:
                method_name = method.method.lower()
                if method_name in spec['paths'][path_name]:
                    warnings.warn(UserWarning('method %s already defined for path: %s' %
                                              (method.method, path_name)))

                espec = spec['paths'][path_name][method_name] = {
                    'responses': {},
                }

                for items in self.items.values():
                    for item in items:
                        item.apply(espec)

                if not espec['responses']:
                    espec['responses']['200'] = {'description': ''}
