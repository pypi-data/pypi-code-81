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
"""
Module for OptimizationVariableNode.
"""
import warnings

import forge

from qctrlcommons.exceptions import QctrlException
from qctrlcommons.node.base import Node

from . import types
from .node_data import TensorNodeData


class OptimizationVariableNode(Node):
    """Represent the OptimizationVariableNode class."""

    _attr = None
    optimizable_variable = True

    def _evaluate_node(self, execution_context, args, kwargs):
        func = getattr(execution_context.variable_factory, self._attr, None)

        if func is None:
            raise RuntimeError(f"attr missing from variable factory: {self._attr}")

        return func(*args, **kwargs)


class OptimizationVariable(OptimizationVariableNode):
    r"""
    Creates optimization variables, which can be bounded, semi-bounded, or unbounded.

    Use this function to create a sequence of variables that can be tuned by
    the optimizer (within specified bounds) in order to minimize the cost
    function.

    Parameters
    ----------
    count : int
        The number :math:`N` of individual real-valued variables to create.
    lower_bound : float
        The lower bound :math:`v_\mathrm{min}` on the variables.
        The same lower bound applies to all `count` individual variables.
        This lower bound will also be used for generating an initial value
        for the variables.
    upper_bound : float
        The upper bound :math:`v_\mathrm{max}` on the variables.
        The same upper bound applies to all `count` individual variables.
        This upper bound will also be used for generating an initial value
        for the variables.
    is_lower_unbounded : bool, optional
        Defaults to False. Set this flag to `True` to define a semi-bounded variable with
        lower bound :math:`-\infty`; in this case, the `lower_bound` parameter is used only for
        generating an initial value.
    is_upper_unbounded : bool, optional
        Defaults to False. Set this flag to True to define a semi-bounded variable with
        upper bound :math:`+\infty`; in this case, the `upper_bound` parameter is used only for
        generating an initial value.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The sequence :math:`\{v_n\}` of :math:`N` optimization variables. If both
        `is_lower_unbounded` and `is_upper_unbounded` are `False`, these variables are
        bounded such that :math:`v_\mathrm{min}\leq v_n\leq v_\mathrm{max}`. If one of the
        flags is `True` (for example `is_lower_unbounded=True`), these variables are
        semi-bounded (for example :math:`-\infty \leq v_n \leq v_\mathrm{max}`).
        If both of them are `True`, then these variables are unbounded and satisfy that
        :math:`-\infty \leq v_n \leq +\infty`.

    See Also
    --------
    :func:`~qctrl.dynamic.namespaces.FunctionNamespace.calculate_optimization` : Find the minimum
        of a generic function.
    anchored_difference_bounded_variables : Create anchored optimization variables
        with a difference bound.
    """

    name = "optimization_variable"
    _attr = "create_optimizable_variables"
    args = [
        forge.arg("count", type=int),
        forge.arg("lower_bound", type=float),
        forge.arg("upper_bound", type=float),
        forge.arg("is_lower_unbounded", type=bool, default=False),
        forge.arg("is_upper_unbounded", type=bool, default=False),
    ]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        count = kwargs["count"]
        lower_bound = kwargs["lower_bound"]
        upper_bound = kwargs["upper_bound"]
        if count <= 0:
            raise QctrlException(f"count={count} must be positive.")
        if upper_bound <= lower_bound:
            raise QctrlException(
                f"lower_bound={lower_bound} must be less than upper_bound={upper_bound}."
            )
        return TensorNodeData(_operation, shape=(count,))


class BoundedOptimizationVariable(OptimizationVariableNode):
    r"""
    Creates bounded optimization variables.

    Use this function to create a sequence of variables that can be tuned by
    the optimizer (within specified bounds) in order to minimize the cost
    function.

    Warnings
    --------
        `bounded_optimization_variable` will be removed in the future.
        Please use `optimization_variable` instead.

    Parameters
    ----------
    count : int
        The number :math:`N` of individual real-valued variables to create.
    lower_bound : float
        The lower bound :math:`v_\mathrm{min}` on the variables.
        The same lower bound applies to all `count` individual variables.
    upper_bound : float
        The upper bound :math:`v_\mathrm{max}` on the variables.
        The same upper bound applies to all `count` individual variables.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The sequence :math:`\{v_n\}` of :math:`N` bounded optimization
        variables, satisfying
        :math:`v_\mathrm{min}\leq v_n\leq v_\mathrm{max}`.

    See Also
    --------
    :func:`~qctrl.dynamic.namespaces.FunctionNamespace.calculate_optimization` : Find the minimum
        of a generic function.
    optimization_variable : Create optimization variables.
    anchored_difference_bounded_variables : Create anchored optimization variables
        with a difference bound.
    unbounded_optimization_variable : Create unbounded optimization variables.
    """

    name = "bounded_optimization_variable"
    _attr = "create_bounded"
    args = [
        forge.arg("count", type=int),
        forge.arg("lower_bound", type=float),
        forge.arg("upper_bound", type=float),
    ]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        warnings.warn(
            "'bounded_optimization_variable' will be removed in the future. "
            "Please use 'optimization_variable' instead."
        )
        count = kwargs["count"]
        lower_bound = kwargs["lower_bound"]
        upper_bound = kwargs["upper_bound"]
        if count <= 0:
            raise QctrlException(f"count={count} must be positive.")
        if upper_bound <= lower_bound:
            raise QctrlException(
                f"lower_bound={lower_bound} must be less than upper_bound={upper_bound}."
            )
        return TensorNodeData(_operation, shape=(count,))


class UnboundedOptimizationVariable(OptimizationVariableNode):
    r"""
    Creates unbounded optimization variables.

    Use this function to create a sequence of variables that can be tuned by
    the optimizer (with no bounds) in order to minimize the cost function.

    Warnings
    --------
        `unbounded_optimization_variable` will be removed in the future.
        Please use `optimization_variable` instead.

    Parameters
    ----------
    count : int
        The number :math:`N` of individual real-valued variables to create.
    initial_lower_bound : float
        The lower bound on the interval used to initialize the variables.
        The same initial lower bound applies to all `count` individual
        variables.
    initial_upper_bound : float
        The upper bound on the interval used to initialize the variables.
        The same initial upper bound applies to all `count` individual
        variables.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The sequence :math:`\{v_n\}` of :math:`N` unbounded optimization
        variables.

    See Also
    --------
    :func:`~qctrl.dynamic.namespaces.FunctionNamespace.calculate_optimization` : Find the minimum
        of a generic function.
    optimization_variable : Create optimization variables.
    anchored_difference_bounded_variables : Create anchored optimization variables
        with a difference bound.
    bounded_optimization_variable : Create bounded optimization variables.
    """

    name = "unbounded_optimization_variable"
    _attr = "create_unbounded"
    args = [
        forge.arg("count", type=int),
        forge.arg("initial_lower_bound", type=float),
        forge.arg("initial_upper_bound", type=float),
    ]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        warnings.warn(
            "'unbounded_optimization_variable' will be removed in the future. "
            "Please use 'optimization_variable' instead."
        )
        count = kwargs["count"]
        initial_lower_bound = kwargs["initial_lower_bound"]
        initial_upper_bound = kwargs["initial_upper_bound"]
        if count <= 0:
            raise QctrlException(f"count={count} must be positive.")
        if initial_upper_bound <= initial_lower_bound:
            raise QctrlException(
                f"initial_lower_bound={initial_lower_bound} must be less than "
                f"initial_upper_bound={initial_upper_bound}."
            )
        return TensorNodeData(_operation, shape=(count,))
