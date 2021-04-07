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
Simulation dynamics implementation using OpenMM. Currently does not support iMD.
"""

from io import BytesIO

from infinite_sets import InfiniteSet
from narupa.trajectory import FrameData
from simtk.openmm.app import Simulation

from narupatools.core.dynamics import SimulationDynamics
from narupatools.openmm.converter import (openmm_context_to_frame,
                                          openmm_topology_to_frame)


class OpenMMDynamics(SimulationDynamics):
    """
    Wrapper around an OpenMM simulation that runs it directly step by step, without using ASE.

    """

    def _step_internal(self) -> None:
        self._simulation.step(steps=1)

    def _reset_internal(self) -> None:
        with BytesIO(self._checkpoint) as bytesio:
            self._simulation.loadCheckpoint(bytesio)

    def _get_frame(self, fields: InfiniteSet[str]) -> FrameData:
        frame = FrameData()
        openmm_context_to_frame(self._simulation.context, fields=fields, frame=frame)
        openmm_topology_to_frame(self._simulation.topology, fields=fields, frame=frame)
        return frame

    def __init__(self, simulation: Simulation, playback_interval: float = 0.0):
        super().__init__(playback_interval=playback_interval)
        self._simulation = simulation
        with BytesIO() as bytesio:
            self._simulation.saveCheckpoint(bytesio)
            self._checkpoint = bytesio.getvalue()

    @property
    def time_step(self) -> float:  # noqa: D102
        return self._simulation.integrator.getStepSize()._value
