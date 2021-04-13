import abc
from functools import reduce
from typing import Any, Callable

from storage.api import Setter, Var, E


class BaseSetter(Setter[E]):

    def __and__(self, other: Setter[E]) -> Setter[E]:
        return ReduceSetter((self, other,))

    @abc.abstractmethod
    def __call__(self, item: E) -> E:
        raise NotImplementedError()


class ReduceSetter(Setter[E]):

    def __init__(self, inner_sets=()):
        self.inner_sets = inner_sets

    def __and__(self, other: Setter[E]) -> Setter[E]:
        if isinstance(other, ReduceSetter):
            return ReduceSetter(self.inner_sets + other.inner_sets)
        return ReduceSetter(self.inner_sets + (other,))

    def __call__(self, item: E) -> E:
        return reduce(lambda a, b: b(a), self.inner_sets, item)


class FnSetter(BaseSetter[E]):

    def __init__(self, fn: Callable[[E], E]):
        self.fn = fn

    def __call__(self, item: E) -> E:
        return self.fn(item)


class Setters:

    @staticmethod
    def key(key: str, var: Var[E, Any]) -> Setter[E]:
        def set_fn(item: E) -> E:
            item[key] = var(item)
            return item

        return FnSetter(set_fn)
