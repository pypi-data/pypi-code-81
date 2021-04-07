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
An ASE constraint that applies an interactive force.
"""

from typing import Optional
from typing import Sequence

import numpy as np
from ase.atoms import Atoms
from narupa.imd import ParticleInteraction

from narupatools.ase.units import UnitsASE
from narupatools.core import UnitsNarupa
from narupatools.imd import calculate_imd_force
from narupatools.physics.typing import Vector3Array
from .constraint import ASEEnergyConstraint
from .constraint import ASEMomentaConstraint

NarupaToASE = UnitsNarupa >> UnitsASE
ASEToNarupa = UnitsASE >> UnitsNarupa


class InteractionConstraint(ASEEnergyConstraint, ASEMomentaConstraint):
    """An ASE constraint that applies an iMD force."""

    def __init__(self, key: str, interaction: ParticleInteraction, start_time: float):
        """
        Create an ASE constraint that will apply an interactive force.

        :param key: Unique key to identify this interaction.
        :param interaction: Initial parameters of the interaction.
        :param start_time: Start time of interaction in simulation time in picoseconds
        """
        self.key: str = key
        self._total_work: float = 0.0
        self._last_step_work: Optional[float] = None
        self.interaction: ParticleInteraction = interaction
        self._previous_positions: Vector3Array = np.zeros(0)
        self._previous_forces: Vector3Array = np.zeros(0)
        self._start_time: float = start_time

        self._cached_atoms: Optional[Atoms] = None
        self._cached_energy: float = 0.0
        self._cached_forces: Vector3Array = np.zeros(0)
        self._cache_valid: bool = False

    def _invalidate_cache(self) -> None:
        self._cached_atoms = None
        self._cached_energy = 0.0
        self._cached_forces = np.zeros(0)
        self._cache_valid = False

    def _ensure_cache_is_valid(self, atoms: Atoms) -> None:
        if self._cache_valid and self._cached_atoms is atoms:
            return
        self._recalculate(atoms)

    @property
    def indices(self) -> Sequence[int]:
        """List of indices affected by this constraint."""
        return self.interaction.particles  # type: ignore

    @property
    def start_time(self) -> float:
        """Start time of the interaction in picoseconds."""
        return self._start_time

    @property
    def total_work(self) -> float:
        """Total work performed by interaction in kilojoules per mole."""
        return self._total_work

    @property
    def work_last_step(self) -> float:
        """Work performed last step in kilojoules per mole."""
        if self._last_step_work is None:
            raise AttributeError("No dynamics steps have occurred yet.")
        return self._last_step_work

    @property
    def interaction(self) -> ParticleInteraction:
        """Current parameters of the interaction."""
        return self._interaction

    @interaction.setter
    def interaction(self, value: ParticleInteraction) -> None:
        self._interaction = value

    @property
    def potential_energy(self) -> float:
        """
        Potential energy of the interaction, in kilojoules per mole.

        :raises ValueError: Potential energy has not been calculated yet, or positions have been changed since it was
        last calculated.
        """
        if not self._cache_valid:
            raise ValueError("Potential energy has not been calculated at this point.")
        return self._cached_energy

    @property
    def forces(self) -> np.ndarray:
        """
        Forces that will be applied by the interaction, in kilojoules per mole per nanometer.

        This is a (N, 3) NumPy array, where N is the number of particles affected by this interaction.

        :raises ValueError: Forces have not been calculated yet, or positions have been changed since they were
        last calculated.
        """
        if not self._cache_valid:
            raise ValueError("Potential energy has not been calculated at this point.")
        return self._cached_forces

    @property
    def particle_indices(self) -> np.ndarray:
        """List of indices affected by this interaction."""
        return self._interaction.particles

    def on_pre_step(self, atoms: Atoms) -> None:
        """Perform any tasks necessary before a dynamics step."""
        self._ensure_cache_is_valid(atoms)
        self._previous_positions = atoms.positions[self._interaction.particles]
        self._previous_forces = self.forces

    def on_post_step(self, atoms: Atoms) -> None:
        """Perform any tasks necessary after a dynamics step."""
        self._ensure_cache_is_valid(atoms)
        _current_positions = atoms.positions[self._interaction.particles]

        work_this_step = 0.0

        for i in range(len(self._interaction.particles)):
            # Use trapezoidal rule to calculate single step of integral F.dS
            F = 0.5 * (self._previous_forces[i] + self.forces[i])
            dS = _current_positions[i] - self._previous_positions[i]
            work_this_step += np.dot(F, dS)

        # work this step is in eV, store it in KJ/MOL
        work_this_step *= ASEToNarupa.energy

        self._last_step_work = work_this_step
        self._total_work += work_this_step

        self._previous_positions = _current_positions

    def adjust_positions(self, atoms: Atoms, positions: np.ndarray) -> None:  # noqa: D102
        # Assume all interactions depend on positions
        if atoms is self._cached_atoms:
            self._invalidate_cache()

    def adjust_momenta(self, atoms: Atoms, momenta: np.ndarray) -> None:  # noqa: D102
        # Assume no interactions depend on velocities
        # When they do, this should conditionally invalidate the cache
        pass

    def adjust_forces(self, atoms: Atoms, forces: np.ndarray) -> None:  # noqa: D102
        self._ensure_cache_is_valid(atoms)
        forces[self._interaction.particles] += self.forces

    def adjust_potential_energy(self, atoms: Atoms) -> float:  # noqa: D102
        self._ensure_cache_is_valid(atoms)
        return self.potential_energy

    def _recalculate(self, atoms: Atoms) -> None:
        positions_nm = atoms.positions[self._interaction.particles] * ASEToNarupa.length
        masses_amu = atoms.get_masses()[self._interaction.particles] * ASEToNarupa.mass

        kwargs = {'position': self._interaction.position,
                  **self._interaction.properties}

        forces_kjmol, energy_kjmol = calculate_imd_force(positions=positions_nm,
                                                         masses=masses_amu,
                                                         interaction_type=self._interaction.interaction_type,
                                                         interaction_scale=self._interaction.scale,
                                                         **kwargs)

        energy_ev = energy_kjmol * NarupaToASE.energy
        forces_ev = forces_kjmol * NarupaToASE.force

        self._cached_atoms = atoms
        self._cached_forces = forces_ev
        self._cached_energy = energy_ev
        self._cache_valid = True
