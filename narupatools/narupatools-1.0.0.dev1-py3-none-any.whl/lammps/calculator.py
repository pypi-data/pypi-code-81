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

"""ASE calculator that uses LAMMPS to calculate energies and forces, but runs dynamics in ASE."""

import importlib
from ctypes import Array, c_double
from threading import Lock
from typing import Any, Collection, List, Optional

has_lammps = importlib.util.find_spec("lammps") is not None

if not has_lammps:
    raise ImportError("narupatools.lammps requires lammps to be installed.")

import numpy as np
from ase import Atoms
from ase.calculators.calculator import Calculator, all_changes
from lammps import PyLammps  # type:ignore

from narupatools.ase.constraints.observer import ASEObserver
from narupatools.ase.units import UnitsASE
from narupatools.lammps.units import get_unit_system


class LAMMPSCalculator(Calculator):
    """
    ASE Calculator that interfaces with a given LAMMPS simulation, by updating positions and reading energy/forces.
    """
    implemented_properties = ['energy', 'forces']

    def __init__(self, lammps: PyLammps, atoms: Optional[Atoms] = None, **kwargs: Any):
        super().__init__(**kwargs)
        self._lammps = lammps
        self._lammps_lock = Lock()
        self._atoms = atoms
        self._identify_units()

        if atoms is not None:
            _position_observer = ASEObserver()
            _position_observer.on_set_positions.add_callback(self._mark_positions_as_dirty)
            atoms.constraints.append(_position_observer)
        self._positions_dirty = True

        self._energy = 0.0
        if self._atoms is None:
            self._forces = np.zeros((3, 0))
        else:
            self._forces = np.zeros((3, len(self._atoms)))

    def calculate(self, atoms: Optional[Atoms] = None,  # noqa: D102
                  properties: Collection[str] = ('energy', 'forces'),
                  system_changes: List[str] = all_changes) -> None:
        if self._atoms is not None and (atoms is self._atoms or atoms is None):
            if self._positions_dirty:
                with self._lammps_lock:
                    self._set_positions(self._atoms.get_positions())
                    self._run_system()
                    self._energy = self._extract_potential_energy()
                    self._forces = self._extract_forces()
                self._positions_dirty = False
        elif atoms is not None:
            with self._lammps_lock:
                self._set_positions(atoms.get_positions())
                self._run_system()
                self._energy = self._extract_potential_energy()
                self._forces = self._extract_forces()
            self._positions_dirty = True
        else:
            raise ValueError("No atoms provided")

        self.results['energy'] = self._energy
        self.results['forces'] = self._forces

    def _mark_positions_as_dirty(self, **kwargs: Any) -> None:
        self._positions_dirty = True

    def _identify_units(self) -> None:
        unit_system = get_unit_system(self._lammps.system.units)
        self.lammps_to_ase = unit_system >> UnitsASE
        self.ase_to_lammps = UnitsASE >> unit_system

    def _extract_potential_energy(self) -> float:
        energy_lammps: float = self._lammps.lmp.extract_compute("thermo_pe", 0, 0)
        return energy_lammps * self.lammps_to_ase.energy

    def _run_system(self) -> None:
        self._lammps.run(1)

    def _extract_forces(self) -> np.ndarray:
        forces_raw = self._lammps.lmp.gather_atoms("f", 1, 3)
        return np.array(forces_raw, dtype=float).reshape((-1, 3)) * self.lammps_to_ase.forces

    def _set_positions(self, positions: np.ndarray) -> None:
        n_atoms = self._lammps.lmp.get_natoms()
        self._lammps.lmp.scatter_atoms("x", 1, 3, _to_ctypes(positions * self.ase_to_lammps.length, n_atoms))


def _to_ctypes(array: np.ndarray, natoms: int) -> Array:
    n3 = 3 * natoms
    x = (n3 * c_double)()
    for i, f in enumerate(array.flat):
        x[i] = f  # type: ignore
    return x
