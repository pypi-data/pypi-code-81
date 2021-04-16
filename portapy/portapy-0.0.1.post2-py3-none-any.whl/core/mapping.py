"""
This module contains interfaces to define mappings.
"""

import typing
import abc
import warnings

from .api import API
from .endpoint import Endpoint
from .endpoint import IEndpointAnnotation
from .model import Model


class IMapping(IEndpointAnnotation, metaclass=abc.ABCMeta):
    """
    This abstract class can be used to define mappings, such as request
    and response mappings.
    """

    def __init__(self, struct: typing.Any, *,
                 content_type: str = None, desc: str = None) -> None:
        """
        The *struct* argument is either a datatype (e.g.: `str`, `bytes`) or
        a dictionary containing a JSON object mapping. If the datatype is
        a non-builtin type, a model definition is used to map to that object.

        The *content_type* argument is used to specify or force the content
        type. It is autodetected based on the type of *struct*, unless forced.

        The *desc* argument describes the request mapping.
        """
        self.model = None
        if struct is not None:
            self.model = Model(struct) if not isinstance(struct, Model) else struct
        self.content_type = content_type
        self.desc = desc

    def get_content_type(self) -> str:
        """
        Get the content type for the mapping.
        """
        if self.content_type:
            return self.content_type

        if not self.model:
            return None

        return self.model.get_content_type()

    def apply(self, spec: dict) -> None:
        """
        Apply the mapping to the OpenAPI specification.
        """
        if self.model and isinstance(self.owner, Endpoint) and isinstance(self.owner.owner, API):
            if isinstance(self.model.struct, (list, tuple)):
                model = self.model.struct[0]
                if model.name:
                    self.owner.owner.add(model)
            elif self.model.name:
                self.owner.owner.add(self.model)


class RequestMapping(IMapping):
    """
    Defines the request body format for an endpoint.
    """

    # Disable multiple definitions
    allow_multi = False

    # TODO: repr()

    def __init__(self, *args, required: bool = True, **kwargs) -> None:
        """
        The *required* argument can be used to denote an optional request body.
        """
        super().__init__(*args, **kwargs)
        self.required = required

    def apply(self, spec: dict) -> None:
        """
        Apply the annotation to the OpenAPI specification.
        """
        super().apply(spec)

        if 'parameters' not in spec:
            spec['parameters'] = []

        content_type = self.get_content_type()
        if content_type:
            spec['consumes'] = [self.get_content_type()]

        spec['parameters'].append({
            'in': 'body',
            'name': 'body',
            'description': self.desc or '',
            'schema': self.model.get_spec(),
            'required': self.required,
        })


class ResponseMapping(IMapping):
    """
    Defines a possible response for an endpoint.
    """

    # TODO: repr()

    def __init__(self, struct: typing.Any = None, *args,
                 status_code: int = 200, **kwargs) -> None:
        """
        The *status_code* argument describes the status code that is expected for
        that type of response mapping.
        """
        super().__init__(struct, *args, **kwargs)
        self.status_code = status_code

    def apply(self, spec: dict) -> None:
        """
        Apply the mapping to the OpenAPI specification.
        """
        super().apply(spec)

        if 'responses' not in spec:
            spec['responses'] = {}

        if 'produces' not in spec:
            spec['produces'] = []

        content_type = self.get_content_type()
        if not content_type:
            del spec['produces']
        elif content_type not in spec['produces']:
            spec['produces'].append(content_type)

        status_code = str(self.status_code)
        if status_code in spec['responses']:
            warnings.warn(UserWarning('response already defines status: %s' % status_code))

        rspec = spec['responses'][status_code] = {
            'description': self.desc or '',
        }

        if self.model is not None:
            rspec['schema'] = self.model.get_spec()


class ResponseError(ResponseMapping):
    """
    Defines a possible error for an endpoint.
    """

    def __init__(self, *args, status_code: int = 500, **kwargs) -> None:
        """
        The *status_code* argument describes the status code that is expected for
        that type of response mapping.
        """
        super().__init__(*args, status_code, **kwargs)
