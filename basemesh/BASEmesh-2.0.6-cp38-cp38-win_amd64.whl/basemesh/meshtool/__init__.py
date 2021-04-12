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

"""Arbitrary 2.5D mesh generator.

This module utilizes BASEmesh components to generate arbitrary meshes.
The mesh geometry itself is derived from meshing a given domain using
'Triangle' and subsequently interpolation its elevation according to a
user-defined function.
"""

from ..core.geometry import Node, Segment
from ..interpolation import calculate_element_elevation
from ..triangle import HoleMarker, RegionMarker
from .core import AbstractFactory, BasicFactory

__version__ = '0.1.0a'
