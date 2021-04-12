# A component of the BASEmesh pre-processing toolkit.
# Copyright (C) 2020  ETH Zürich

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Core components of the BASEmesh data model.

This includes the implementation of data classes for geometry and mesh
objects, as well as supporting code and utilities specific to them.
"""

from .geometry import Lattice, Node, Segment
from .mesh import Mesh, MeshElement, MeshNode

__all__ = [
    'Lattice',
    'Mesh',
    'MeshElement',
    'MeshNode',
    'Node',
    'Segment'
]
