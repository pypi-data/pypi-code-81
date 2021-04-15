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
"""Utilities for commons nodes."""
from typing import Union

import numpy as np

from qctrlcommons.exceptions import QctrlException
from qctrlcommons.preconditions import (
    check_argument,
    check_argument_integer,
    check_argument_numeric,
    check_argument_operator,
)

from . import types

NumericOrFunction = Union[
    float, complex, np.ndarray, types.Tensor, types.TensorPwc, types.Stf
]


def is_broadcastable(shape_a, shape_b) -> bool:
    """
    Checks if the shapes of two objects are broadcastable.

    Two shapes are broadcastable if, for each dimension starting from the end,
    they have the same size value, or if one of them has size 1.

    The function returns True even if some matching "dimensions" are negative.
    This can be used to compare shapes of Stf/Pwc objects by setting the size
    of their time_dimension to -1.

    Parameters
    ----------
    shape_a : tuple[int]
        Shape of one of the objects.
    shape_b : tuple[int]
        Shape of the other object.

    Returns
    -------
    bool
        True if shapes of two objects are broadcastable otherwise False
    """
    return all(
        ((dimension_a == dimension_b) or (dimension_a == 1) or (dimension_b == 1))
        for (dimension_a, dimension_b) in zip(shape_a[::-1], shape_b[::-1])
    )


def validate_broadcasted_shape(x_shape, y_shape, x_name, y_name):
    """
    Gets the resulting broadcasted shape for two input shapes.

    Parameters
    ----------
    x_shape : tuple[int]
        One of the shapes to be broadcasted.
    y_shape : tuple[int]
        The other of the shapes to be broadcasted.
    x_name : str
        The name of the variable whose shape is `x_shape`, used for the error
        message in case the shapes aren't broadcastable.
    y_name : str
        The name of the variable whose shape is `y_shape`, used for the error
        message in case the shapes aren't broadcastable.

    Returns
    -------
    tuple[int]
        The shape of the broadcasted array.

    Raises
    ------
    QctrlException
        if the two shapes aren't broadcastable.
    """

    if not is_broadcastable(x_shape, y_shape):
        raise QctrlException(
            f"The shapes {x_shape} of {x_name} and {y_shape} of {y_name}"
            " must be broadcastable."
        )

    # This is to make sure that the output doesn't have more than one
    # time dimension.
    if (-1 in x_shape) and (-1 in y_shape):
        if (len(x_shape) - x_shape.index(-1)) != (len(y_shape) - y_shape.index(-1)):
            raise QctrlException(
                f"The time dimensions of {x_name} and {y_name} are in incompatible positions."
            )

    shape_length = max(len(x_shape), len(y_shape))

    long_x_shape = (1,) * (shape_length - len(x_shape)) + tuple(x_shape)
    long_y_shape = (1,) * (shape_length - len(y_shape)) + tuple(y_shape)

    shape = (
        long_x_shape[index] if long_x_shape[index] != 1 else long_y_shape[index]
        for index in range(shape_length)
    )

    return tuple(shape)


def validate_function_output_shapes(
    x_batch_shape,
    x_values_shape,
    y_batch_shape,
    y_values_shape,
    validate_output_shape,
):
    """
    Gets the output batch and values shape for two input shapes of Pwcs/Stfs.
    The names of the variables are assumed to be x and y when reporting errors.

    Parameters
    ----------
    x_batch_shape : tuple[int]
        The batch shape of the first object.
    x_values_shape : tuple[int]
        The values shape of the first object.
    y_batch_shape : tuple[int]
        The batch shape of the second object.
    y_values_shape : tuple[int]
        The values shape of the second object.
    validate_output_shape : Callable[[tuple, tuple, str, str], tuple]
        Function that takes the full shapes of two Tensors, TensorPwcs, or
        Stfs (as well as their names), and returns the expected full shape
        of the output Tensor, TensorPwc, or Stf. (In these shapes, the time
        dimension is replaced with `-1`. If the other operand is a Tensor,
        a `-1` is inserted in the position that corresponds to the time
        dimension in the TensorPwc or Stf.) The function shouldn't assume
        that the shapes are compatible, and raise an exception if they
        aren't. The names of the Tensors should be used to generate the
        error message.

    Returns
    -------
    tuple[int], tuple[int]
        The batch and values shapes of the output Pwc/Stf.

    Raises
    ------
    QctrlException
        if the two objects aren't compatible.
    """
    x_shape = x_batch_shape + (-1,) + x_values_shape
    y_shape = y_batch_shape + (-1,) + y_values_shape

    shape = validate_output_shape(x_shape, y_shape, "x", "y")

    time_dimension = shape.index(-1)

    return shape[:time_dimension], shape[time_dimension + 1 :]


def validate_tensor_and_function_output_shapes(
    t_shape,
    f_batch_shape,
    f_values_shape,
    t_name,
    f_name,
    validate_output_shape,
    tensor_first=True,
):
    """
    Gets the output batch and values shape for an input tensor and an input Pwc/Stf.

    Parameters
    ----------
    t_shape : tuple[int]
        The shape of the tensor.
    f_batch_shape : tuple[int]
        The batch shape of the Pwc/Stf.
    f_values_shape : tuple[int]
        The values shape of the Pwc/Stf.
    t_name : str
        The name of the tensor variable, used for the error message in case the shapes aren't
        compatible.
    f_name : str
        The name of the function variable, used for the error message in case the shapes aren't
        compatible.
    validate_output_shape : Callable[[tuple, tuple, str, str], tuple]
        Function that takes the full shapes of two Tensors, TensorPwcs, or
        Stfs (as well as their names), and returns the expected full shape
        of the output Tensor, TensorPwc, or Stf. (In these shapes, the time
        dimension is replaced with `-1`. If the other operand is a Tensor,
        a `-1` is inserted in the position that corresponds to the time
        dimension in the TensorPwc or Stf.) The function shouldn't assume
        that the shapes are compatible, and raise an exception if they
        aren't. The names of the Tensors should be used to generate the
        error message.
    tensor_first : bool, optional
        Whether the Tensor is the leftmost parameter. Defaults to True.

    Returns
    -------
    tuple[int], tuple[int]
        The batch and values shapes of the output Pwc/Stf.

    Raises
    ------
    QctrlException
        if the two objects aren't compatible.
    """

    if len(f_values_shape) == 0:
        t_batch_shape = t_shape
        t_values_shape = ()
    else:
        t_batch_shape = t_shape[: -len(f_values_shape)]
        t_values_shape = t_shape[-len(f_values_shape) :]

    f_shape = f_batch_shape + (-1,) + f_values_shape
    if len(t_batch_shape) > 0:
        t_shape = t_batch_shape + (-1,) + t_values_shape
    else:
        t_shape = t_values_shape

    if tensor_first:
        shape = validate_output_shape(t_shape, f_shape, t_name, f_name)
    else:
        shape = validate_output_shape(f_shape, t_shape, f_name, t_name)

    time_dimension = shape.index(-1)

    return shape[:time_dimension], shape[time_dimension + 1 :]


def validate_shape(tensor_like, tensor_like_name):
    """
    Returns the shape of a scalar, np.ndarray, scipy.sparse.coo_matrix, or Tensor node.

    Parameters
    ----------
    tensor_like : number or np.ndarray or scipy.sparse.coo_matrix or TensorNodeData
        The object whose shape you want to obtain.
    tensor_like_name : str
        The name of the `tensor_like`, used for error message in case the
        input object is not valid.

    Returns
    -------
    tuple[int]
        The tuple with the size of each dimension of `tensor_like`.

    Raises
    ------
    QctrlException
        if the input is neither a scalar, a NumPy array, nor a Tensor.
    """

    if hasattr(tensor_like, "shape"):
        return tuple(tensor_like.shape)

    if np.isscalar(tensor_like):
        return ()

    raise QctrlException(f"The type of {tensor_like_name}={tensor_like} is not valid.")


def validate_batch_and_values_shapes(tensor, tensor_name):
    """
    Returns the batch and values shapes of TensorPwc or Stf.

    Paremeters
    ----------
    tensor : TensorPwcNodeData or StfNodeData
        The NodeData for the TensorPwc or Stf whose batch and values shapes
        you want to obtain.
    tensor_name : str
        The name of the TensorPwc or Stf, used for the error message in
        case `tensor` doesn't have a values shape.

    Returns
    -------
    tuple[tuple[int]]
        A tuple with a tuple that represents the batch shape, and a tuple
        that represents the values shape, in this sequence.

    Raises
    ------
    QctrlException
        if the input is neither a scalar, a TensorPwc, nor an Stf
    """

    if hasattr(tensor, "values_shape") and hasattr(tensor, "batch_shape"):
        return tuple(tensor.batch_shape), tuple(tensor.values_shape)

    if hasattr(tensor, "values_shape"):
        return (), tuple(tensor.values_shape)

    raise QctrlException(
        f"The type of {tensor_name}={tensor} must be TensorPwc or Stf."
    )


def validate_hamiltonian(hamiltonian, hamiltonian_name):
    """
    Checks whether a TensorPwc, Stf or SparsePwc contains values that are Hamiltonians.

    Hamiltonians are two-dimensional and square.

    Parameters
    ----------
    hamiltonian : TensorPwc or Stf or SparsePwc
        The Hamiltonian to be tested.
    hamiltonian_name : str
        The name of the Hamiltonian, used in the error message.
    """
    values_shape = getattr(hamiltonian, "values_shape", ())

    check_argument(
        len(values_shape) == 2,
        "The shape of the Hamiltonian must have 2 dimensions.",
        {hamiltonian_name: hamiltonian},
        extras={f"{hamiltonian_name}.values_shape": values_shape},
    )
    check_argument(
        values_shape[-1] == values_shape[-2],
        "The dimensions of the Hamiltonian must have equal sizes.",
        {hamiltonian_name: hamiltonian},
        extras={f"{hamiltonian_name}.values_shape": values_shape},
    )


def validate_ms_shapes(ion_count, ld_values, ld_name, rd_values, rd_name):
    """
    Checks if the shapes of the Mølmer–Sørensen parameters are correct.

    The correct shapes for the input parameters of Mølmer–Sørensen gate are
    ``(3, ion_count, ion_count)`` for the Lamb–Dicke parameters and
    ``(3, ion_count)`` for the relative detunings.

    Parameters
    ----------
    ion_count : int
        The number of ions in the chain.
    ld_values : np.ndarray
        The input values of the Lamb–Dicke parameters.
    ld_name : str
        The name of the argument that holds the Lamb–Dicke parameters.
    rd_values : np.ndarray
        The input values of the relative detunings.
    rd_name : str
        The name of the argument that holds the relative detunings.
    """
    check_argument_numeric(ld_values, ld_name)
    check_argument_numeric(rd_values, rd_name)

    ld_shape = validate_shape(ld_values, ld_name)
    rd_shape = validate_shape(rd_values, rd_name)

    check_argument(
        ld_shape == (3, ion_count, ion_count),
        "The Lamb–Dicke parameters must have shape (3, ion_count, ion_count).",
        {ld_name: ld_values},
        extras={"ion_count": ion_count, f"{ld_name}.shape": ld_shape},
    )
    check_argument(
        rd_shape == (3, ion_count),
        "The relative detunings must have shape (3, ion_count).",
        {rd_name: rd_values},
        extras={"ion_count": ion_count, f"{rd_name}.shape": rd_shape},
    )


def check_density_matrix_shape(density_matrix, name):
    """
    Checks the shape of the input density matrix.

    Parameters
    ----------
    density_matrix : Union[TensorNodeData, np.ndarray]
        A density matrix.
    name : str
        Name of the density matrix.
    """
    check_argument_numeric(density_matrix, name)
    density_matrix_shape = validate_shape(density_matrix, name)
    check_argument(
        len(density_matrix_shape) in [2, 3],
        f"The {name} must be 2D or 3D with the first axis as the batch dimension.",
        {name: density_matrix},
        extras={"density matrix shape": density_matrix_shape},
    )
    check_argument(
        density_matrix_shape[-1] == density_matrix_shape[-2],
        f"The {name} must be a square in the last two dimensions.",
        {name: density_matrix},
        extras={"density matrix shape": density_matrix_shape},
    )


def check_oqs_hamiltonian(hamiltonian, system_dimension):
    """
    Check whether open quantum system (OQS) Hamiltonian is valid.

    Parameters
    ----------
    hamiltonian : Union[TensorPwc, SparsePwc]
        Effective system Hamiltonian.
    system_dimension : int
        System Hilbert space dimension.
    """
    check_argument_integer(system_dimension, "system dimension")
    check_argument(
        hamiltonian.values_shape == (system_dimension, system_dimension),
        "The dimension of the Hamiltonian compatible with the dimension "
        "of the system Hilbert space.",
        {
            "hamiltonian": hamiltonian,
        },
        extras={
            "hamiltonian dimension": hamiltonian.values_shape,
            "system dimension": system_dimension,
        },
    )


def check_lindblad_terms(lindblad_terms, system_dimension):
    """
    Check whether Lindblad terms are valid.

    Parameters
    ----------
    lindblad_terms : List[Tuple[float, Union[np.ndarray, coo_matrix]]]
        Effective system Hamiltonian.
    system_dimension : int
        System Hilbert space dimension.
    """
    check_argument_integer(system_dimension, "system dimension")
    for index, (rate, operator) in enumerate(lindblad_terms):
        check_argument(
            rate > 0,
            ("The decay rate must be positive."),
            {"lindblad_terms": lindblad_terms},
        )
        check_argument_numeric(operator, f"lindblad_terms[{index}][1]")
        _ = validate_shape(operator, f"lindblad_terms[{index}][1]")
        check_argument_operator(operator, f"lindblad_terms[{index}][1]")
        check_argument(
            operator.shape[0] == system_dimension,
            "The dimension of Lindblad operator must be compatible with the dimension "
            "of the system Hilbert space.",
            {"lindblad_terms": lindblad_terms},
            extras={
                "lindblad operator dimension": operator.shape,
                "system dimension": system_dimension,
            },
        )
