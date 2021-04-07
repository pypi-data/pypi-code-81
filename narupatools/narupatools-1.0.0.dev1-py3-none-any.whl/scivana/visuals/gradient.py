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

"""Functions for generating gradients for use with Scivana."""

from matplotlib import cm

from .typing import SerializableColor, SerializableGradient


def gradient_from_colors(*args: SerializableColor) -> SerializableGradient:
    """Create a gradient from a set of colors."""
    return list(args)


def gradient_from_matplotlib(name: str) -> SerializableGradient:
    """Create a gradient from a matploblib color map."""
    cmap = cm.get_cmap(name)
    return [list(cmap(x / 7)) for x in range(0, 8, 1)]  # type: ignore
