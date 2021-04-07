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
An ASE calculator that has a force and energy that applies to each particle separately.
"""
from abc import ABCMeta, abstractmethod
from typing import Any, Collection, List

import numpy as np
from ase import Atom
from ase.atoms import Atoms
from ase.calculators.calculator import Calculator, all_changes

from narupatools.physics.typing import Vector3


class OneBodyPotentialCalculator(Calculator, metaclass=ABCMeta):
    """Abstract base class for an ASE calculator whose potential depends on each atom individually."""

    def __init__(self, **kwargs: Any):
        """Create a new `OneBodyPotentialCalculator`, passing on any keyword arguments to ASE `Calculator`."""
        super().__init__(**kwargs)
        self.implemented_properties = ['forces', 'energy']

    def calculate(self, atoms: Atoms = None,  # noqa: D102
                  properties: Collection[str] = ('forces', 'energy'),
                  system_changes: List[str] = all_changes) -> None:
        if atoms is None:
            raise ValueError("Atoms cannot be null")
        forces = np.zeros((len(atoms), 3))
        energy = 0.0
        for i, atom in enumerate(atoms):
            energy += self.calculate_energy(atom)
            forces[i] += self.calculate_force(atom)
        self.results = {'forces': forces, 'energy': energy}

    @abstractmethod
    def calculate_energy(self, atom: Atom) -> float:
        """
        Calculate the potential energy for a given atom, in electronvolts.

        :param atom: Atom to calculate the energy for.
        :return: Potential energy in electronvolts.
        """
        raise NotImplementedError

    @abstractmethod
    def calculate_force(self, atom: Atom) -> Vector3:
        """
        Calculate the force on a given atom, in electronvolts per angstrom.

        :param atom: Atom to calculate the force for.
        :return: Force in electronvolts per angstrom.
        """
        raise NotImplementedError
