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
Base class for some kind of runner that uses simulation dynamics.
"""
import time
from abc import ABCMeta
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Dict, Generator, Generic, Optional, Protocol, TypeVar

from infinite_sets import InfiniteSet
from narupa.app import NarupaImdApplication
from narupa.app.app_server import DEFAULT_NARUPA_PORT
from narupa.core import DEFAULT_SERVE_ADDRESS, NarupaServer
from narupa.essd import DiscoveryServer
from narupa.trajectory import FrameData
from narupa.utilities.change_buffers import DictionaryChange

from narupatools.core.dynamics import SimulationDynamics
from narupatools.core.event import Event
from narupatools.core.playable import Playable
from narupatools.core.servable import Servable
from narupatools.frame import KineticEnergy, ParticlePositions, PotentialEnergy
from narupatools.frame.frame_producer import FrameProducer
from narupatools.frame.frame_source import FrameSource

TTarget = TypeVar('TTarget')


@dataclass
class SharedStateKeyInfo:
    """Tracks information about who is intefering with a shared state key and when it is occuring."""

    key: str
    last_access_token: Optional[str]
    time_first_updated: float
    time_last_updated: float

    def __init__(self, key: str, time: float, token: Optional[str]):
        self.key = key
        self.time_first_updated = time
        self.time_last_updated = time
        self.last_access_token = token

    def update(self, time: float, token: Optional[str]) -> None:
        """
        Update the information stored about this key.

        :param time: Real time that this key was last updated.
        :param token: Token who was responsible for the last update.
        """
        self.time_last_updated = time
        self.last_access_token = token


class OnSharedStateAddedCallback(Protocol):
    """Callback for when a key is first added to the shared state."""

    def __call__(self, *, key: str, token: Optional[str], time_added: float) -> None:
        """
        Called when a key is first added to the shared state.

        :param key: Full key of the item.
        :param token: Access token used to add this item.
        :param time_added: Real time that this key was added.
        """
        pass


class OnSharedStateChangedCallback(Protocol):
    """Callback for when a key is changed in the shared state."""

    def __call__(self, *, key: str, token: Optional[str], previous_token: Optional[str],
                 time_updated: float, time_last_updated: float) -> None:
        """
        Called when a key is changed in the shared state.

        :param key: Full key of the item.
        :param token: Access token that is modifying this item.
        :param previous_token: Access token that last modified this item.
        :param time_updated: Real time that this key was updated.
        :param time_last_updated: Real time that this key was last updated.
        """
        pass


class OnSharedStateRemovedCallback(Protocol):
    """Callback for when a key is removed from the shared state."""

    def __call__(self, *, key: str, token: Optional[str], previous_token: Optional[str],
                 time_deleted: float, time_last_updated: float) -> None:
        """
        Called when a key is removed from the shared state.

        :param key: Full key of the item.
        :param token: Access token that is deleting this item.
        :param previous_token: Access token that last modified this item.
        :param time_deleted: Real time that this key was deleted.
        :param time_last_updated: Real time that this key was last updated.
        """
        pass


TTarget_Co = TypeVar('TTarget_Co', contravariant=True)


class OnTargetChanged(Protocol[TTarget_Co]):
    """Callback for when the target of a NarupaSession is altered."""

    def __call__(self, target: Optional[TTarget_Co], previous_target: Optional[TTarget_Co]) -> None:
        """
        Called when the target of a NarupaSession is altered.

        :param target: The new target of the session, if any.
        :param previous_target: The previous target of the session, if any.
        """
        pass


class NarupaSession(Generic[TTarget], metaclass=ABCMeta):
    """
    A session is a Narupa server bundled with the ability to change what is being displayed.

    A session has one target at a time, which can be a simulation, trajectory or a single frame.

    The session has a background loop which periodically gets a FrameData to send to the clients. If the target
    implements FrameSource, this indicates the target can produce a frame and this will be sent to the clients. This
    background loop only sends fields which have been marked as dirty.
    """

    _target: Optional[TTarget]
    _on_shared_state_added: Event[OnSharedStateAddedCallback]
    _on_shared_state_changed: Event[OnSharedStateChangedCallback]
    _on_shared_state_removed: Event[OnSharedStateRemovedCallback]
    _on_target_changed: Event[OnTargetChanged[TTarget]]
    _shared_state_key_info: Dict[str, SharedStateKeyInfo]
    server: NarupaImdApplication

    def __init__(self, **kwargs: Any):
        self._target = None

        self.frame_index = 0
        self._initialise_server(**kwargs)

        self._frame_producer = FrameProducer(self._produce_frame)
        self._frame_producer.on_frame_produced.add_callback(self._on_frame_produced)
        self._frame_producer.start(block=False)

        self._shared_state_key_info = {}

        self.server.server._state_service.state_dictionary.content_updated.add_callback(self._on_content_updated)

        self._on_shared_state_added = Event(OnSharedStateAddedCallback)
        self._on_shared_state_changed = Event(OnSharedStateChangedCallback)
        self._on_shared_state_removed = Event(OnSharedStateRemovedCallback)
        self._on_target_changed = Event(OnTargetChanged)

    def _on_content_updated(self, access_token: str, change: DictionaryChange) -> None:
        current_time = time.monotonic()
        for key in change.updates:
            if key not in self._shared_state_key_info:
                self._shared_state_key_info[key] = SharedStateKeyInfo(key, current_time, access_token)
                self._on_shared_state_added.invoke(key=key, token=access_token, time_added=current_time)
            else:
                info = self._shared_state_key_info[key]
                last_time = info.time_last_updated
                last_token = info.last_access_token
                info.update(current_time, access_token)
                self._on_shared_state_changed.invoke(key=key, token=access_token, time_updated=current_time,
                                                     time_last_updated=last_time, previous_token=last_token)
        for key in change.removals:
            if key in self._shared_state_key_info:
                info = self._shared_state_key_info[key]
                del self._shared_state_key_info[key]
                last_time = info.time_last_updated
                last_token = info.last_access_token
                self._on_shared_state_removed.invoke(key=key, token=access_token, time_deleted=current_time,
                                                     time_last_updated=last_time, previous_token=last_token)

    def _on_frame_produced(self, *, frame: FrameData, **kwargs: Any) -> None:
        self.server.frame_publisher.send_frame(self.frame_index, frame)
        self.frame_index += 1

    def run(self, block: bool = False) -> None:
        """
        Run the target if it is a playable object.

        :raises RuntimeError: The target is not an instance of Playable.
        :param block: Should this be run in blocking mode.
        """
        if not isinstance(self._target, Playable):
            raise RuntimeError("Runner has invalid target.")
        self._target.run(block)

    def stop(self) -> None:
        """
        Stop the target if it is a playable object.
        """
        if isinstance(self._target, Playable):
            self._target.stop(wait=True)

    def show(self, target: TTarget) -> None:
        """Broadcast the given object through the session, replacing the old target if it exists."""
        self.target = target

    @property
    def target(self) -> Optional[TTarget]:
        """Target which is being broadcast by this session."""
        return self._target

    @target.setter
    def target(self, value: TTarget) -> None:
        if isinstance(self._target, Playable):
            self._target.stop(wait=True)
        if isinstance(self._target, SimulationDynamics):
            self._target.on_reset.remove_callback(self._on_target_reset)
            self._target.on_post_step.remove_callback(self._on_target_step)
        if isinstance(self._target, Servable):
            self._target.end_being_served(self)

        previous_target = self._target
        self._target = value

        if isinstance(self._target, SimulationDynamics):
            self._target.on_reset.add_callback(self._on_target_reset)
            self._target.on_post_step.add_callback(self._on_target_step)
        if isinstance(self._target, Servable):
            self._target.start_being_served(self)

        # Trigger a full frame reset
        self._frame_producer.mark_dirty()

        self._on_target_changed.invoke(target=self._target, previous_target=previous_target)  # type: ignore

    def _on_target_reset(self, **kwargs: Any) -> None:
        self._frame_producer.mark_dirty()

    def _on_target_step(self, **kwargs: Any) -> None:
        self._frame_producer.mark_dirty({ParticlePositions.key, PotentialEnergy.key, KineticEnergy.key})

    def _produce_frame(self, fields: InfiniteSet[str]) -> FrameData:
        """
        Called by the frame producing loop to request a new frame. Also a level 0 cantrip.

        :param fields: The set of fields that the frame is interested in.
        :return: A FrameData to send to the clients. If there isn't a target or the target doesn't produce frames, this
        returns a blank frame.
        """
        if isinstance(self._target, FrameSource):
            return self._target.get_frame(fields)
        return FrameData()

    def _initialise_server(self,
                           name: Optional[str] = None,
                           address: Optional[str] = None,
                           port: Optional[int] = None,
                           run_discovery: bool = True,
                           discovery_port: Optional[int] = None) -> None:

        address = address or DEFAULT_SERVE_ADDRESS
        if port is None:
            port = DEFAULT_NARUPA_PORT
        server = NarupaServer(address=address, port=port)
        discovery: Optional[DiscoveryServer] = None
        if run_discovery:
            discovery = DiscoveryServer(broadcast_port=discovery_port)
        self.server = NarupaImdApplication(server, discovery, name)

    def close(self) -> None:
        """Remove the current target and close down the server and background tasks."""
        self.target = None
        self._frame_producer.stop(wait=True)
        self.server.close()

    def health_check(self) -> None:
        """Triggers an exception if an issue has occured in a background task."""
        self._frame_producer.health_check()
        if isinstance(self._target, Playable):
            self._target.health_check()

    @classmethod
    @contextmanager
    def start(cls, **kwargs: Any) -> Generator['NarupaSession', None, None]:
        """Start a `NarupaSession` as a context manager, calling close() after completion."""
        session = cls(**kwargs)
        yield session
        session.close()
