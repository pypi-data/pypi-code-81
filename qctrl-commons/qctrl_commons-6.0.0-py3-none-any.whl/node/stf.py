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
"""Module for all the node related to stf."""
from typing import (
    Callable,
    List,
    Optional,
    Union,
)

import forge
import numpy as np

from qctrlcommons.node import types
from qctrlcommons.node.module import CoreNode
from qctrlcommons.node.node_data import (
    StfNodeData,
    TensorNodeData,
    TensorPwcNodeData,
)
from qctrlcommons.node.utils import (
    validate_batch_and_values_shapes,
    validate_hamiltonian,
    validate_shape,
)
from qctrlcommons.preconditions import (
    check_argument,
    check_argument_integer,
    check_argument_iteratable,
    check_operator,
    check_sample_times,
)


class StfOperator(CoreNode):
    """
    Creates a constant operator multiplied by a sampleable signal.

    Parameters
    ----------
    signal : Stf
        A sampleable function representing the signal :math:`a(t)`
        or a batch of sampleable functions.
    operator : np.ndarray or Tensor
        The operator :math:`A`. It must have two equal dimensions.

    Returns
    -------
    Stf
        The sampleable operator :math:`a(t)A` (or batch of sampleable operators, if
        you provide a batch of signals).

    See Also
    --------
    constant_stf_operator : Create a constant `Stf` operator.
    pwc_operator : Corresponding operation for `TensorPwc`s.
    stf_sum : Sum multiple `Stf`s.
    """

    name = "stf_operator"
    _module_attr = "create_stf_operator"
    args = [
        forge.arg("signal", type=types.Stf),
        forge.arg("operator", type=Union[np.ndarray, types.Tensor]),
    ]
    kwargs = {}  # Stfs don't accept name as an argument.
    rtype = types.Stf

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        signal = kwargs.get("signal")
        operator = kwargs.get("operator")
        check_argument(
            isinstance(signal, StfNodeData),
            "The signal must be an Stf.",
            {"signal": signal},
        )
        batch_shape, _ = validate_batch_and_values_shapes(signal, "signal")
        values_shape = validate_shape(operator, "operator")
        check_operator(operator, "operator")
        check_argument(
            len(values_shape) == 2,
            "The operator must be a matrix, not a batch.",
            {"operator": operator},
            extras={"operator.shape": values_shape},
        )
        return StfNodeData(
            _operation,
            values_shape=values_shape,
            batch_shape=batch_shape,
        )


class ConstantStfOperator(CoreNode):
    r"""
    Creates a constant operator.

    Parameters
    ----------
    operator : np.ndarray or Tensor
        The operator :math:`A`, or a batch of operators. It must have at
        least two dimensions, and its last two dimensions must be equal.

    Returns
    -------
    Stf(3D)
        The operator :math:`t\mapsto A` (or batch of
        operators, if you provide a batch of operators).

    See Also
    --------
    constant_pwc_operator : Corresponding operation for `TensorPwc`s.
    stf_operator : Create an `Stf` operator.
    """

    name = "constant_stf_operator"
    _module_attr = "create_constant_stf_operator"
    args = [forge.arg("operator", type=Union[np.ndarray, types.Tensor])]
    kwargs = {}  # Stfs don't accept name as an argument.
    rtype = types.Stf

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        operator = kwargs.get("operator")
        shape = validate_shape(operator, "operator")
        check_operator(operator, "operator")
        return StfNodeData(
            _operation,
            values_shape=shape[-2:],
            batch_shape=shape[:-2],
        )


class StfSum(CoreNode):
    r"""
    Creates the sum of multiple sampleable functions.

    Parameters
    ----------
    terms : list[Stf]
        The individual sampleable function :math:`\{v_j(t)\}` to sum.

    Returns
    -------
    Stf
        The sampleable function of time :math:`\sum_j v_j(t)`. It has the same
        shape as each of the `terms` that you provide.

    See Also
    --------
    pwc_sum : Corresponding operation for `TensorPwc`s.
    stf_operator : Create an `Stf` operator.
    stf_sum : Sum multiple `Stf`s.
    """

    name = "stf_sum"
    _module_attr = "get_stf_sum"
    args = [forge.arg("terms", type=List[types.Stf])]
    kwargs = {}  # Stfs don't accept name as an argument.
    rtype = types.Stf

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        terms = kwargs.get("terms")
        check_argument_iteratable(terms, "terms")
        check_argument(
            all(isinstance(term, StfNodeData) for term in terms),
            "Each of the terms must be an Stf.",
            {"terms": terms},
        )
        batch_shape, values_shape = validate_batch_and_values_shapes(
            terms[0],
            "terms[0]",
        )
        check_argument(
            all(
                (
                    (values_shape == term.values_shape)
                    and (batch_shape == term.batch_shape)
                )
                for term in terms[1:]
            ),
            "All the terms must have the same shape.",
            {"terms": terms},
        )
        return StfNodeData(
            _operation,
            values_shape=values_shape,
            batch_shape=batch_shape,
        )


class DiscretizeStf(CoreNode):
    r"""
    Creates a piecewise-constant function by discretizing a sampleable function.

    Use this function to create a piecewise-constant approximation to a sampleable
    function (obtained, for example, by filtering an initial
    piecewise-constant function).

    Parameters
    ----------
    stf : Stf
        The sampleable function :math:`v(t)` to discretize. The values of the
        function can have any shape. You can also provide a batch of
        functions, in which case the discretization is applied to each
        element of the batch.
    duration : float
        The duration :math:`\tau` over which discretization should be
        performed. The resulting piecewise-constant function has this
        duration.
    segments_count : int
        The number of segments :math:`N` in the resulting piecewise-constant
        function.
    samples_per_segment : int, optional
        The number of samples :math:`M` of the sampleable function to take when
        calculating the value of each segment in the discretization. Defaults
        to 1.
    name : str, optional
        The name of the node.

    Returns
    -------
    TensorPwc
        The piecewise-constant function :math:`w(t)` obtained by discretizing
        the sampleable function (or batch of piecewise-constant functions, if
        you provided a batch of sampleable functions).

    Notes
    -----
    The resulting function :math:`w(t)` is piecewise-constant with :math:`N`
    segments, meaning it has segment values :math:`\{w_n\}` such that
    :math:`w(t)=w_n` for :math:`t_{n-1}\leq t\leq t_n`, where :math:`t_n= n \tau/N`.

    Each segment value :math:`w_n` is the average of samples of :math:`v(t)`
    at the midpoints of :math:`M` equally sized subsegments between
    :math:`t_{n-1}` and :math:`t_n`:

    .. math::
        w_n = \frac{1}{M}
        \sum_{m=1}^M v\left(t_{n-1} + \left(m-\tfrac{1}{2}\right) \frac{\tau}{MN} \right).

    See Also
    --------
    convolve_pwc : Create an `Stf` by convolving a `TensorPwc` with a kernel.
    identity_stf : Create an `Stf` representing the identity function.
    sample_stf : Sample an `Stf` at given times.
    """

    name = "discretize_stf"
    _module_attr = "discretize_stf"
    args = [
        forge.arg("stf", type=types.Stf),
        forge.arg("duration", type=float),
        forge.arg("segments_count", type=int),
        forge.arg("samples_per_segment", type=int, default=1),
    ]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        stf = kwargs.get("stf")
        duration = kwargs.get("duration")
        segments_count = kwargs.get("segments_count")
        batch_shape, values_shape = validate_batch_and_values_shapes(
            stf,
            "stf",
        )
        check_argument_integer(segments_count, "segments_count")
        check_argument(
            segments_count > 0,
            "The segments count must be greater than zero.",
            {"segments_count": segments_count},
        )
        durations = duration / segments_count * np.ones(segments_count)
        return TensorPwcNodeData(
            _operation,
            values_shape=values_shape,
            durations=durations,
            batch_shape=batch_shape,
        )


class TimeEvolutionOperatorsStf(CoreNode):
    """
    Calculates the time-evolution operators for a system defined by an STF Hamiltonian by using a
    4th order Runge–Kutta method.

    Parameters
    ----------
    hamiltonian : Stf
        The control Hamiltonian, or batch of control Hamiltonians.
    sample_times : np.ndarray(1D, real)
        The N times at which you want to sample the unitaries. Must be ordered and contain
        at least one element. If you don't provide `evolution_times`, `sample_times` must
        start with 0.
    evolution_times : np.ndarray(1D, real), optional
        The times at which the Hamiltonian should be sampled for the Runge–Kutta integration.
        If you provide it, must start with 0 and be ordered.
        If you don't provide it, the `sample_times` are used for the integration.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        Tensor of shape [..., N, D, D], representing the unitary time evolution.
        The n-th element (along the -3 dimension) represents the unitary (or batch of unitaries)
        from t = 0 to ``sample_times[n]``.

    See Also
    --------
    time_evolution_operators_pwc : Corresponding operation for `TensorPwc` Hamiltonians.
    """

    name = "time_evolution_operators_stf"
    _module_attr = "create_unitaries_from_stf_hamiltonian"
    args = [
        forge.arg("hamiltonian", type=types.Stf),
        forge.arg("sample_times", type=np.ndarray),
        forge.arg("evolution_times", type=Optional[np.ndarray], default=None),
    ]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        hamiltonian = kwargs.get("hamiltonian")
        sample_times = kwargs.get("sample_times")
        evolution_times = kwargs.get("evolution_times")
        check_argument(
            isinstance(hamiltonian, StfNodeData),
            "The Hamiltonian must be an Stf.",
            {"hamiltonian": hamiltonian},
        )
        batch_shape, values_shape = validate_batch_and_values_shapes(
            hamiltonian,
            "hamiltonian",
        )
        check_sample_times(sample_times, "sample_times")
        validate_hamiltonian(hamiltonian, "hamiltonian")
        time_count = len(sample_times)
        if evolution_times is not None:
            check_sample_times(evolution_times, "evolution_times")
            check_argument(
                evolution_times[0] == 0,
                "The first of the evolution times must be zero.",
                {"evolution_times": evolution_times},
            )
        else:
            check_argument(
                sample_times[0] == 0,
                "If you don't provide evolution times, the first of the sample"
                " times must be zero.",
                {"sample_times": sample_times},
            )
        shape = batch_shape + (time_count,) + values_shape
        return TensorNodeData(_operation, shape=shape)


class ConvolvePwc(CoreNode):
    r"""
    Creates the convolution of a piecewise-constant function with a kernel.

    Parameters
    ----------
    pwc : TensorPwc
        The piecewise-constant function :math:`\alpha(t)` to convolve. You
        can provide a batch of functions, in which case the convolution is
        applied to each element of the batch.
    kernel_integral : Function
        The node representing the function that computes the integral of the
        kernel :math:`K(t)`.

    Returns
    -------
    Stf
        The sampleable function representing the signal :math:`(\alpha * K)(t)`
        (or batch of signals, if you provide a batch of functions).

    Notes
    -----
    The convolution is

    .. math::
        (\alpha * K)(t) \equiv
        \int_{-\infty}^\infty \alpha(\tau) K(t-\tau) d\tau.

    Convolution in the time domain is equivalent to multiplication in the
    frequency domain, so this function can be viewed as applying a linear
    time-invariant filter (specified via its time domain kernel :math:`K(t)`)
    to :math:`\alpha(t)`.

    See Also
    --------
    discretize_stf : Discretize an `Stf` into a `TensorPwc`.
    gaussian_integral_function : Create a function that computes the integral of a normalized
        Gaussian.
    sample_stf : Sample an `Stf` at given times.
    sinc_integral_function : Create a function that computes the integral of the sinc function.
    tensor_pwc : Create piecewise-constant functions.
    """

    name = "convolve_pwc"
    _module_attr = "convolve_pwc"
    args = [
        forge.arg("pwc", type=types.TensorPwc),
        forge.arg("kernel_integral", type=Callable),
    ]
    kwargs = {}  # Stfs don't accept name as an argument.
    rtype = types.Stf

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        pwc = kwargs.get("pwc")
        batch_shape, values_shape = validate_batch_and_values_shapes(pwc, "pwc")
        return StfNodeData(
            _operation,
            values_shape=values_shape,
            batch_shape=batch_shape,
        )


class SincIntegralFunction(CoreNode):
    r"""
    Creates a function that computes the integral of the sinc function.

    Use this function to create a filter kernel that eliminates frequencies
    that are above a certain cut-off.

    Parameters
    ----------
    cut_off_frequency : float or Tensor
        Upper limit :math:`\omega_c` of the range of frequencies that you want
        to preserve. The filter eliminates components of the signal that have
        higher frequencies.

    Returns
    -------
    Function
        A node representing a function that computes the integral of the sinc
        function.

    Notes
    -----
    The range of frequencies that this kernel lets pass is
    :math:`[-\omega_c, \omega_c]`. After a Fourier transform to convert from
    frequency domain to time domain, this becomes:

    .. math::
        \frac{1}{2\pi} \int_{-\omega_c}^{\omega_c} \mathrm{d}\omega
        e^{i \omega t} = \frac{\sin(\omega_c t)}{\pi t}.

    The function on the right side of the equation is the sinc function.
    Its integral is the sine integral function (Si).
    """

    name = "sinc_integral_function"
    _module_attr = "create_sinc_integral_function"
    args = [
        forge.arg("cut_off_frequency", type=Union[float, types.Tensor]),
    ]
    kwargs = {}  # Functions don't accept name as an argument.
    rtype = types.Function


class GaussianIntegralFunction(CoreNode):
    r"""
    Creates a function that computes the integral of a normalized Gaussian.

    Use this function to create a filter kernel that has a Gaussian shape. A
    Gaussian kernel lets pass frequencies in the range roughly determined
    by its width, and progressively suppresses components outside that
    range.

    Parameters
    ----------
    std : float or Tensor
        Standard deviation :math:`\sigma` of the Gaussian in the time domain.
        The standard deviation in the frequency domain is its inverse, so that
        a high value of this parameter lets fewer frequencies pass.
    offset : float or Tensor, optional
        Center :math:`\mu` of the Gaussian distribution in the time domain.
        Use this to offset the signal in time. Defaults to 0.

    Returns
    -------
    Function
        A node representing a function that computes the integral of the
        Gaussian function.

    Notes
    -----
    The Gaussian that this function integrates is normalized in the time
    domain:

    .. math::
        \frac{e^{-(t-\mu)^2/(2\sigma^2)}}{\sqrt{2\pi\sigma^2}}.

    In the frequency domain, this Gaussian has standard deviation
    :math:`\omega_c= \sigma^{-1}`. The filter it represents therefore
    passes frequencies roughly in the range :math:`[-\omega_c, \omega_c]`.
    """

    name = "gaussian_integral_function"
    _module_attr = "create_gaussian_integral_function"
    args = [
        forge.arg("std", type=Union[float, types.Tensor]),
        forge.arg("offset", type=Optional[Union[float, types.Tensor]], default=0),
    ]
    kwargs = {}  # Functions don't accept name as an argument.
    rtype = types.Function


class SampleStf(CoreNode):
    """
    Samples an Stf at the given times.

    Parameters
    ----------
    stf : Stf
        The Stf to sample.
    sample_times : np.ndarray(1D, real)
        The times at which you want to sample the Stf. Must be ordered and contain
        at least one element.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The values of the Stf at the given times.

    See Also
    --------
    constant_stf_operator : Create a constant `Stf` operator.
    discretize_stf : Discretize an `Stf` into a `TensorPwc`.
    identity_stf : Create an `Stf` representing the identity function.
    """

    name = "sample_stf"
    _module_attr = "sample_stf"
    args = [
        forge.arg("stf", type=types.Stf),
        forge.arg("sample_times", type=np.ndarray),
    ]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        stf = kwargs.get("stf")
        check_argument(
            isinstance(stf, StfNodeData), "The stf must be an Stf.", {"stf": stf}
        )
        batch_shape, values_shape = validate_batch_and_values_shapes(stf, "stf")
        sample_times = kwargs.get("sample_times")
        check_sample_times(sample_times, "sample_times")
        time_count = len(sample_times)
        shape = batch_shape + (time_count,) + values_shape
        return TensorNodeData(_operation, shape=shape)


class IdentityStf(CoreNode):
    """
    Returns an Stf representing the identity function, f(t) = t.

    Returns
    -------
    Stf
        An Stf representing the identity function.

    See Also
    --------
    discretize_stf : Discretize an `Stf` into a `TensorPwc`.
    sample_stf : Sample an `Stf` at given times.
    """

    name = "identity_stf"
    _module_attr = "identity_stf"
    args = []
    kwargs = {}  # Stfs don't accept name as an argument.
    rtype = types.Stf

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        return StfNodeData(
            _operation,
            values_shape=(),
            batch_shape=(),
        )
