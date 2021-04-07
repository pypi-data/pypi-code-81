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
Types for annotating physics methods in a more meaningful way.
"""

from typing import Sequence, Union

import numpy as np

Matrix3x3Like = Union[np.ndarray, Sequence[np.ndarray], Sequence[Sequence[float]]]
"""Any type which can be interpreted as a (3, 3) float array by NumPy."""

QuaternionLike = Union[np.ndarray, Sequence[float]]
"""Any type which can be interpreted as a (4,) float array by NumPy."""

Vector3Like = Union[np.ndarray, Sequence[float]]
"""Any type which can be interpreted as a (3,) float array by NumPy."""

VectorNLike = Union[np.ndarray, Sequence[float]]
"""Any type which can be interpreted as a (N,) float array by NumPy."""

ScalarArrayLike = Union[np.ndarray, Sequence[np.ndarray], Sequence[Sequence[float]]]
"""Any type which can be interpreted as a (n,) float array by NumPy."""

Vector3ArrayLike = Union[np.ndarray, Sequence[np.ndarray], Sequence[Sequence[float]]]
"""Any type which can be interpreted as a (n, 3) float array by NumPy."""

RotationLike = Union[np.ndarray, Sequence[float]]
"""Any type which can be interpreted as a rotation, either a (3, 3) float array or a (4, ) float array."""

ScalarArray = np.ndarray
"""A NumPy float array of shape (n,), representing a list of scalar values."""

Vector3 = np.ndarray
"""A NumPy float array of shape (3, ), representing a three dimensional vector."""

Vector3Array = np.ndarray
"""A NumPy float array of shape (N, 3), representing a list of three dimensional vectors."""

VectorN = np.ndarray
"""A NumPy float array of shape (N,), representing an N-dimensional vector."""

Matrix3x3 = np.ndarray
"""A NumPy float array of shape (3, 3), representing a 3x3 matrix."""

Quaternion = np.ndarray
"""A NumPy float array of shape (4,), representing a quaternion :math:`q = x i + y j + z k + w` as a
vector (x, y, z, w)."""
