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
An ASE calculator that contains constant values.
"""

from typing import Any, Collection, List, Optional

import numpy as np
from ase.atoms import Atoms
from ase.calculators.calculator import Calculator, all_changes

from narupatools.physics.typing import ScalarArrayLike, Vector3ArrayLike


class ConstantCalculator(Calculator):
    """ASE calculator which contains constant values."""

    def __init__(self, forces: Optional[Vector3ArrayLike] = None,
                 energy: Optional[float] = None,
                 charges: Optional[ScalarArrayLike] = None,
                 **kwargs: Any):
        """Create a new `ConstantCalculator`, passing on any keyword arguments to ASE `Calculator`."""
        super().__init__(**kwargs)
        self.implemented_properties = ['forces', 'energy', 'charges']
        if forces is not None:
            self.results['forces'] = np.asfarray(forces)
        if energy is not None:
            self.results['energy'] = energy
        if charges is not None:
            self.results['charges'] = np.asfarray(charges)

    def reset(self) -> None:  # noqa: D102
        pass

    def calculate(self, atoms: Atoms = None,  # noqa: D102
                  properties: Collection[str] = ('forces', 'energy'),
                  system_changes: List[str] = all_changes) -> None:
        pass
