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

from typing import Mapping, Optional

from .typing import *


class Scale:

    @classmethod
    def covalent(cls,
                 scale: Optional[float] = None,
                 particle_elements: Optional[List[SerializableElement]] = None) -> SerializableDictionary:
        data: SerializableDictionary = {}
        data["type"] = "covalent"
        if scale is not None:
            data["scale"] = scale
        if particle_elements is not None:
            data["particle.elements"] = particle_elements
        return data

    @classmethod
    def secondary_structure(cls,
                            residue_secondarystructures: Optional[List[SecondaryStructure]] = None,
                            particle_residues: Optional[List[int]] = None,
                            scheme: Optional[Mapping[SecondaryStructure, float]] = None) -> SerializableDictionary:
        data: SerializableDictionary = {}
        data["type"] = "secondary structure"
        if residue_secondarystructures is not None:
            data["residue.secondarystructures"] = residue_secondarystructures
        if particle_residues is not None:
            data["particle.residues"] = particle_residues
        if scheme is not None:
            data["scheme"] = scheme
        return data

    @classmethod
    def vdw(cls,
            scale: Optional[float] = None,
            particle_elements: Optional[List[SerializableElement]] = None) -> SerializableDictionary:
        data: SerializableDictionary = {}
        data["type"] = "vdw"
        if scale is not None:
            data["scale"] = scale
        if particle_elements is not None:
            data["particle.elements"] = particle_elements
        return data
