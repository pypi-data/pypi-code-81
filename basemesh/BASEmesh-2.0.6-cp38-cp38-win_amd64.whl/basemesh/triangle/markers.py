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

"""Defines the hole and region point markers for quality meshing."""

from typing import Optional, Tuple


class HoleMarker:
    """Marks a segment-bounded region as a hole."""

    __slots__ = ('_pos_x', '_pos_y')

    def __init__(self, pos_x: float, pos_y: float) -> None:
        """Initialize a new hole marker.

        Parameters
        ----------
        pos_x : float
            X position of the marker
        pos_y : float
            Y position of the marker
        """
        self._pos_x = pos_x
        self._pos_y = pos_y

    def as_tuple(self) -> Tuple[float, float]:
        """Return the coordinates of the marker as a tuple."""
        return self._pos_x, self._pos_y


class RegionMarker:
    """Defines properties of a segment-bounded region."""

    __slots__ = ('_attribute', '_max_area', '_pos_x', '_pos_y')

    def __init__(self, pos_x: float, pos_y: float, *, max_area: float = -1.0,
                 attribute: Optional[int] = None) -> None:
        """Initialise a new region marker.

        Parameters
        ----------
        pos_x : float
            X position of the marker
        pos_y : float
            Y position of the marker
        max_area : float, optional
            A maximum area constraint to apply to elements in this
            region, negative values signify that no area constraints
            should be applied, by default -1.0
        attribute : int, optional
            A regional attribute to associate with elements in this
            region, by default None
        """
        self._attribute = attribute
        self._max_area = max_area if max_area > 0.0 else -1.0
        self._pos_x = pos_x
        self._pos_y = pos_y

    @property
    def attribute(self) -> Optional[int]:
        """Return the attribute to apply to elements in this region."""
        return self._attribute

    @property
    def max_area(self) -> float:
        """Return the maximum area constraint for this region.

        A value of -1.0 signifies that no constraint will be applied.
        """
        return self._max_area

    def as_tuple(self) -> Tuple[float, float]:
        """Return the coordinates of the marker as a tuple."""
        return self._pos_x, self._pos_y
