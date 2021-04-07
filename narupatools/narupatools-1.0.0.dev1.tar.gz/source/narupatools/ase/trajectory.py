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
#
# Originally part of the narupa-ase package.
# Copyright (c) Intangible Realities Lab, University Of Bristol. All rights reserved.
# Modified under the terms of the GPL.

"""
Implements a set of ASE atoms objects as a trajectory that can be played back.
"""

from typing import Collection

from ase.atoms import Atoms

from narupatools.core.trajectory import TrajectoryPlayback


class ASETrajectoryPlayback(TrajectoryPlayback):
    """A wrapper around a set of one or more ASE `Atoms` objects representing a trajectory."""

    def __init__(self, trajectory: Collection[Atoms], playback_interval: float = 0.1, looping: bool = True):
        """
        Create a new playback of the given trajectory of ASE `Atoms` objects.

        :param trajectory: A collection of one or more ASE `Atoms` objects representing a trajectory.
        :param playback_interval: The interval between consecutive trajectory frames as it is played back, in seconds.
        :param looping: Should playback restart from the beginning when the end of the trajectory is reached.
        """
        super().__init__(playback_interval, looping)
        self._trajectory = trajectory

    def _trajectory_length(self) -> int:
        return len(self._trajectory)
