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
Code for handling selections in Scivana.
"""

from typing import Any, Iterable, List, Optional

from narupatools.state.serializable_object import Serializable
from narupatools.state.state_object import SharedStateObject


class ParticleSelection(SharedStateObject):
    """A selection of a set of particles in a simulation or trajectory."""

    _particle_ids: Optional[List[int]]
    _display_name: Optional[str]

    def __init__(self, *, particle_ids: Optional[Iterable[int]] = None, display_name: Optional[str] = None,
                 **kwargs: Serializable):
        super().__init__(**kwargs)
        if particle_ids is None:
            self.particle_ids = None
        else:
            self.particle_ids = list(particle_ids)
        self.display_name = display_name

    @property
    def particle_ids(self) -> Optional[List[int]]:
        """Set of ordered indices in the selection."""
        return self._particle_ids

    @particle_ids.setter
    def particle_ids(self, value: Optional[Iterable[int]]) -> None:
        if value is None:
            self._particle_ids = None
        else:
            self._particle_ids = list(value)

    @property
    def display_name(self) -> Optional[str]:
        """Display name of the selection."""
        return self._display_name

    @display_name.setter
    def display_name(self, value: Optional[str]) -> None:
        self._display_name = value

    def __repr__(self) -> str:
        representation = "<ParticleSelection"
        if self.particle_ids is not None:
            representation += f" particle_ids:{self.particle_ids}"
        if self.display_name is not None:
            representation += f" display_name:{self.display_name}"
        if self._arbitrary_data:
            representation += f" extra:{self._arbitrary_data}"
        representation += ">"
        return representation

    def __eq__(self, other: Any) -> bool:
        return (
                isinstance(other, ParticleSelection)
                and self.particle_ids == other.particle_ids
                and self.display_name == other.display_name
                and super().__eq__(other)
        )
