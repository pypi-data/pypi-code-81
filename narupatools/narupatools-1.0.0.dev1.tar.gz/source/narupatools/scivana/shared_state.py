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
View of a shared state of a Scivana-using server.
"""

from narupa.app import NarupaImdClient
from narupa.core import NarupaServer

from narupatools.scivana import (MultiplayerAvatar, ParticleSelection,
                                 Visualisation)
from narupatools.state.view import (SharedStateCollectionView,
                                    SharedStateDictionaryView)
from narupatools.state.view.wrappers import (SharedStateClientWrapper,
                                             SharedStateServerWrapper)


class SharedState(SharedStateDictionaryView):
    """Represents the shared state of a Narupa simulation, accessed through either a client or a server."""

    @classmethod
    def from_client(cls, client: NarupaImdClient) -> 'SharedState':
        """Get the shared state of a :func:`narupa.app.NarupaImdClient`."""
        return SharedState(SharedStateClientWrapper(client))

    @classmethod
    def from_server(cls, server: NarupaServer) -> 'SharedState':
        """Get the shared state of a :func:`narupa.core.NarupaServer`."""
        return SharedState(SharedStateServerWrapper(server))

    @property
    def selections(self) -> SharedStateCollectionView[ParticleSelection]:
        """Get a view of all the selections defined in the shared state dictionary."""
        return self.collection("selection.", snapshot_type=ParticleSelection)

    @property
    def visualisations(self) -> SharedStateCollectionView[Visualisation]:
        """Get a view of all the visualisations defined in the shared state dictionary."""
        return self.collection("visualisation.", snapshot_type=Visualisation)

    @property
    def avatars(self) -> SharedStateCollectionView[MultiplayerAvatar]:
        """Get a view of all the multiplayer avatars defined in the shared state dictionary."""
        return self.collection("avatar.", snapshot_type=MultiplayerAvatar)
