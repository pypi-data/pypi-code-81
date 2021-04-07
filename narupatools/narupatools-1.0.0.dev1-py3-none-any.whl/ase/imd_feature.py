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
Implementation of IMD for an ASE dynamics simulation as dynamics restraints added and removed from the ASE atoms object.
"""

from __future__ import annotations

from typing import Any, Dict, Mapping, Protocol

import numpy as np
from ase import Atoms
from narupa.imd import ParticleInteraction

import narupatools.ase.dynamics as dynamics
from narupatools.ase.constraints.imd_constraint import InteractionConstraint
from narupatools.core.dynamics import SimulationDynamics
from narupatools.core.event import Event, EventListener
from narupatools.core.session import NarupaSession


class OnStartInteractionCallback(Protocol):
    """Callback for when an interaction is first applied to the system."""

    def __call__(self, *, key: str, interaction: ParticleInteraction) -> None:
        """
        Called when an interaction is first applied to the system.

        :param key: Full shared state key of the interaction.
        :param interaction: Interaction object sent by client.
        """
        ...


class OnEndInteractionCallback(Protocol):
    """Callback for when an interaction is removed from the system."""

    def __call__(self, *, key: str, work_done: float, duration: float) -> None:
        """
        Called when an interaction is removed from the system.

        :param key: Full shared state key of the interaction.
        :param work_done: Total work done by interaction in kilojoules per mole.
        :param duration: Duration of interaction in simulation time in picoseconds.
        """
        ...


class InteractionsSource(Protocol):
    """
    General protocol for an object which can provide interactions.

    Exists to generalize Narupa's ImdStateWrapper so interactions can be provided from other sources.
    """

    @property
    def active_interactions(self) -> Mapping[str, ParticleInteraction]:
        """Key-indexed set of interactions that should be applied to the system."""
        ...


class ASEImdProvider:
    """Interactive Molecular Dynamics manager for ASE dynamics, which dynamically adds and removes constraints."""

    _current_interactions: Dict[str, InteractionConstraint]
    _on_start_interaction: Event[OnStartInteractionCallback]
    _on_end_interaction: Event[OnEndInteractionCallback]

    def __init__(self,
                 imd_source: InteractionsSource,
                 atoms: Atoms,
                 dynamics: SimulationDynamics):
        """
        Create a new ASEImdProvider. Generally should be constructed using ASEImdProvider.add_to_dynamics.

        :param imd_source: An InteractionSource which provides access to the current dictionary of interactions.
        :param atoms: An ASE atoms object to add and remove constraints from.
        :param dynamics: A SimulationDynamics object which notifies the ASEImdProvider when dynamics steps occur.
        """
        self._imd_source = imd_source
        self._atoms = atoms
        self._dynamics = dynamics
        self._dynamics.on_pre_step.add_callback(self._on_pre_step)
        self._dynamics.on_post_step.add_callback(self._on_post_step)
        self._dynamics.on_reset.add_callback(self._on_reset)

        self._current_interactions = {}

        self._on_start_interaction = Event()
        self._on_end_interaction = Event()

        self._has_reset = True

    @property
    def current_interactions(self) -> Mapping[str, InteractionConstraint]:
        """Key-index set of interaction constraints currently applied to the system."""
        return self._current_interactions

    @classmethod
    def add_to_dynamics(cls, dynamics: dynamics.ASEDynamics, session: NarupaSession) -> ASEImdProvider:
        """
        Create an ASEImdProvider that watches the given dynamics and applies IMD forces obtained from the given
        session.

        :param dynamics: ASE dynamics object to apply IMD to.
        :param session: Session which will provide set of interactions through shared state.
        """
        source = session.server.imd
        atoms = dynamics.atoms
        return ASEImdProvider(source, atoms, dynamics)

    @property
    def on_start_interaction(self) -> EventListener[OnStartInteractionCallback]:
        """Event triggered when an interaction is first applied to the system."""
        return self._on_start_interaction

    @property
    def on_end_interaction(self) -> EventListener[OnEndInteractionCallback]:
        """Event triggered when an interaction is removed from the system."""
        return self._on_end_interaction

    @property
    def total_work(self) -> float:
        """
        Total work performed by all active interactions, in kilojoules per mole.

        This does not include interactions which have now finished.
        """
        total_work = [interaction.total_work for interaction in self.current_interactions.values()]
        return np.array(total_work, dtype=float).sum()  # type:ignore

    @property
    def work_last_step(self) -> float:
        """Total work performed last step by all active interactions, in kilojoules per mole."""
        work_last_step = [interaction.work_last_step for interaction in self.current_interactions.values()]
        return np.array(work_last_step, dtype=float).sum()  # type:ignore

    @property
    def potential_energy(self) -> float:
        """Total potential energy from all active interactions, in kilojoules per mole."""
        potential_energy = [interaction.potential_energy for interaction in self.current_interactions.values()]
        return np.array(potential_energy, dtype=float).sum()  # type:ignore

    @property
    def imd_forces(self) -> np.ndarray:
        """
        Total interactive forces from all active interactions, in kilojoules per mole per nanometer.

        This returns a (N, 3) NumPy array, where N is the number of atoms in the system.
        """
        forces = np.zeros((3, len(self._atoms)))
        for interaction in self._current_interactions.values():
            forces[interaction.particle_indices] += interaction.forces
        return forces

    def close(self) -> None:
        """Remove this ASEImdProvider from the dynamics it was applied to."""
        self._dynamics.on_pre_step.remove_callback(self._on_pre_step)
        self._dynamics.on_post_step.remove_callback(self._on_post_step)
        self._dynamics.on_reset.remove_callback(self._on_reset)

    def _on_pre_step(self, **kwargs: Any) -> None:
        """
        Called before each dynamics step.

        The interactions and corresponding constraints are updated based on the interactions listed by the interaction
        source provided on creation.
        """
        interactions = self._imd_source.active_interactions
        for key in list(self.current_interactions.keys()):
            if self._has_reset or key not in interactions.keys():
                constraint = self._remove_interaction(key)
                end_time = self._dynamics.total_time
                duration = end_time - constraint.start_time
                self._on_end_interaction.invoke(key=key, work_done=constraint.total_work, duration=duration)
            self._has_reset = False

        for key in interactions.keys():
            if key not in self.current_interactions.keys():
                self._add_interaction(key, interactions[key])
                self._on_start_interaction.invoke(key=key, interaction=interactions[key])
            else:
                self.current_interactions[key].interaction = interactions[key]

        for interaction in self.current_interactions.values():
            interaction.on_pre_step(self._atoms)

    def _on_post_step(self, **kwargs: Any) -> None:
        for interaction in self.current_interactions.values():
            interaction.on_post_step(self._atoms)

    def _add_interaction(self, key: str, interaction: ParticleInteraction) -> None:
        constraint = InteractionConstraint(key, interaction, self._dynamics.total_time)
        self._current_interactions[key] = constraint
        self._atoms.constraints.append(constraint)

    def _remove_interaction(self, key: str) -> InteractionConstraint:
        constraint = self.current_interactions[key]
        del self._current_interactions[key]
        self._atoms.constraints.remove(constraint)
        return constraint

    def _on_reset(self, **kwargs: Any) -> None:
        self._has_reset = True
