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
A shared state dictionary is constantly updating, but it is useful to keep track of references to
individual keys.

A SharedStateView represents a view to a SerializableDictionary, with more useful utility methods than
the simple wrapper SharedStateClientWrapper and SharedStateServerWrapper. When setting keys, either a
normal Serializable value can be provided, or alternatively any object which implements SerializableObject.
This removes the onus from the user from having to explicitly convert certain objects such as selections
into a serializable form before insertion into the dictionary.

Because the dictionary could be changing, accessing a key directly through the view does not actually
read the value from the dictionary. Instead, it returns a SharedStateReference, which stores both the
key you requested and the dictionary itself. For more information, see the documentation for
SharedStateReference.

A reference to a whole set of keys with a common prefix can be obtained by using the collection() method.

A snapshot of the current state of the dictionary can be obtained by calling the snapshot() method. This
returns a copy of the dictionary, which is no longer tied to the original and hence is a snapshot of its
value at that point in time.
"""
import abc
from abc import ABC
from contextlib import contextmanager
from typing import (AbstractSet, Any, Dict, Generic, Iterator, Mapping,
                    TypeVar, Union)

from narupatools.state.typing import Serializable, SerializableDictionary
from .reference import SharedStateReference
from ..serializable_object import SerializableObject

TValue = TypeVar('TValue', bound=Union[SerializableObject, Serializable])


class SharedStateView(ABC, Generic[TValue], Mapping[str, SharedStateReference[TValue]]):
    """
    Represents a view of a shared state dictionary. Accessing specific keys will not return their current
    value, but instead a SharedStateReference to a specific key.
    """

    def __init__(self, view: SerializableDictionary):
        """
        Create a view of a shared state dictionary, exposing the values only as references that can be
        snapshotted.

        :param view: A view of the shared state dictionary that handles getting, updating and removing keys
        """
        self._view = view

    def snapshot(self) -> Dict[str, TValue]:
        """
        Return a snapshot of each of the current items in this collection
        """
        keys = self._keys()
        return {key: self._make_snapshot(key) for key in keys}

    def set(self, key: str, snapshot: TValue) -> SharedStateReference[TValue]:
        """
        Insert a snapshot into the shared state dictionary and return a reference to it
        """
        key = self._resolve_key(key)
        self[key] = snapshot
        return self._make_reference(key)

    def update(self, key: str, **kwargs: Serializable) -> SharedStateReference[TValue]:
        """
        Update a value which is stored as a dictionary by getting the existing value and adding the provided
        key-value pairs.
        """
        key = self._resolve_key(key)
        self[key].update(**kwargs)
        return self._make_reference(key)

    @contextmanager
    def modify(self, key: str) -> Iterator[TValue]:
        """
        Return a snapshot of the current state, whose changes are applied to the shared state after it is modified
        """
        key = self._resolve_key(key)
        with self[key].modify() as snapshot:
            yield snapshot

    def __getitem__(self, key: str) -> SharedStateReference[TValue]:
        """
        Get a reference to the item with the given key

        :param key: The key to store in the dictionary

        :raises KeyError: The given key is not present in the shared state dictionary
        """
        key = self._resolve_key(key)
        if not isinstance(key, str):
            raise KeyError

        return self._make_reference(key)

    def __setitem__(self, key: str, value: TValue) -> None:
        """
        Set a shared state value with the given key

        :param key: The key to alter in the dictionary
        :param value: The value to be inserted into the dictionary. If it implements ``SharedStateSnapshot``, then
                      the ``serialize()`` method is called to generate the actual value to store

        :raises KeyError: The given key is not present in the shared state dictionary
        """
        key = self._resolve_key(key)
        if not isinstance(key, str):
            raise KeyError

        if isinstance(value, SerializableObject):
            self._view[key] = value.serialize()
        else:
            self._view[key] = value  # type: ignore

    def __delitem__(self, key: str) -> None:
        """
        Remove the item with the given key from the shared state dictionary

        :param key: The key to remove from the dictionary

        :raises KeyError: The given key is not present in the shared state dictionary
        """
        key = self._resolve_key(key)
        if not isinstance(key, str):
            raise KeyError

        del self._view[key]

    def __contains__(self, item: Any) -> bool:
        if isinstance(item, str):
            return self._resolve_key(item) in self._view
        elif isinstance(item, SharedStateReference):
            return item.key in self._view
        return False

    def __len__(self) -> int:
        return len(self._keys())

    def _keys(self) -> AbstractSet[str]:
        return self._view.keys()

    def _resolve_key(self, key: str) -> str:
        """Resolves a key, so collections can append their prefix if required."""
        return key

    @abc.abstractmethod
    def _make_reference(self, full_key: str) -> SharedStateReference[TValue]:
        """
        Create a reference to a specific item with the given key, which belongs in this collection

        :param full_key: The exact key to be referenced. This should begin with the prefix.
        """
        raise NotImplementedError

    def _make_snapshot(self, full_key: str) -> TValue:
        """
        Create a snapshot of the specific item with the given key, with the value copied at the time this
        function is called

        :param full_key: The exact key to be referenced. This should begin with the prefix.
        """
        return self._make_reference(full_key).snapshot()

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {len(self)} item(s)>"

    def clear(self) -> None:
        """
        Remove all keys in this dictionary
        """
        keys = self._keys()
        for key in list(keys):
            del self[key]

    def __iter__(self) -> Iterator[str]:
        yield from self._keys()
