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
An ASE calculator that does nothing. Useful for unit testing.
"""

from typing import Any, Collection, List

import numpy as np
from ase.atoms import Atoms
from ase.calculators.calculator import Calculator, all_changes


class NullCalculator(Calculator):
    """Empty ASE calculator which generates zero values for forces and energies."""

    def __init__(self, **kwargs: Any):
        """Create a new `NullCalculator`, passing on any keyword arguments to ASE `Calculator`."""
        super().__init__(**kwargs)
        self.implemented_properties = ['forces', 'energy']

    def calculate(self, atoms: Atoms = None,  # noqa: D102
                  properties: Collection[str] = ('forces', 'energy'),
                  system_changes: List[str] = all_changes) -> None:
        if atoms is None:
            raise ValueError("Atoms cannot be null")
        self.results = {'forces': np.zeros((len(atoms), 3)), 'energy': 0.0}
