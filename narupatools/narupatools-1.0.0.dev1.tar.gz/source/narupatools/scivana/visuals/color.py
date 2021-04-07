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


class Color:

    @classmethod
    def element(cls,
                scheme: Optional[Mapping[SerializableElement, SerializableColor]] = None,
                particle_elements: Optional[List[SerializableElement]] = None) -> SerializableDictionary:
        data: SerializableDictionary = {}
        data["type"] = "particle element"
        if scheme is not None:
            data["scheme"] = scheme
        if particle_elements is not None:
            data["particle.elements"] = particle_elements
        return data

    @classmethod
    def particle_type(cls,
                      particle_types: Optional[List[str]] = None,
                      scheme: Optional[Mapping[str, SerializableColor]] = None) -> SerializableDictionary:
        data: SerializableDictionary = {}
        data["type"] = "particle type"
        if particle_types is not None:
            data["particle.types"] = particle_types
        if scheme is not None:
            data["scheme"] = scheme
        return data

    @classmethod
    def residue_name(cls,
                     residue_names: Optional[List[str]] = None,
                     particle_residues: Optional[List[int]] = None,
                     scheme: Optional[Mapping[str, SerializableColor]] = None) -> SerializableDictionary:
        data: SerializableDictionary = {}
        data["type"] = "residue name"
        if residue_names is not None:
            data["residue.names"] = residue_names
        if particle_residues is not None:
            data["particle.residues"] = particle_residues
        if scheme is not None:
            data["scheme"] = scheme
        return data

    @classmethod
    def secondary_structure(cls,
                            residue_secondarystructures: Optional[List[SecondaryStructure]] = None,
                            particle_residues: Optional[List[int]] = None,
                            scheme: Optional[
                                Mapping[SecondaryStructure, SerializableColor]] = None) -> SerializableDictionary:
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
    def gradient_particle_float(cls,
                                input: Optional[List[float]] = None,
                                minimum: Optional[float] = None,
                                maximum: Optional[float] = None,
                                gradient: Optional[SerializableGradient] = None) -> SerializableDictionary:
        data: SerializableDictionary = {}
        data["type"] = "float data gradient"
        if input is not None:
            data["input"] = input
        if minimum is not None:
            data["minimum"] = minimum
        if maximum is not None:
            data["maximum"] = maximum
        if gradient is not None:
            data["gradient"] = gradient
        return data

    @classmethod
    def gradient_particle_index(cls,
                                particle_count: Optional[int] = None,
                                gradient: Optional[SerializableGradient] = None) -> SerializableDictionary:
        data: SerializableDictionary = {}
        data["type"] = "particle index"
        if particle_count is not None:
            data["particle.count"] = particle_count
        if gradient is not None:
            data["gradient"] = gradient
        return data

    @classmethod
    def gradient_residue_index(cls,
                               particle_residues: Optional[List[int]] = None,
                               residue_count: Optional[int] = None,
                               gradient: Optional[SerializableGradient] = None) -> SerializableDictionary:
        data: SerializableDictionary = {}
        data["type"] = "residue index"
        if particle_residues is not None:
            data["particle.residues"] = particle_residues
        if residue_count is not None:
            data["residue.count"] = residue_count
        if gradient is not None:
            data["gradient"] = gradient
        return data

    @classmethod
    def color_pulser(cls,
                     particle_colors: Optional[List[SerializableColor]] = None,
                     highlighted_particles: Optional[List[int]] = None,
                     highlighted_color: Optional[SerializableColor] = None) -> SerializableDictionary:
        data: SerializableDictionary = {}
        data["type"] = "color pulser"
        if particle_colors is not None:
            data["particle.colors"] = particle_colors
        if highlighted_particles is not None:
            data["highlighted.particles"] = highlighted_particles
        if highlighted_color is not None:
            data["highlighted.color"] = highlighted_color
        return data

    @classmethod
    def goodsell(cls,
                 particle_elements: Optional[List[SerializableElement]] = None,
                 particle_residues: Optional[List[int]] = None,
                 residue_chains: Optional[List[int]] = None,
                 residue_names: Optional[List[str]] = None,
                 scheme: Optional[List[SerializableColor]] = None) -> SerializableDictionary:
        data: SerializableDictionary = {}
        data["type"] = "goodsell"
        if particle_elements is not None:
            data["particle.elements"] = particle_elements
        if particle_residues is not None:
            data["particle.residues"] = particle_residues
        if residue_chains is not None:
            data["residue.chains"] = residue_chains
        if residue_names is not None:
            data["residue.names"] = residue_names
        if scheme is not None:
            data["scheme"] = scheme
        return data
