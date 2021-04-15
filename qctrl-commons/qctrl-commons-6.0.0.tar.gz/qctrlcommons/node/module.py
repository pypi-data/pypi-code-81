# Copyright 2020 Q-CTRL Pty Ltd & Q-CTRL Inc. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#     https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.
"""Module for ModuleNode."""
from types import ModuleType
from typing import (
    Any,
    Callable,
    Dict,
    List,
)

from qctrlcommons.node.base import Node


class ModuleNode(Node):
    """A Node that is implemented by a python module."""

    _module_name = None
    _module_attr = None

    def _get_module(self, execution_context: "ExecutionContext") -> ModuleType:
        module = getattr(execution_context, self._module_name, None)

        if module is None:
            raise RuntimeError(
                f"module missing from execution_context: {self._module_name}"
            )

        return module

    def _evaluate_node(
        self, execution_context: "ExecutionContext", args: List, kwargs: Dict
    ) -> Any:
        """
        Evaluate the node by executing its callable module attribute.

        Parameters
        ----------
        execution_context : ExecutionContext
            Helper class for evaluating the value of the node.
        args : List
            Argument list for the node.
        kwargs : Dict
            Keyword arguments for the node.

        Returns
        -------
        Any
            The value of the node.
        """
        value: callable = self._get_attr_from_module(
            execution_context, self._module_attr
        )
        return value(*args, **kwargs)

    def _get_attr_from_module(
        self, execution_context: "ExecutionContext", attr_path: str
    ) -> Callable:
        """
        Get attribute from the execution context.

        Parameters
        ----------
        execution_context : ExecutionContext
            Helper class for evaluating the value of node.
        attr_path: str
            The dotted path within our module. (e.g. "calculate_mean", "ions.ms_phases")

        Returns
        -------
        Callable
            Function, method, or class in our module.

        Raises
        ------
        RuntimeError
            When the object cannot be found in our module.
            When the object is not callable.
        """
        return get_attr_from_module(self._get_module(execution_context), attr_path)


def get_attr_from_module(module: ModuleType, attr_path: str) -> Callable:
    """
    Get attribute from the execution context.

    Parameters
    ----------
    module: ModuleType
        The module containing the callable. (e.g. qctrlcore)
    attr_path: str
        The dotted path within the module. (e.g. "calculate_mean", "ions.ms_phases")

    Returns
    -------
    Callable
        Function, method, or class in the module.

    Raises
    ------
    RuntimeError
        When the object cannot be found in the module.
    ValueError
        When the object is not callable.
    """
    value = module
    for name in attr_path.split("."):
        value = getattr(value, name, None)
        if value is None:
            raise RuntimeError(f"attr missing from module: {attr_path}")

    if not callable(value):
        raise ValueError(f"Want {attr_path} to be callable. Got {value!r}")

    return value


class CoreNode(ModuleNode):
    """Abstract class to represent the module is qctrlcore."""

    _module_name = "qctrlcore"


class TensorFlowNode(ModuleNode):
    """Represents TensorFlowNode class."""

    _module_name = "tensorflow"
