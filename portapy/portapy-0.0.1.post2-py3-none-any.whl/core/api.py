"""
This module contains the basic annotations for defining portable API structures.
"""

import abc

from .types import IAnnotation
from .types import IAnnotatable


class IAPIAnnotation(IAnnotation, metaclass=abc.ABCMeta):
    """
    This interface is used to specify annotations for API specifications.
    """


class APIInfo(IAPIAnnotation):
    """
    Defines an API basic information such as title, version and description.
    """

    # Disallow multiple definitions of this type
    allow_multi = False

    def __init__(self, title: str = None, version: str = None, desc: str = None,
                 tos: str = None) -> None:
        """
        Most arguments here are self-explanatory.

        The *tos* argument is a URL pointing to the terms of service of the API, if necessary.
        """
        self.title = title
        self.version = version
        self.desc = desc
        self.tos = tos

    def apply(self, spec: dict) -> None:
        """
        Apply the annotation to the OpenAPI specification.
        """
        spec['info'] = {
            'title': self.title or '',
            'version': self.version or '',
            'description': self.desc or '',
            'termsOfService': self.tos or '',
        }


class API(IAnnotatable[IAPIAnnotation]):
    """
    Defines an API.
    """

    def get_spec(self) -> dict:
        """
        Get the complete OpenAPI definition.
        """
        while True:
            spec = {
                'swagger': '2.0',
                'info': {
                    'version': '1.0.0',
                    'title': 'Untitled API',
                },
                'definitions': {},
            }

            try:
                for items in self.items.values():
                    for item in items:
                        item.apply(spec)
            except RuntimeError:
                continue

            return spec
