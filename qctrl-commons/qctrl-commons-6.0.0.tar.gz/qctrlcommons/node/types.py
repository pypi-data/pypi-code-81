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
"""Argument and result types for nodes."""

# pylint:disable=too-few-public-methods


class Target:
    """
    A target gate for an infidelity calculation.

    See Also
    --------
    target : Define the target operation of a time evolution.
    """


class Tensor:
    """
    A multi-dimensional array of data.

    Most functions accepting a :obj:`.Tensor` object can alternatively accept a NumPy array.

    You can use the arithmetic operators ``+``, ``-``, ``*``, ``**``, ``/``, ``//``, and ``@``
    to perform operations between two `Tensor` objects.
    """


class TensorPwc:
    """
    A piecewise-constant tensor-valued function of time (or batch of such functions).

    You can use the arithmetic operators ``+``, ``-``, ``*``, ``**``, ``/``, ``//``, and ``@``
    to perform operations between two `TensorPwc` objects or between a `TensorPwc` and a `Tensor`.

    Attributes
    ----------
    values : Tensor
        The values of the function on the piecewise-constant segments.

    See Also
    --------
    tensor_pwc : Create piecewise-constant functions.
    """


class SparsePwc:
    """
    A piecewise-constant sparse-matrix-valued function of time.

    See Also
    --------
    sparse_pwc_operator : Create `SparsePwc` operators.
    """


class Stf:
    """
    A sampleable tensor-valued function of time (or batch of such functions).

    You can use the arithmetic operators ``+``, ``-``, ``*``, ``**``, ``/``, ``//``, and ``@``
    to perform operations between two `Stf` objects or between an `Stf` and a `Tensor`.

    Notes
    -----
    Stf represents an arbitrary function of time. Piecewise-constant (PWC) or constant functions
    are special cases of Stfs and Q-CTRL python package provides specific APIs to support them.
    Note that as the PWC property can simplify the calculation, you should always consider using
    PWC-related APIs if your system parameters or controls are described by PWC functions.

    See Also
    --------
    identity_stf : Create an `Stf` representing the identity function.
    """


class Function:
    """
    A generic callable function.

    See Also
    --------
    convolve_pwc : Create an `Stf` by convolving a `TensorPwc` with a kernel.
    gaussian_integral_function : Create a function that computes the integral of a normalized
        Gaussian.
    sinc_integral_function : Create a function that computes the integral of the sinc function.
    """


# Registry of all types created by operations.
TYPE_REGISTRY = [
    Target,
    Tensor,
    TensorPwc,
    SparsePwc,
    Stf,
    Function,
]
