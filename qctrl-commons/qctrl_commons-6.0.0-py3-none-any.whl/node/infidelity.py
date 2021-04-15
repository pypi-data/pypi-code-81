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
"""Module for InfidelityNode."""
from typing import (
    Dict,
    List,
    Optional,
)

import forge
import numpy as np

from qctrlcommons.node.module import ModuleNode
from qctrlcommons.node.utils import validate_batch_and_values_shapes
from qctrlcommons.preconditions import (
    check_argument,
    check_sample_times,
)

from . import types
from .node_data import (
    StfNodeData,
    TargetNodeData,
    TensorNodeData,
    TensorPwcNodeData,
)


class InfidelityNode(ModuleNode):
    """Represent InfidelityNode."""

    _module_name = "qctrlcore"

    def _evaluate_node(
        self, execution_context: "ExecutionContext", args: List, kwargs: Dict
    ):
        """Handle the condition that cannot use target as kwargs in pythonflow.

        Parameters
        ----------
        execution_context : ExecutionContext
            helper class for evaluating the value of the node.
        args : List
            argument list for the node.
        kwargs : Dict
            keyword arguments for the node.

        Returns
        -------
        Any
            the value of the node.
        """
        if kwargs.get("target_operator", None):
            kwargs["target"] = kwargs.pop("target_operator")
        return super()._evaluate_node(execution_context, args, kwargs)


class InfidelityPwc(InfidelityNode):
    r"""
    Creates the total infidelity of the given piecewise-constant system.

    Use this function to compute the sum of the operational infidelity (which
    measures how effectively the system achieves a target gate) and filter
    function values (which measure how robust the system evolution is to
    various perturbative noise processes). This total infidelity value
    provides a cost that measures how effectively and robustly a set of
    controls achieves a target operation.

    Note that the total infidelity returned by this function is at least zero,
    but might be larger than one (for example if the system is highly
    sensitive to one of the noise processes).

    Parameters
    ----------
    hamiltonian : TensorPwc
        The control Hamiltonian :math:`H_{\mathrm c}(t)`. You can provide
        either a single Hamiltonian or a batch of them.
    target_operator : Target
        The object describing the target gate :math:`U_\mathrm{target}` and
        (optionally) the filter function projector :math:`P`. If you
        provide a batch of Hamiltonians, the function uses the same target
        for all the elements in the batch.
    noise_operators : List[TensorPwc], optional
        The perturbative noise operators :math:`\{N_j(t)\}`. You can omit this
        list if there are no noises. If you provide a batch of Hamiltonians
        rather than a single Hamiltonian, don't provide noise operators.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The total infidelity (operational infidelity plus filter function
        values) of the given system, with respect to the given target gate.
        If you provide a batch of Hamiltonians, the function returns a
        batch of infidelities contaning one infidelity for each Hamiltonian
        of the input batch.

    Warnings
    --------
    This function currently doesn't support noise operators when you
    provide a batch of Hamiltonians (rather than a single Hamiltonian).

    The Hessian matrix cannot currently be calculated for a graph which includes
    an `infidelity_pwc` node if the `hamiltonian` has degenerate eigenvalues at
    any segment.

    See Also
    --------
    infidelity_stf : Corresponding operation for `Stf` Hamiltonians.
    time_evolution_operators_pwc : Unitary time evolution operators for quantum systems with
        `TensorPwc` Hamiltonians.
    target : Define the target operation of the time evolution.

    Notes
    -----
    The total system Hamiltonian is

    .. math:: H_{\mathrm c}(t) + \sum_j \beta_j(t) N_j(t),

    where :math:`\{\beta_j(t)\}` are small, dimensionless, stochastic
    variables.

    The total infidelity, as represented by this node, is the sum of the
    operational infidelity :math:`\mathcal{I}` and the filter functions
    :math:`\{F_j(0)\}` of each noise operator evaluated at zero frequency.

    The operational infidelity is

    .. math::
      \mathcal{I} = 1-\left|
        \frac{\mathrm{Tr} \left(U_\mathrm{target}^\dagger U(t)\right)}
        {\mathrm{Tr} \left(U_\mathrm{target}^\dagger U_\mathrm{target}\right)}
        \right|^2,

    where :math:`U(t)` is the unitary time evolution operator due to
    :math:`H_{\mathrm c}(t)`.

    The filter function for the noise operator :math:`N_j(t)` is a measure of
    robustness, defined at frequency :math:`f` as

    .. math::
      F_j(f) = \frac{1}{\mathrm{Tr}(P)} \mathrm{Tr} \left( P
        \mathcal{F} \left\{ \tilde N_j^\prime(t) \right\} \left[ \mathcal{F}
        \left\{ \tilde N^\prime (t) \right\} \right]^\dagger P \right),

    where :math:`\mathcal{F}` is the Fourier transform,
    :math:`\tilde N_j(t) \equiv U_c^\dagger(t) N_j(t) U_c(t)` is the
    toggling-frame noise operator, and
    :math:`\tilde N_j^\prime(t)\equiv
    \tilde N_j(t)-
    \frac{\mathrm{Tr}(P\tilde N_j(t)P)}{\mathrm{Tr}(P)} \mathbb{I}`
    differs from :math:`\tilde N_j(t)` only by a multiple of the identity but
    is trace-free on the subspace of interest. The filter function value at
    zero frequency quantifies the sensitivity of the controls to quasi-static
    noise applied via the corresponding noise operator.
    """

    name = "infidelity_pwc"
    _module_attr = "create_infidelity"
    args = [
        forge.arg("hamiltonian", type=types.TensorPwc),
        forge.arg("target_operator", type=types.Target),
        forge.arg(
            "noise_operators", type=Optional[List[types.TensorPwc]], default=None
        ),
    ]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        hamiltonian = kwargs.get("hamiltonian")
        target_operator = kwargs.get("target_operator")
        noise_operators = kwargs.get("noise_operators")
        check_argument(
            isinstance(hamiltonian, TensorPwcNodeData),
            "The Hamiltonian must be a TensorPwc.",
            {"hamiltonian": hamiltonian},
        )
        check_argument(
            isinstance(target_operator, TargetNodeData),
            "The target_operator must be a Target.",
            {"target_operator": target_operator},
        )
        batch_shape, _ = validate_batch_and_values_shapes(hamiltonian, "hamiltonian")
        if noise_operators is not None:
            check_argument(
                len(noise_operators) == 0 or batch_shape == (),
                "If you provide a batch of Hamiltonians, you can't provide noise operators.",
                {"hamiltonian": hamiltonian, "noise_operators": noise_operators},
            )
            check_argument(
                all(isinstance(noise, TensorPwcNodeData) for noise in noise_operators),
                "Each of the noise_operators must be a TensorPwc.",
                {"noise_operators": noise_operators},
            )
        return TensorNodeData(_operation, shape=batch_shape)


class InfidelityStf(InfidelityNode):
    r"""
    Creates the total infidelity of a given system with a sampleable Hamiltonian.

    See :obj:`infidelity_pwc` for information about the total infidelity
    created by this function.

    Parameters
    ----------
    sample_times : np.ndarray(1D, real)
        The times at which the Hamiltonian and noise operators (if present) should be sampled for
        the integration. Must start with 0, be ordered, and contain at least one element.
    hamiltonian : Stf
        The control Hamiltonian :math:`H_{\mathrm c}(t)`. You can provide
        either a single Hamiltonian or a batch of them.
    target_operator : Target
        The object describing the target gate :math:`U_\mathrm{target}` and
        (optionally) the filter function projector :math:`P`. If you
        provide a batch of Hamiltonians, the function uses the same target
        for all the elements in the batch.
    noise_operators : List[Stf], optional
        The perturbative noise operators :math:`\{N_j(t)\}`. You can omit this
        list if there are no noises.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The infidelity of the given system with respect to the given target at the last time in
        `sample_times`.
        If you provide a batch of Hamiltonians, the function returns a batch of infidelities
        contaning one infidelity for each Hamiltonian of the input batch.

    See Also
    --------
    infidelity_pwc : Corresponding operation for `TensorPwc` Hamiltonians.
    target : Define the target operation of the time evolution.
    time_evolution_operators_stf : Unitary time evolution operators for quantum systems with
        `Stf` Hamiltonians.
    """

    name = "infidelity_stf"
    _module_attr = "create_infidelity_stf"
    args = [
        forge.arg("sample_times", type=np.ndarray),
        forge.arg("hamiltonian", type=types.Stf),
        forge.arg("target_operator", type=types.Target),
        forge.arg("noise_operators", type=Optional[List[types.Stf]], default=None),
    ]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        sample_times = kwargs.get("sample_times")
        hamiltonian = kwargs.get("hamiltonian")
        target_operator = kwargs.get("target_operator")
        noise_operators = kwargs.get("noise_operators")
        check_sample_times(sample_times, "sample_times")
        check_argument(
            sample_times[0] == 0,
            "The first of the sample times must be zero.",
            {"sample_times": sample_times},
        )
        check_argument(
            isinstance(hamiltonian, StfNodeData),
            "The Hamiltonian must be an Stf.",
            {"hamiltonian": hamiltonian},
        )
        check_argument(
            isinstance(target_operator, TargetNodeData),
            "The target_operator must be a Target.",
            {"target_operator": target_operator},
        )
        if noise_operators is not None:
            check_argument(
                all(isinstance(noise, StfNodeData) for noise in noise_operators),
                "Each of the noise_operators must be an Stf.",
                {"noise_operators": noise_operators},
            )
        batch_shape, _ = validate_batch_and_values_shapes(hamiltonian, "hamiltonian")
        return TensorNodeData(_operation, shape=batch_shape)
