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

"""Converter functions for interfacing with LAMMPS."""

import importlib

has_lammps = importlib.util.find_spec("lammps") is not None

if not has_lammps:
    raise ImportError("narupatools.lammps requires lammps to be installed.")

import ase.io
from ase.atoms import Atoms
from lammps import PyLammps  # type: ignore

from .calculator import LAMMPSCalculator


def atoms_from_lammps(lammps_input_filename: str, lammps_data_filename: str) -> Atoms:
    """
    Start up a LAMMPS instance from the given lammps input file, and return an ASE atoms object which reads data from
    the lammps data file to initialize the atom states, and uses the LAMMPS instance as a calculator to compute
    forces and energies.

    :param lammps_input_filename: A LAMMPS input filename (usually of the the form in.*).
    :param lammps_data_filename: A LAMMPS data filename (usually of the the form data.*).
    :return: An ASE Atoms object with a calculator running LAMMPS.
    """
    atoms: Atoms = ase.io.read(lammps_data_filename, format="lammps-data")  # type: ignore
    add_lammps_calculator_to_atoms(lammps_input_filename, atoms)
    return atoms


def add_lammps_calculator_to_atoms(lammps_input_filename: str, atoms: Atoms) -> None:
    """
    Add a calculator to a set of ASE atoms which uses the provided LAMMPS input file to generate forces and energies.
    The input file will be run immediately, but left open after all commands have been run. To recalculate the
    forces and energy, the ASE calculator will advance the system forward one step. The LAMMPS input file must therefore
    not actually do anything when advanced one step.

    :param lammps_input_filename: A LAMMPS input filename (usually of the the form in.*).
    :param atoms: An ASE atoms object to add a calculator to.
    """
    lammps = PyLammps()
    lammps.file(lammps_input_filename)
    calc = LAMMPSCalculator(lammps, atoms)
    atoms.set_calculator(calc)
