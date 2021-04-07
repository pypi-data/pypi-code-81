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
There is a difference between talking about in general something in the shared state dictionary (identified
by its key) and talking about its current value.

A SharedStateReference represents the former, defining a reference to a certain key in a certain dictionary.
As with the SharedStateView, the current value of the reference can be obtained by using snapshot(), which
returns a deep copy of the current value.

The value may also be modified, either by directly calling the update() function with a new value, or by
using the modify() context manager:

.. code:: python

    with reference.modify() as current_value:     # takes a snapshot and returns the current value
        current_value.x = 2                       # modify the value directly
                                                  # when the block ends, the value is automatically updated

Another feature of a SharedStateReference is that it can optionally be passed a type which inherits
from SerializableObject. Setting values in a dictionary from a SerializableObject is fine, as we know what
the type is and can call save(). However, to read a value from a dictionary as a certain object, we need to
know what kind of object to interperet it as. This is the point of the snapshot_class argument. Whenever
you obtain a snapshot of a value using a reference with this defined, the returned value will be of the
provided type.
"""

import copy
from contextlib import contextmanager
from typing import Any, Generic, Iterator, Optional, Type, TypeVar

from narupatools.state.typing import Serializable, SerializableDictionary
from ..serializable_object import SerializableObject

TValue = TypeVar('TValue')

TSpecificType = TypeVar('TSpecificType', bound=SerializableObject)


class SharedStateReference(Generic[TValue]):
    """
    Represents a reference to an item in a shared state dictionary
    """

    def __init__(self,
                 view: SerializableDictionary,
                 key: str,
                 snapshot_class: Optional[Type[TSpecificType]] = None):
        """
        Create a new reference to a shared state object

        :param view: A view of the shared state dictionary that handles getting, updating and removing keys
        :param key: The key in the shared state dictionary that this reference references
        :param snapshot_class: The class that snapshots of this reference should implement
        """

        self._view = view
        self.key = key
        self._snapshot_class = snapshot_class

    @classmethod
    def untyped_reference(cls,
                          view: SerializableDictionary,
                          key: str) -> 'SharedStateReference[Serializable]':
        """Get a reference to the specified key, without assuming its type."""
        return SharedStateReference(view, key)

    @classmethod
    def typed_reference(cls,
                        view: SerializableDictionary,
                        key: str,
                        snapshot_class: Type[TSpecificType]) -> 'SharedStateReference[TSpecificType]':
        """Get a reference to the specified key, assuming it can be represented as the specified type."""
        return SharedStateReference(view, key, snapshot_class)

    def snapshot(self) -> TValue:
        """
        Return a snapshot of the current state of the item at the time this function is called

        :raises KeyError: The shared state does not currently have a value with this key
        """
        value = copy.deepcopy(self._view[self.key])
        if self._snapshot_class is not None:
            return self._snapshot_class.deserialize(value)  # type: ignore
        return value  # type: ignore

    def remove(self) -> None:
        """
        Remove the key this reference references from the shared state

        :raises KeyError: If this reference doesn't have a value
        """
        del self._view[self.key]

    def _set_value(self, value: Any) -> None:
        if isinstance(value, SerializableObject):
            self._view[self.key] = value.serialize()
        else:
            self._view[self.key] = value

    def update(self, **kwargs: Serializable) -> None:
        """Update keys of this value, assuming that this value can be modified in this way."""
        snapshot = self.snapshot()
        for key, value in kwargs.items():
            snapshot[key] = value  # type: ignore
        self.set(snapshot)

    def set(self, snapshot: Optional[TValue] = None) -> None:
        """
        Update the current value, either by setting a completely new value or by passing in the keywords and values to
        add to the existing value.
        """
        self._set_value(snapshot)

    def has_value(self) -> bool:
        """
        Does this reference currently have a value in the shared state dictionary
        """
        return self.key in self._view

    @contextmanager
    def modify(self) -> Iterator[TValue]:
        """
        Return a snapshot of the current state, whose changes are applied to the shared state after it is modified
        """
        snapshot = self.snapshot()
        yield snapshot
        self.set(snapshot)

    def __repr__(self) -> str:
        representation = f"<SharedStateReference key:{self.key}"
        if self._snapshot_class:
            representation += f" type:{self._snapshot_class.__name__}"
        representation += ">"
        return representation

    def __eq__(self, obj: Any) -> bool:
        return isinstance(obj, SharedStateReference) and obj.key == self.key

    def __hash__(self) -> int:
        return hash(self.key)
