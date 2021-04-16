"""
This module contains the annotation types for specifying API endpoints.
"""

import typing
import abc

from .model import Model
from .endpoint import IEndpointAnnotation


class Parameter(IEndpointAnnotation):
    """
    Defines a request parameter for an endpoint.
    """

    def __init__(self, name: str, data_type: typing.Type, where: str, *, desc: str = None,
                 required: bool = False) -> None:
        """
        The *name* argument defines the name of the parameter.
        The *data_type* argument is the type to expect from the argument. The
        *desc* argument describes the parameter.
        """
        self.name = name
        self.where = where
        self.data_type = data_type
        self.desc = desc
        self.required = required

    def __repr__(self) -> str:
        """
        Get a human readable representation of the object.
        """
        return '{}<{}:{}>'.format(self.__class__.__name__, self.name, self.data_type.__name__)

    def apply(self, spec: dict) -> None:
        """
        Apply the annotation to the OpenAPI specification.
        """
        if 'parameters' not in spec:
            spec['parameters'] = []

        # TODO enums, defaults

        param = {
            # 'default': all,
            # 'enum': [
            #     'all',
            #     'bleh',
            # ],
            'in': self.where,
            'required': self.required,
            'name': self.name or '',
        }

        param_type = Model(self.data_type, self.desc, self.name).get_spec()
        param.update(param_type)
        spec['parameters'].append(param)


class PathParameter(Parameter):
    """
    Defines a path parameter mapping for an endpoint.
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        Set the parameter as required.
        """
        kwargs['where'] = 'path'
        kwargs['required'] = True
        super().__init__(*args, **kwargs)


class QueryParameter(Parameter):
    """
    Defines the query string format for an endpoint.
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        Set the parameter as required.
        """
        kwargs['where'] = 'query'
        super().__init__(*args, **kwargs)


class HeaderParameter(Parameter):
    """
    Defines a header for an endpoint.
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        Set the parameter as required.
        """
        kwargs['where'] = 'header'
        super().__init__(*args, **kwargs)
