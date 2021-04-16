from collections import Hashable, Mapping, Sequence
from typing import Generic, TYPE_CHECKING, TypeVar


if TYPE_CHECKING:

    from typing import Any, Callable, Union


T = TypeVar("T")


def watch(target: "T", callback: "Callable[[], None]") -> "Union[T, Watch[T]]":
    if isinstance(target, Hashable):
        # Immutable values don't need to be watched for changes.
        return target
    elif isinstance(target, Mapping):
        return DictWatch(target, callback)
    elif isinstance(target, Sequence):
        return ListWatch(target, callback)
    else:
        return Watch(target, callback)


def unwatch(target: "Union[T, Watch[T]]") -> "T":
    if isinstance(target, Watch):
        return target._Watch__target
    else:
        return target


class Watch(Generic[T]):

    __slots__ = ("__target", "__callback")

    def __init__(self, target: "T", callback: "Callable[[], None]"):
        self.__target = target
        self.__callback = callback

    def __repr__(self):
        return "<{}: {!r}>".format(self.__class__.__name__, self.__target)

    def __getattr__(self, name):
        value = getattr(self.__target, name)
        if not name.startswith("__"):
            value = watch(value, self.__callback)
        return value

    def __setattr__(self, name, value):
        if name in ("_Watch__target", "_Watch__callback"):
            super().__setattr__(name, value)
        else:
            setattr(self.__target, name, unwatch(value))
            self.__callback()

    def __delattr__(self, name):
        if name in ("_Watch__target", "_Watch__callback"):
            super().__delattr__(name)
        else:
            delattr(self.__target, name)
            self.__callback()

    def __getitem__(self, name):
        return watch(self.__target[name], self.__callback)

    def __setitem__(self, name, value):
        self.__target[name] = unwatch(value)
        self.__callback()

    def __delitem__(self, name):
        del self.__target[name]
        self.__callback()


class ListWatch(Watch):

    def insert(self, index, value):
        self.__target.insert(index, value)
        self.__callback()

    def append(self, value):
        self.__target.append(value)
        self.__callback()

    def extend(self, other):
        self.__target.extend(other)
        self.__callback()


class DictWatch(Watch):

    def update(self, other=None, **kwargs):
        self.__target.update(other or (), **kwargs)
        self.__callback()
