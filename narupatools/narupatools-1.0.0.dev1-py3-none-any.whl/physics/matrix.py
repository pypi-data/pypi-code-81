# This file is part of narupatools (https://gitlab.com/alexjbinnie/narupatools).
# Copyright (c) University of Bristol. All rights reserved.
#
# narupatools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# narupatools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with narupatools.  If not, see <http://www.gnu.org/licenses/>.

"""
Utility methods for using matrices.
"""

import numpy as np

from .typing import Matrix3x3, Matrix3x3Like


def zero_matrix() -> Matrix3x3:
    """Create a 3x3 matrix with all zero entries."""
    return np.zeros((3, 3))


def identity_matrix() -> Matrix3x3:
    """Create a 3x3 identity matrix, with 1 along the diagonal and 0 on the off diagonal."""
    return np.identity(3)


def kronecker_delta(i: int, j: int) -> float:
    """
    Evaluates as 1 when parameters i and j are equal and 0 otherwise.
    """
    return 1.0 if i == j else 0.0


def matrix_inverse(matrix: Matrix3x3Like) -> Matrix3x3:
    """
    Calculate the inverse :math:`M^{-1}` of a 3x3 matrix :math:`M`.

    :param matrix: Matrix :math:`M^{-1} to invert.
    :raises ValueError: Matrix is singular and hence an inverse does not exist.
    :return: Inverse of the matrix :math:`M`
    """
    try:
        return np.linalg.inv(matrix)  # type: ignore[no-any-return]
    except np.linalg.LinAlgError:
        raise ValueError("Matrix is singular and hence cannot be inverted.")
