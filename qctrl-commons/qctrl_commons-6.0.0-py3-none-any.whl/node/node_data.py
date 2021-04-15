"""Module for inherited wrapper class"""
from dataclasses import dataclass
from typing import Tuple

import numpy as np

# pylint:disable=cyclic-import
from qctrlcommons.node import binary
from qctrlcommons.node import unary as unary_ops
from qctrlcommons.node.attribute import GetAttributeNode
from qctrlcommons.node.wrapper import (
    NamedNodeData,
    NodeData,
)

from .attribute import GetItemNode
from .wrapper import NamedNodeData


class ArithmeticMixin:
    """
    Mixin to be used by NodeData that support binary arithmetic operations with
    number/array/Tensor/TensorPwc/Stf objects.

    By default ``arr + pf.func_op(*)`` throws an error, since NumPy doesn't know how to add
    `pf.func_op` objects to arrays. Even the fact that the func ops override `__radd__` doesn't
    help, since the NumPy addition takes precedence. We can instead tell NumPy to delegate all
    binary operations to the other operand, by explicitly clearing the `__array_ufunc__`
    attribute.
    """

    __array_ufunc__ = None

    def __add__(self, other):
        return binary.Addition.create_pf()(self, other)

    def __radd__(self, other):
        return binary.Addition.create_pf()(other, self)

    def __sub__(self, other):
        return binary.Subtraction.create_pf()(self, other)

    def __rsub__(self, other):
        return binary.Subtraction.create_pf()(other, self)

    def __matmul__(self, other):
        return binary.Matmul.create_pf()(self, other)

    def __rmatmul__(self, other):
        return binary.Matmul.create_pf()(other, self)

    def __mul__(self, other):
        return binary.Multiplication.create_pf()(self, other)

    def __rmul__(self, other):
        return binary.Multiplication.create_pf()(other, self)

    def __floordiv__(self, other):
        return binary.FloorDivision.create_pf()(self, other)

    def __rfloordiv__(self, other):
        return binary.FloorDivision.create_pf()(other, self)

    def __pow__(self, power):
        return binary.Exponentiation.create_pf()(self, power)

    def __rpow__(self, other):
        return binary.Exponentiation.create_pf()(other, self)

    def __truediv__(self, other):
        return binary.TrueDivision.create_pf()(self, other)

    def __rtruediv__(self, other):
        return binary.TrueDivision.create_pf()(other, self)

    def __abs__(self):
        return unary_ops.Absolute.create_pf()(self)

    def __neg__(self):
        return unary_ops.Negative.create_pf()(self)


@dataclass
class TensorNodeData(NamedNodeData, ArithmeticMixin):
    """
    Wrapper class for tensor type Node.
    """

    shape: Tuple[int]

    def __getitem__(self, item) -> "Operation":
        """
        refer to item in pythonflow operation.

        Returns
        -------
        Operation
            getitem operation.
        """
        node_data = GetItemNode.create_pf()(self, item)
        shape = np.empty(self.shape)[item].shape
        return TensorNodeData(node_data.operation, shape=shape)

    def __iter__(self):
        # Disable iteration for now. Even though this should work fine in theory (since all client
        # tensors have fully-defined shapes), allowing iterability on the client causes tensors to
        # pass checks that will fail in the backend (for example, if tensors are iterable on the
        # client, a multi-dimensional tensor can be passed to a function that expects a list of
        # tensors; such an input will fail in the backend though). This could be revisited in the
        # future if we're more strict about client-side validation of iterable inputs, or if we
        # update the backend to be able to iterate over tensors.
        raise TypeError(
            "You cannot iterate over Tensors directly. Instead you can iterate over the indices "
            "and extract elements of the tensor using `tensor[index]`."
        )


@dataclass
class TensorPwcNodeData(NamedNodeData, ArithmeticMixin):
    """
    Wrapper class for TensorPwc type Node.
    """

    values_shape: Tuple[int]
    durations: np.ndarray
    batch_shape: Tuple[int]

    @property
    def values(self):
        """
        Access to the values in TensorPwc.
        """
        node_data = GetAttributeNode.create_pf()(self, "values")
        shape = (
            tuple(self.batch_shape) + (len(self.durations),) + tuple(self.values_shape)
        )
        return TensorNodeData(node_data.operation, shape=shape)


@dataclass
class StfNodeData(NodeData, ArithmeticMixin):
    """
    Wrapper class for Stf type Node.
    """

    values_shape: Tuple[int]
    batch_shape: Tuple[int]


@dataclass
class SparsePwcNodeData(NodeData):
    """
    Wrapper class for SparsePwc type Node.
    """

    values_shape: Tuple[int]


@dataclass
class TargetNodeData(NamedNodeData):
    """
    Wrapper class for Target type node
    """

    values_shape: Tuple[int]
