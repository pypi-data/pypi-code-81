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
Code for dealing with visualisations in Scivana.
"""

from typing import Any, Dict, Optional, Union

from narupatools.state.serializable_object import Serializable
from narupatools.state.state_object import SharedStateObject


class Visualisation(SharedStateObject):
    """Visualisation of molecular data."""

    _display_name: Optional[str]
    _selection: Optional[str]
    _visualiser: Optional[Union[str, Dict[str, Serializable]]]
    _frame: Optional[Dict[str, Any]]
    _hide: Optional[bool]
    _layer: Optional[int]
    _priority: Optional[float]

    def __init__(self, *, display_name: Optional[str] = None, selection: Optional[str] = None,
                 frame: Optional[Dict[str, Serializable]] = None,
                 visualiser: Optional[Union[str, Dict[str, Serializable]]] = None, hide: Optional[bool] = None,
                 layer: Optional[int] = None, priority: Optional[float] = None,
                 **kwargs: Serializable):
        super().__init__(**kwargs)
        self.display_name = display_name
        self.selection = selection
        self.frame = frame
        self.visualiser = visualiser
        self.hide = hide
        self.layer = layer
        self.priority = priority

    @property
    def display_name(self) -> Optional[str]:
        """User-facing display name of the visualisation."""
        return self._display_name

    @display_name.setter
    def display_name(self, value: Optional[str]) -> None:
        self._display_name = value

    @property
    def selection(self) -> Optional[str]:
        """Full id of the selection drawn by this visualiser."""
        return self._selection

    @selection.setter
    def selection(self, value: Optional[str]) -> None:
        self._selection = value

    @property
    def frame(self) -> Optional[Dict[str, Any]]:
        """Frame to be drawn by this visualiser."""
        return self._frame

    @frame.setter
    def frame(self, value: Optional[Dict[str, Any]]) -> None:
        self._frame = value

    @property
    def visualiser(self) -> Optional[Union[str, Dict[str, Serializable]]]:
        """Definition of this visualiser."""
        return self._visualiser

    @visualiser.setter
    def visualiser(self, value: Optional[Union[str, Dict[str, Serializable]]]) -> None:
        self._visualiser = value

    @property
    def hide(self) -> Optional[bool]:
        """Should this visualiser be hidden?"""
        return self._hide

    @hide.setter
    def hide(self, value: Optional[bool]) -> None:
        self._hide = value

    @property
    def layer(self) -> Optional[int]:
        """Layer should this visualiser be drawn on."""
        return self._layer

    @layer.setter
    def layer(self, value: Optional[int]) -> None:
        self._layer = value

    @property
    def priority(self) -> Optional[float]:
        """Priority of this visualiser in its layer."""
        return self._priority

    @priority.setter
    def priority(self, value: Optional[float]) -> None:
        self._priority = value

    def __repr__(self) -> str:
        str = "<Visualisation"
        if self.display_name is not None:
            str += f" display_name:{self.display_name}"
        if self.selection is not None:
            str += f" selection:{self.selection}"
        if self.frame is not None:
            str += f" frame:{self.frame}"
        if self.visualiser is not None:
            str += f" visualiser:{self.visualiser}"
        if self.hide is not None:
            str += f" hide:{self.hide}"
        if self.layer is not None:
            str += f" layer:{self.layer}"
        if self.priority is not None:
            str += f" priority:{self.priority}"
        if self._arbitrary_data:
            str += f" extra:{self._arbitrary_data}"
        str += ">"
        return str

    def __eq__(self, other: Any) -> bool:
        return (
                isinstance(other, Visualisation)
                and self.display_name == other.display_name
                and self.selection == other.selection
                and self.visualiser == other.visualiser
                and self.frame == other.frame
                and self.hide == other.hide
                and self.layer == other.layer
                and self.priority == other.priority
                and super().__eq__(other)
        )
