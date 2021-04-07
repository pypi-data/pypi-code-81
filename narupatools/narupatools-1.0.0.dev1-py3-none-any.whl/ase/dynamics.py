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
Simulation dynamics implementation using ASE.
"""
from typing import Generic, Optional, TypeVar

from MDAnalysis import Universe
from ase.atoms import Atoms
from ase.md.md import MolecularDynamics
from infinite_sets import InfiniteSet
from narupa.trajectory import FrameData

from narupatools.ase.imd_feature import ASEImdProvider
from narupatools.core.dynamics import SimulationDynamics
from narupatools.core.servable import Servable
from narupatools.core.session import NarupaSession
from narupatools.core.units import UnitsNarupa
from .converter import ase_atoms_to_frame
from .units import UnitsASE
from ..mdanalysis import mdanalysis_universe_to_frame

TIntegrator = TypeVar('TIntegrator', bound=MolecularDynamics)

NarupaToASE = UnitsNarupa >> UnitsASE
ASEToNarupa = UnitsASE >> UnitsNarupa


class ASEDynamics(Generic[TIntegrator], SimulationDynamics, Servable):
    """
    Wrapper around an ASE `MolecularDynamics` object through the `SimulationDynamics` interface.

    This allows the simulation to be run at a set playback rate, as well as exposing standard properties such as
    time step and elapsed steps.
    """

    imd: Optional[ASEImdProvider]

    def __init__(self, dynamics: TIntegrator, universe: Optional[Universe] = None, *, playback_interval: float = 0.0):
        """
        Create a `SimulationDynamics` wrapper around an ASE `MolecularDynamics` object.

        :param dynamics: ASE `MolecularDynamics` object to be simulated.
        :param universe: Optional MDAnalysis universe to provide additional topology.
        :param playback_interval: Time to wait between steps in seconds. Defaults to 0.0 (run as fast as possible).
        """
        super().__init__(playback_interval)
        self._dynamics = dynamics
        self._universe = universe
        self._initial_positions = self.atoms.get_positions()
        self._initial_momenta = self.atoms.get_momenta()
        self._initial_box = self.atoms.get_cell()

    def start_being_served(self, server: NarupaSession) -> None:  # noqa: D102
        self.imd = ASEImdProvider.add_to_dynamics(self, server)

    def end_being_served(self, server: NarupaSession) -> None:  # noqa: D102
        if self.imd is not None:
            self.imd.close()
        self.imd = None

    @property
    def atoms(self) -> Atoms:
        """Get the wrapped ASE `Atoms` object. Direct modification of this may have side effects."""
        return self.molecular_dynamics.atoms

    @property
    def molecular_dynamics(self) -> TIntegrator:
        """Get the wrapped ASE `MolecularDynamics`` object. Direct modification of this may have side effects."""
        return self._dynamics

    def _step_internal(self) -> None:
        self._dynamics.run(1)

    def _reset_internal(self) -> None:
        self.atoms.set_positions(self._initial_positions)
        self.atoms.set_momenta(self._initial_momenta)
        self.atoms.set_cell(self._initial_box)

    @property
    def time_step(self) -> float:  # noqa: D102
        return self.molecular_dynamics.dt * ASEToNarupa.time

    @time_step.setter
    def time_step(self, value: float) -> None:
        self.molecular_dynamics.dt = value * NarupaToASE.time

    def _get_frame(self, fields: InfiniteSet[str]) -> FrameData:
        frame = FrameData()
        if self._universe:
            ase_atoms_to_frame(self.atoms, fields=fields, frame=frame)
            added_fields = set(frame.arrays.keys()) | set(frame.values.keys())
            mdanalysis_universe_to_frame(self._universe, fields=fields - added_fields, frame=frame)
            return frame
        else:
            ase_atoms_to_frame(self.atoms, fields=fields, frame=frame)
        return frame
