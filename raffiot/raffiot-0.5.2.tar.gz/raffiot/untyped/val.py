"""
Local Variables to work around Python annoying limitations about lambdas.

Python forbids local variables and
"""
from __future__ import annotations

from collections import abc
from dataclasses import dataclass


from raffiot.untyped import io, resource
from raffiot.untyped.io import IO
from raffiot.untyped.resource import Resource

__all__ = [
    "Val",
]


@dataclass
class Val:
    """
    Immutable Value.

    Used to create local "variables" in lambdas.
    """

    __slots__ = "value"

    value: None

    def get(self):
        """
        Get this Val value.
        :return:
        """
        return self.value

    def get_io(self):
        """
        Get this Val value.
        :return:
        """
        return io.defer(self.get)

    def get_rs(self):
        """
        Get this Val value.
        :return:
        """
        return resource.defer(self.get)

    @classmethod
    def pure(cls, a):
        """
        Create a new Val with value `a`

        :param a: the value of this val.
        :return:
        """
        return Val(a)

    def map(self, f):
        """
        Create a new Val from this one by applying this **pure** function.

        :param f:
        :return:
        """
        return Val(f(self.value))

    def traverse(self, f):
        """
        Create a new Val from this one by applying this `IO` function.

        :param f:
        :return:
        """

        return io.defer_io(f, self.value).map(Val)

    def flat_map(self, f):
        """
        Create a new Val from this one.

        :param f:
        :return:
        """
        return f(self.value)

    def flatten(self):  # A = Val
        """ "
        Flatten this `Val]` into a `Val`
        """

        return Val(self.value.value)

    @classmethod
    def zip(cls, *vals):
        """ "
        Group these list of Val into a Val of List
        """

        if len(vals) == 1 and isinstance(vals[0], abc.Iterable):
            return Val([x.value for x in vals[0]])
        return Val([x.value for x in vals])  # type: ignore

    def zip_with(self, *vals):
        """
        Group this Val with other Val into a list of Val.

        :param vals: other Val to combine with self.
        :return:
        """

        return Val.zip(self, *vals)

    def ap(self, *arg):
        """
        Apply the function contained in this Val to `args` Vals.

        :param arg:
        :return:
        """

        if len(arg) == 1 and isinstance(arg[0], abc.Iterable):
            l = [x.value for x in arg[0]]
        else:
            l = [x.value for x in arg]
        return Val(self.value(*l))  # type: ignore
