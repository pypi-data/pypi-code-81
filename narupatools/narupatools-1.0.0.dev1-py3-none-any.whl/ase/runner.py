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
Runner that uses ASE to simulate a system.
"""

from __future__ import annotations

from typing import Optional, TypeVar

from MDAnalysis import Universe
from ase.atoms import Atoms
from ase.md import Langevin
from ase.md.md import MolecularDynamics

from narupatools.core.units import UnitsNarupa
from .calculators.null_calculator import NullCalculator
from .dynamics import ASEDynamics
from .system import ASESystem
from .units import UnitsASE

NarupaToASE = UnitsNarupa >> UnitsASE


def from_ase_atoms(atoms: Atoms, universe: Optional[Universe] = None) -> ASESystem:
    """
    Create a representation of an ASE atoms object that can be broadcast through a Narupa session.

    If the Atoms object does not have a calculator, a null calculator will be added.

    :param atoms: ASE atoms object.
    :param universe: Optional MDAnalysis universe with additional system information.
    :return: A representation of the system which can be broadcast through a Narupa session.
    """
    if atoms.get_calculator() is None:
        atoms.set_calculator(NullCalculator())
    return ASESystem(atoms, universe)


TIntegrator = TypeVar('TIntegrator', bound=MolecularDynamics)


def from_ase_dynamics(dynamics: TIntegrator, universe: Optional[Universe] = None) -> ASEDynamics[TIntegrator]:
    """
    Create a representation of an ASE dynamics object that can be broadcast through a Narupa session.

    This object implements the SimulationDynamics API, and hence can be played at a specific playback rate. It also
    provides callbacks for when the simulation advances a step or is reset.

    :param dynamics: Any ASE dynamics derived from MolecularDynamics.
    :param universe: Optional MDAnalysis universe with additional system information.
    :return: An ASEDynamics object which wraps the provided dynamics in a Narupa friendly way.
    """
    return ASEDynamics(dynamics, universe)


def from_ase_atoms_langevin(atoms: Atoms,
                            *, universe: Optional[Universe] = None,
                            friction: float = 1e-2,
                            temperature: float = 300,
                            timestep: float = 1) -> ASEDynamics[Langevin]:
    """
    Create a representation of a Langevin integrator running on the provided ASE atoms object, that can be broadcast
    through a Narupa session.

    :param atoms: An ASE atoms object to simulate.
    :param universe: Optional MDAnalysis universe with additional system information.
    :param friction: Friction of the Langevin integrator in inverse picoseconds.
    :param temperature: Temperature of the Langevin integrator in kelvin.
    :param timestep: Timestep of the Langevin integrator in picoseconds.
    :return: An ASEDynamics object which wraps a Langevin integrator running on the specified system.
    """
    if atoms.get_calculator() is None:
        atoms.set_calculator(NullCalculator())
    dynamics = Langevin(atoms,
                        timestep=timestep * NarupaToASE.time,
                        temperature_K=temperature,
                        friction=friction / NarupaToASE.time,
                        fixcm=False)
    return from_ase_dynamics(dynamics, universe)
