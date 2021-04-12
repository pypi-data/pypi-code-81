"""Pre-processing and mesh generation toolkit for BASEMENT.

This package contains utilities for generating and processing 1D and 2D
mesh geometries for use with the numerical simulation software such as
BASEMENT (https://basement.ethz.ch/).

It features standalone mesh generation utilities leveraging Jonathan
Shewchunk's Triangle (https://www.cs.cmu.edu/~quake/triangle.html), as
well as mesh editing and interpolation utilities.

BASEmesh can also be installed as a plugin for QGIS
(https://qgis.org/en/site/), allowing usage of its functionality via
the plugin interface.

For additional information, refer to the BASEMENT website linked above
or visit the project repository at
https://git.ee.ethz.ch/basemesh/basemesh-v2/.


Copyright (C) 2020  ETH Zürich

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from . import abc
from . import meshtool
from . import triangle
from .core import Node, Mesh, MeshElement, MeshNode, Segment
from .interpolation import calculate_element_elevation, interpolate_mesh
from .meshing import elevation_mesh, quality_mesh
from .stringdefs import (resolve_string_defs, write_string_defs_mesh,
                         write_string_defs_sidecar)

__version__ = '2.0.6'

try:
    from qgis.gui import QgisInterface  # type: ignore
except ImportError:
    QGIS_ENVIRONMENT = False
else:
    QGIS_ENVIRONMENT = True
    from .plugin import classFactory
