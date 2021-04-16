"""
This module contains the basic annotations for defining portable API structures.
"""

import typing
import abc
import warnings


# Type variable for IAnnotatable
T = typing.TypeVar('T')


class IAnnotation(metaclass=abc.ABCMeta):
    """
    This interface is used to specify generic annotations.
    """

    allow_multi = True
    """ Whether or not to allow multiple definitions of the annotation type. """

    owner: 'IAnnotation' = None
    """ The owner (parent) annotation object. """

    def __class_getitem__(cls, args: typing.Tuple) -> typing.Type['IAnnotation']:
        """
        Get the property using type hinting.
        """
        if not isinstance(args, tuple):
            args = [args]
        args = list(args)
        return type(cls.__name__, (cls,), {'__args__': tuple(args)})  # pylint:disable=no-member

    @classmethod
    def from_type_hint(cls) -> 'IAnnotation':
        """
        Create a new instance from a type hint.
        """
        return cls(*cls.__args__)  # pylint:disable=no-member


class IAnnotatable(typing.Generic[T], abc.ABC):
    """
    This abstract generic class allows can be subclassed to define annotatable
    objects.
    """

    def __init__(self, *args: T) -> None:
        """
        Set up the API using the annotations defined in *args*.
        """
        self.items = {}
        self.stack = {}
        self.add_all(args)

    def add(self, item: T) -> None:
        """
        Add an annotation.
        """
        cls = item.__class__
        T = IAnnotation

        try:
            if issubclass(item, T):
                warnings.warn(UserWarning('adding an annotation declared using subscription'))
            item = item.from_type_hint()
        except TypeError:
            pass

        if not isinstance(item, T):
            raise TypeError('unexpected %s type, expected %s' % (cls.__name__, T.__name__))

        if cls not in self.items:
            self.items[cls] = []

        if item in self.items[cls]:
            return

        if not item.allow_multi and self.items[cls]:
            warnings.warn(UserWarning('annotation type already specified: %s' % cls.__name__))
            self.items[cls] = []

        if item.owner:
            warnings.warn(UserWarning('annotation object already has an owner: %r', item))
            item.owner = self
        else:
            item.owner = self

        self.items[cls].append(item)

        for mro in cls.__mro__[1:]:
            if mro not in self.stack:
                self.stack[mro] = []

            if item not in self.stack[mro]:
                self.stack[mro].append(item)

    def add_all(self, items: typing.List[T]) -> None:
        """
        Add multiple annotations.
        """
        for item in items:
            self.add(item)

    def get(self, cls: typing.Type[T]) -> typing.Union[T, typing.List[T]]:
        """
        Get annotation(s) of a specific type.
        """
        if cls.allow_multi:
            return self.items.get(cls, []) + self.stack.get(cls, [])
        return self.items.get(cls, [None])[0]
