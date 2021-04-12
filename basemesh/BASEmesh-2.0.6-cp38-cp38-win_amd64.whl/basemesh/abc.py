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

"""Abstract base classes for BASEmesh."""

# pylint: disable=too-few-public-methods

from abc import ABCMeta, abstractmethod
from typing import Iterator, Collection, Generic, TypeVar
from .types import Point2D

T = TypeVar('T')


class ElevationSource(metaclass=ABCMeta):
    """ABC for elevation information provider classes.

    Classes supporting this ABC can be used as elevation sources for
    mesh interpolation.
    """

    @abstractmethod
    def elevation_at(self, point: Point2D) -> float:
        """Return the elevation at the given point.

        If the point lies outside the intended area of this elevation
        source, a ValueError should be raised instead. The interpolator
        will then fall through to the next elevation source and attempt
        to use its elevation data.

        Parameters
        ----------
        point : Tuple[float, float]
            The point to interpolate

        Returns
        -------
        float
            The interpolated elevation

        Raises
        ------
        NotImplementedError
            Always raised as this is an abstract method
        """
        raise NotImplementedError


class SpatialCollection(Generic[T], Collection[T]):
    """Represents a spatial container type.

    This ABC adds the iter_spatial() method, which allows optimisation
    of the iteration order using a seed point.

    iter_spatial() will fall back to the default iterator if not
    overridden.
    """

    def iter_spatial(self, point: Point2D) -> Iterator[T]:
        """Iterate over the contents, starting near the seed point.

        Similar to __iter__, but with a predefined starting point
        used for iterator creation. The iterator will return elements
        near the given point before moving outwards.

        Note that there is no guarantee that the order will actually
        hit nearby elements first.

        Parameters
        ----------
        point : Tuple[float, float]
            The seed point to start iterating at

        Returns
        -------
        Iterator[T]
            Iterator over the contents
        """
        _ = point  # Value intentionally discarded
        return iter(self)


class SupportsSpatial(metaclass=ABCMeta):
    """ABC for objects that can be used in space-aware containers.

    This ABC defines the spatial_marker property, which returns a
    tuple of two floats representing the given object.

    Attributes
    ----------
    spatial_marker : Tuple[float, float]
        A 2D point representing the object, used for positioning in
        memory
    """

    @property
    @abstractmethod
    def spatial_marker(self) -> Point2D:
        """Return a 2D point representing this object.

        This point will be used by space-aware containers to optimise
        memory layout.
        """
        raise NotImplementedError
