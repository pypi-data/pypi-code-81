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
A python client for connecting to Narupa servers.
"""

from typing import AbstractSet, Any, Protocol

from narupa.app import NarupaImdClient
from narupa.trajectory import FrameData

from narupatools.core.event import Event, EventListener


class OnFrameReceivedCallback(Protocol):
    """Callback for when a frame is received by a client."""

    def __call__(self, *, changes: AbstractSet[str]) -> None:  # noqa: D102
        ...


class NarupaClient(NarupaImdClient):
    """An extension of NarupaImdClient with more features."""

    _on_frame_received_event: Event[OnFrameReceivedCallback]

    def __init__(self, **kwargs: Any) -> None:
        """Create a NarupaClient.

        :param kwargs: Keyword arguments to pass to NarupaImdClient.
        """
        self._on_frame_received_event = Event()
        super().__init__(**kwargs)

    @property
    def on_frame_received(self) -> EventListener[OnFrameReceivedCallback]:
        """Event triggered when a frame is received by the client."""
        return self._on_frame_received_event

    def _on_frame_received(self, frame_index: int, frame: FrameData) -> None:
        changes = frame.array_keys | frame.value_keys
        super()._on_frame_received(frame_index, frame)
        self._on_frame_received_event.invoke(changes=changes)
