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
Code for handling the Scivana multiplayer avatar.
"""

from typing import Any, List, Optional, Tuple

from narupatools.state.serializable_object import Serializable
from narupatools.state.state_object import SharedStateObject

Vector3 = Tuple[float, float, float]
Quaternion = Tuple[float, float, float, float]


class AvatarComponent(SharedStateObject):
    """A part of a multiplayer avatar, such as a controller or a headset."""
    _name: str
    _position: Vector3
    _rotation: Quaternion

    def __init__(self, name: str, position: Optional[Vector3] = None, rotation: Optional[Quaternion] = None,
                 **kwargs: Serializable):
        super().__init__(**kwargs)
        self.name = name
        self.position = position
        self.rotation = rotation

    @property
    def name(self) -> str:
        """The identifying name of the component that identifies what it is, such as a hand or headset."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def position(self) -> Optional[Vector3]:
        """The position of the component in world space."""
        return self._position

    @position.setter
    def position(self, value: Optional[Vector3]) -> None:
        if value is None:
            self._position = (0, 0, 0)
        else:
            self._position = value

    @property
    def rotation(self) -> Optional[Quaternion]:
        """The rotation of the component in world space."""
        return self._rotation

    @rotation.setter
    def rotation(self, value: Optional[Quaternion]) -> None:
        if value is None:
            self._rotation = (0, 0, 0, 1)
        else:
            self._rotation = value


class MultiplayerAvatar(SharedStateObject):
    """A multiplayer avatar in a Narupa session."""
    _name: Optional[str]
    _color: Optional[str]
    _components: List[AvatarComponent]

    def __init__(self, *, name: Optional[str] = None, color: Optional[str] = None,
                 components: Optional[List[AvatarComponent]] = None, **kwargs: Serializable):
        super().__init__(**kwargs)
        self.name = name
        self.color = color
        if components is None:
            self.components = []
        else:
            self.components = components

    @property
    def name(self) -> Optional[str]:
        """The player's display name."""
        return self._name

    @name.setter
    def name(self, value: Optional[str]) -> None:
        self._name = value

    @property
    def color(self) -> Optional[str]:
        """The player's color."""
        return self._color

    @color.setter
    def color(self, value: Optional[str]) -> None:
        self._color = value

    @property
    def components(self) -> List[AvatarComponent]:
        """A list of components (such as headsets and controllers) that make up this avatar."""
        return self._components

    @components.setter
    def components(self, value: List[AvatarComponent]) -> None:
        self._components = value

    def __eq__(self, other: Any) -> bool:
        return (
                isinstance(other, type(self))
                and self.name == other.name
                and self.color == other.color
                and super().__eq__(other)
        )
