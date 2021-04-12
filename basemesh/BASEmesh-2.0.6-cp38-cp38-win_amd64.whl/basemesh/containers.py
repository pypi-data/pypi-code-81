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

"""Custom container and iterator definitions for BASEmesh."""

from typing import Any, Generic, Iterable, Iterator, Optional, Set, TypeVar
from .abc import SpatialCollection

T = TypeVar('T')


class SpatialSet(SpatialCollection[T], Generic[T], Set[T]):
    """A set subclass compatible with the SpatialCollection ABC.

    This behaves exactly like a normal set and is used as a temporary
    container until proper space-aware containers are added.

    Please note that this is a temporary solution that will not be
    satisfactory for large data sets.
    It can be considered "deprecated by design" and will be replaced
    with a proper solution very soon.
    """

    def __init__(self, iterable: Optional[Iterable[T]] = None) -> None:
        """Initialise the container.

        Parameters
        ----------
        iterable : Iterable[T], optional
            An iterable to populate the set with, by default None
        """
        self._data: Set[T] = set()
        if iterable is not None:
            self._data.update(iterable)

    def __contains__(self, element: Any) -> bool:
        """Return whether the element is contained.

        Parameters
        ----------
        element : Any
            The element to check for containment

        Returns
        -------
        bool
            Whether the element is contained in the collection
        """
        return element in self._data

    def __iter__(self) -> Iterator[T]:
        """Return an iterator over the container's elements."""
        return iter(self._data)

    def __len__(self) -> int:
        """Return the number of elements in the container."""
        return len(self._data)

    def add(self, value: T) -> None:
        """Add the given value to the collection.

        Parameters
        ----------
        value : T
            The value to add
        """
        self._data.add(value)

    def clear(self) -> None:
        """Remove all items from the container."""
        self._data.clear()

    def discard(self, element: T) -> None:
        """Remove an item from the container.

        If the item cannot be found, do nothing.

        Parameters
        ----------
        element : T
            Discard an element from the collection
        """
        self._data.discard(element)

    def remove(self, element: T) -> None:
        """Remove an element from the container.

        If the element cannot be found, a KeyError will be raised.

        Parameters
        ----------
        element : T
            The element to remove
        """
        self._data.remove(element)

    def pop(self) -> T:
        """Remove and return any item from the container."""
        return self._data.pop()
