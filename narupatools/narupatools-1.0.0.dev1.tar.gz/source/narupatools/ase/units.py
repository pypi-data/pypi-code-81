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

"""Unit conversions for ASE."""

from narupatools.core.units import (UnitSystem, amu, angstrom, electronvolt,
                                    elementary_charge, kelvin)

UnitsASE = UnitSystem(length=angstrom,
                      mass=amu,
                      temperature=kelvin,
                      time=angstrom * (amu / electronvolt) ** 0.5,
                      charge=elementary_charge)
