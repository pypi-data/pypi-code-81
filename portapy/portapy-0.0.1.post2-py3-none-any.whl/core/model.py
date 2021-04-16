"""
This module contains the interfaces for defining models.
"""

import types
import typing
import inspect
import datetime
from sphinx.pycode import Parser

from portapy.utils import extract_summary_from_string

from .types import IAnnotation
from .api import IAPIAnnotation


class Model(IAPIAnnotation):
    """
    This class is used to define models on the fly.
    """

    # TODO: add this to the models OpenAPI spec

    def __init__(self, struct: typing.Any, desc: str = None, name: str = None,
                 required: bool = True) -> None:
        """
        The *struct* argument can be a type (e.g.: str, bytes), a class (e.g.: MyClass) or
        a dictionary describing the model structure.

        The *name* and *desc* arguments describe the model. If *name* is omitted and *struct*
        is a class, the name is inferred from the class name.
        """
        self.struct = {}
        self.classref = None
        self.desc = desc
        self.name = name
        self.required = required
        self.update(struct)

    # FIXME: repr()
    # TODO: optional fields

    # def __repr__(self) -> str:
    #     """
    #     Get a human readable representation of the object.
    #     """
    #     if not isinstance(self.struct, dict):
    #         return '{}<{}>'.format(
    #             self.__class__.__name__,
    #             self.struct.data_type.__name__,
    #         )

    #     return '{}{{\n  {}\n}}'.format(
    #         self.__class__.__name__,
    #         '\n  '.join([repr(x) for x in self.struct.values()]),
    #     )

    def update(self, struct: typing.Any) -> None:
        """
        Update the model's structure.
        """
        self.struct = {}

        try:
            if struct.__module__ in ['builtins', '__builtins__', 'datetime']:
                self.struct = struct
                return
        except AttributeError:
            pass

        if isinstance(struct, Model):
            self.struct = struct.struct
            self.desc = struct.desc
            self.name = struct.name
            return

        try:
            if issubclass(struct, Model):
                model = Model(struct.from_type_hint())
                self.update(model)
                return
        except TypeError:
            pass

        if hasattr(struct, '__origin__'):
            if struct.__origin__ is list or struct.__origin__ is tuple:
                struct = list(struct.__args__)
            else:
                struct = struct.__origin__

        if isinstance(struct, dict):
            items = {}

            for key, value in struct.items():
                model = value
                if not isinstance(model, Model):
                    model = self.__class__(model)

                items[key] = model

            self.struct = items

        elif isinstance(struct, (list, tuple)):
            if len(struct) != 1:
                raise TypeError('model with list spec must have exactly one item')

            model = struct[0]
            if not isinstance(model, Model):
                model = self.__class__(model)

            self.struct = [model]

        else:
            type_hints = typing.get_type_hints(struct)
            comments = {}

            try:
                # FIXME: move this to an extension
                for cls in struct.__mro__:
                    bef_comments = comments
                    source = inspect.getsource(cls)
                    parser = Parser(source)
                    parser.parse()
                    comments = {k[1]: v for k, v in parser.comments.items()}
                    comments.update(bef_comments)
            except Exception:
                pass

            data = {}
            for key, value in struct.__dict__.items():
                if key[0] == '_':
                    continue
                if value.__class__ is types.FunctionType:
                    continue
                if hasattr(value, '__mro__'):
                    continue
                if isinstance(value, property):
                    # FIXME: handle this
                    continue

                type_hint = type_hints.get(key)
                value = type_hint if type_hint else value.__class__
                desc = comments.get(key)

                model = Model(value, desc=desc)
                if not model.struct:
                    continue

                data[key] = model

            self.update(data)
            self.desc = extract_summary_from_string(struct.__doc__)
            self.name = struct.__name__
            self.classref = struct

    def get_spec(self, force: bool = False) -> dict:
        """
        Get the OpenAPI specification for this model.
        """
        spec = {
            'type': 'object',
            'properties': {},
        }

        if isinstance(self.struct, dict):
            if not force and self.name:
                return {'$ref': '#/definitions/{}'.format(self.name)}

            for key, value in self.struct.items():
                spec['properties'][key] = value.get_spec()

        elif isinstance(self.struct, (list, tuple)):
            spec = {
                'type': 'array',
                'items': self.struct[0].get_spec(),
            }

        else:
            if self.struct is str:
                spec = {'type': 'string'}
            if self.struct is bytes:
                spec = {'type': 'string', 'format': 'binary'}
            if self.struct is int:
                spec = {'type': 'integer'}
            if self.struct is float:
                spec = {'type': 'number', 'format': 'float'}
            if self.struct is bool:
                spec = {'type': 'boolean'}
            if self.struct is dict:
                spec = {'type': 'object'}
            if self.struct is list or self.struct is tuple:
                spec = {'type': 'array'}
            if self.struct is datetime.date:
                spec = {'type': 'string', 'format': 'date'}
            if self.struct is datetime.datetime:
                spec = {'type': 'string', 'format': 'date-time'}

        # TODO: enums

        if self.desc:
            spec['description'] = self.desc

        return spec

    def get_content_type(self) -> str:
        """
        Get the default content type for a type.
        """
        try:
            if issubclass(self.struct, str):
                return 'text/plain'
            if issubclass(self.struct, bytes):
                return 'application/octet-stream'
        except TypeError:
            pass

        return 'application/json'

    def apply(self, spec: dict) -> None:
        """
        Apply the annotation to the OpenAPI specification.
        """
        if self.owner:
            if isinstance(self.struct, (list, tuple)):
                model = self.struct[0]
                if model.name:
                    self.owner.add(model)
            if isinstance(self.struct, dict):
                for value in self.struct.values():
                    if isinstance(value, Model) and value.name:
                        self.owner.add(value)

        spec['definitions'][self.name] = self.get_spec(force=True)
