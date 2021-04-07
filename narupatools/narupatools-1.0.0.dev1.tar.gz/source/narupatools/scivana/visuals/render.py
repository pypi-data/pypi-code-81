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

from typing import Optional

from .typing import *


class Render:

    @classmethod
    def ball_and_stick(cls,
                       particle_scale: Optional[float] = None,
                       bond_scale: Optional[float] = None,
                       particle_material: Optional[SerializableMaterial] = None,
                       bond_material: Optional[SerializableMaterial] = None,
                       particle_mesh: Optional[SerializableMesh] = None,
                       bond_mesh: Optional[SerializableMesh] = None,
                       particle_positions: Optional[List[Vector3]] = None,
                       particle_colors: Optional[List[SerializableColor]] = None,
                       particle_scales: Optional[List[float]] = None,
                       scale: Optional[float] = None,
                       particle_sizes: Optional[List[Vector3]] = None,
                       particle_rotations: Optional[List[Quaternion]] = None,
                       color: Optional[SerializableColor] = None,
                       mesh: Optional[SerializableMesh] = None,
                       material: Optional[SerializableMaterial] = None,
                       opacity: Optional[float] = None,
                       bond_pairs: Optional[List[BondPair]] = None,
                       edge_sharpness: Optional[float] = None) -> SerializableDictionary:
        data: SerializableDictionary = {}
        data["type"] = "ball and stick"
        if particle_scale is not None:
            data["particle.scale"] = particle_scale
        if bond_scale is not None:
            data["bond.scale"] = bond_scale
        if particle_material is not None:
            data["particle.material"] = particle_material
        if bond_material is not None:
            data["bond.material"] = bond_material
        if particle_mesh is not None:
            data["particle.mesh"] = particle_mesh
        if bond_mesh is not None:
            data["bond.mesh"] = bond_mesh
        if particle_positions is not None:
            data["particle.positions"] = particle_positions
        if particle_colors is not None:
            data["particle.colors"] = particle_colors
        if particle_scales is not None:
            data["particle.scales"] = particle_scales
        if scale is not None:
            data["scale"] = scale
        if particle_sizes is not None:
            data["particle.sizes"] = particle_sizes
        if particle_rotations is not None:
            data["particle.rotations"] = particle_rotations
        if color is not None:
            data["color"] = color
        if mesh is not None:
            data["mesh"] = mesh
        if material is not None:
            data["material"] = material
        if opacity is not None:
            data["opacity"] = opacity
        if bond_pairs is not None:
            data["bond.pairs"] = bond_pairs
        if edge_sharpness is not None:
            data["edge.sharpness"] = edge_sharpness
        return data

    @classmethod
    def cycles(cls,
               scale: Optional[float] = None,
               cycle_scale: Optional[float] = None,
               cycles: Optional[List[List[int]]] = None,
               particle_positions: Optional[List[Vector3]] = None,
               particle_colors: Optional[List[SerializableColor]] = None,
               particle_scales: Optional[List[float]] = None,
               particle_sizes: Optional[List[Vector3]] = None,
               particle_rotations: Optional[List[Quaternion]] = None,
               color: Optional[SerializableColor] = None,
               mesh: Optional[SerializableMesh] = None,
               material: Optional[SerializableMaterial] = None,
               opacity: Optional[float] = None,
               bond_pairs: Optional[List[BondPair]] = None,
               bond_scale: Optional[float] = None,
               edge_sharpness: Optional[float] = None) -> SerializableDictionary:
        data: SerializableDictionary = {}
        data["type"] = "cycles"
        if scale is not None:
            data["scale"] = scale
        if cycle_scale is not None:
            data["cycle.scale"] = cycle_scale
        if cycles is not None:
            data["cycles"] = cycles
        if particle_positions is not None:
            data["particle.positions"] = particle_positions
        if particle_colors is not None:
            data["particle.colors"] = particle_colors
        if particle_scales is not None:
            data["particle.scales"] = particle_scales
        if particle_sizes is not None:
            data["particle.sizes"] = particle_sizes
        if particle_rotations is not None:
            data["particle.rotations"] = particle_rotations
        if color is not None:
            data["color"] = color
        if mesh is not None:
            data["mesh"] = mesh
        if material is not None:
            data["material"] = material
        if opacity is not None:
            data["opacity"] = opacity
        if bond_pairs is not None:
            data["bond.pairs"] = bond_pairs
        if bond_scale is not None:
            data["bond.scale"] = bond_scale
        if edge_sharpness is not None:
            data["edge.sharpness"] = edge_sharpness
        return data

    @classmethod
    def ribbon(cls,
               particle_positions: Optional[List[Vector3]] = None,
               sequences_particles: Optional[List[List[int]]] = None,
               particle_colors: Optional[List[SerializableColor]] = None,
               particle_scales: Optional[List[float]] = None,
               particle_widths: Optional[List[float]] = None,
               scale: Optional[float] = None,
               width: Optional[float] = None,
               speed: Optional[float] = None,
               input: Optional[List[SerializableColor]] = None,
               particle_sizes: Optional[List[Vector3]] = None,
               particle_rotations: Optional[List[Quaternion]] = None,
               color: Optional[SerializableColor] = None,
               mesh: Optional[SerializableMesh] = None,
               material: Optional[SerializableMaterial] = None,
               opacity: Optional[float] = None,
               spline_segments: Optional[List[SplineSegment]] = None,
               edge_sharpness: Optional[float] = None) -> SerializableDictionary:
        data: SerializableDictionary = {}
        data["type"] = "elliptic spline"
        if particle_positions is not None:
            data["particle.positions"] = particle_positions
        if sequences_particles is not None:
            data["sequences.particles"] = sequences_particles
        if particle_colors is not None:
            data["particle.colors"] = particle_colors
        if particle_scales is not None:
            data["particle.scales"] = particle_scales
        if particle_widths is not None:
            data["particle.widths"] = particle_widths
        if scale is not None:
            data["scale"] = scale
        if width is not None:
            data["width"] = width
        if speed is not None:
            data["speed"] = speed
        if input is not None:
            data["input"] = input
        if particle_sizes is not None:
            data["particle.sizes"] = particle_sizes
        if particle_rotations is not None:
            data["particle.rotations"] = particle_rotations
        if color is not None:
            data["color"] = color
        if mesh is not None:
            data["mesh"] = mesh
        if material is not None:
            data["material"] = material
        if opacity is not None:
            data["opacity"] = opacity
        if spline_segments is not None:
            data["spline_segments"] = spline_segments
        if edge_sharpness is not None:
            data["edge.sharpness"] = edge_sharpness
        return data

    @classmethod
    def geometric_spline(cls,
                         particle_positions: Optional[List[Vector3]] = None,
                         sequences_particles: Optional[List[List[int]]] = None,
                         particle_colors: Optional[List[SerializableColor]] = None,
                         particle_widths: Optional[List[float]] = None,
                         scale: Optional[float] = None,
                         width: Optional[float] = None,
                         particle_scales: Optional[List[float]] = None,
                         particle_sizes: Optional[List[Vector3]] = None,
                         particle_rotations: Optional[List[Quaternion]] = None,
                         color: Optional[SerializableColor] = None,
                         mesh: Optional[SerializableMesh] = None,
                         material: Optional[SerializableMaterial] = None,
                         opacity: Optional[float] = None,
                         bond_pairs: Optional[List[BondPair]] = None,
                         bond_scale: Optional[float] = None,
                         edge_sharpness: Optional[float] = None,
                         cycles: Optional[List[List[int]]] = None) -> SerializableDictionary:
        data: SerializableDictionary = {}
        data["type"] = "tetrahedral spline"
        if particle_positions is not None:
            data["particle.positions"] = particle_positions
        if sequences_particles is not None:
            data["sequences.particles"] = sequences_particles
        if particle_colors is not None:
            data["particle.colors"] = particle_colors
        if particle_widths is not None:
            data["particle.widths"] = particle_widths
        if scale is not None:
            data["scale"] = scale
        if width is not None:
            data["width"] = width
        if particle_scales is not None:
            data["particle.scales"] = particle_scales
        if particle_sizes is not None:
            data["particle.sizes"] = particle_sizes
        if particle_rotations is not None:
            data["particle.rotations"] = particle_rotations
        if color is not None:
            data["color"] = color
        if mesh is not None:
            data["mesh"] = mesh
        if material is not None:
            data["material"] = material
        if opacity is not None:
            data["opacity"] = opacity
        if bond_pairs is not None:
            data["bond.pairs"] = bond_pairs
        if bond_scale is not None:
            data["bond.scale"] = bond_scale
        if edge_sharpness is not None:
            data["edge.sharpness"] = edge_sharpness
        if cycles is not None:
            data["cycles"] = cycles
        return data

    @classmethod
    def goodsell(cls,
                 particle_residues: Optional[List[int]] = None,
                 particle_positions: Optional[List[Vector3]] = None,
                 particle_colors: Optional[List[SerializableColor]] = None,
                 particle_scales: Optional[List[float]] = None,
                 scale: Optional[float] = None,
                 particle_sizes: Optional[List[Vector3]] = None,
                 particle_rotations: Optional[List[Quaternion]] = None,
                 color: Optional[SerializableColor] = None,
                 mesh: Optional[SerializableMesh] = None,
                 material: Optional[SerializableMaterial] = None,
                 opacity: Optional[float] = None) -> SerializableDictionary:
        data: SerializableDictionary = {}
        data["type"] = "goodsell"
        if particle_residues is not None:
            data["particle.residues"] = particle_residues
        if particle_positions is not None:
            data["particle.positions"] = particle_positions
        if particle_colors is not None:
            data["particle.colors"] = particle_colors
        if particle_scales is not None:
            data["particle.scales"] = particle_scales
        if scale is not None:
            data["scale"] = scale
        if particle_sizes is not None:
            data["particle.sizes"] = particle_sizes
        if particle_rotations is not None:
            data["particle.rotations"] = particle_rotations
        if color is not None:
            data["color"] = color
        if mesh is not None:
            data["mesh"] = mesh
        if material is not None:
            data["material"] = material
        if opacity is not None:
            data["opacity"] = opacity
        return data

    @classmethod
    def hydrogen_caps(cls,
                      acceptor_scale: Optional[float] = None,
                      donor_scale: Optional[float] = None,
                      acceptor_color: Optional[SerializableColor] = None,
                      donor_color: Optional[SerializableColor] = None,
                      particle_positions: Optional[List[Vector3]] = None,
                      particle_elements: Optional[List[SerializableElement]] = None,
                      bond_pairs: Optional[List[BondPair]] = None,
                      particle_colors: Optional[List[SerializableColor]] = None,
                      particle_scales: Optional[List[float]] = None,
                      scale: Optional[float] = None,
                      particle_sizes: Optional[List[Vector3]] = None,
                      particle_rotations: Optional[List[Quaternion]] = None,
                      color: Optional[SerializableColor] = None,
                      mesh: Optional[SerializableMesh] = None,
                      material: Optional[SerializableMaterial] = None,
                      opacity: Optional[float] = None) -> SerializableDictionary:
        data: SerializableDictionary = {}
        data["type"] = "hydrogen cap"
        if acceptor_scale is not None:
            data["acceptor.scale"] = acceptor_scale
        if donor_scale is not None:
            data["donor.scale"] = donor_scale
        if acceptor_color is not None:
            data["acceptor.color"] = acceptor_color
        if donor_color is not None:
            data["donor.color"] = donor_color
        if particle_positions is not None:
            data["particle.positions"] = particle_positions
        if particle_elements is not None:
            data["particle.elements"] = particle_elements
        if bond_pairs is not None:
            data["bond.pairs"] = bond_pairs
        if particle_colors is not None:
            data["particle.colors"] = particle_colors
        if particle_scales is not None:
            data["particle.scales"] = particle_scales
        if scale is not None:
            data["scale"] = scale
        if particle_sizes is not None:
            data["particle.sizes"] = particle_sizes
        if particle_rotations is not None:
            data["particle.rotations"] = particle_rotations
        if color is not None:
            data["color"] = color
        if mesh is not None:
            data["mesh"] = mesh
        if material is not None:
            data["material"] = material
        if opacity is not None:
            data["opacity"] = opacity
        return data

    @classmethod
    def hyperballs(cls,
                   scale: Optional[float] = None,
                   particle_positions: Optional[List[Vector3]] = None,
                   particle_colors: Optional[List[SerializableColor]] = None,
                   particle_scales: Optional[List[float]] = None,
                   particle_sizes: Optional[List[Vector3]] = None,
                   particle_rotations: Optional[List[Quaternion]] = None,
                   color: Optional[SerializableColor] = None,
                   mesh: Optional[SerializableMesh] = None,
                   material: Optional[SerializableMaterial] = None,
                   opacity: Optional[float] = None,
                   bond_pairs: Optional[List[BondPair]] = None,
                   bond_scale: Optional[float] = None,
                   edge_sharpness: Optional[float] = None) -> SerializableDictionary:
        data: SerializableDictionary = {}
        data["type"] = "hyperballs"
        if scale is not None:
            data["scale"] = scale
        if particle_positions is not None:
            data["particle.positions"] = particle_positions
        if particle_colors is not None:
            data["particle.colors"] = particle_colors
        if particle_scales is not None:
            data["particle.scales"] = particle_scales
        if particle_sizes is not None:
            data["particle.sizes"] = particle_sizes
        if particle_rotations is not None:
            data["particle.rotations"] = particle_rotations
        if color is not None:
            data["color"] = color
        if mesh is not None:
            data["mesh"] = mesh
        if material is not None:
            data["material"] = material
        if opacity is not None:
            data["opacity"] = opacity
        if bond_pairs is not None:
            data["bond.pairs"] = bond_pairs
        if bond_scale is not None:
            data["bond.scale"] = bond_scale
        if edge_sharpness is not None:
            data["edge.sharpness"] = edge_sharpness
        return data

    @classmethod
    def liquorice(cls,
                  scale: Optional[float] = None,
                  bond_material: Optional[SerializableMaterial] = None,
                  particle_positions: Optional[List[Vector3]] = None,
                  particle_colors: Optional[List[SerializableColor]] = None,
                  particle_scales: Optional[List[float]] = None,
                  particle_sizes: Optional[List[Vector3]] = None,
                  particle_rotations: Optional[List[Quaternion]] = None,
                  color: Optional[SerializableColor] = None,
                  mesh: Optional[SerializableMesh] = None,
                  material: Optional[SerializableMaterial] = None,
                  opacity: Optional[float] = None,
                  bond_pairs: Optional[List[BondPair]] = None,
                  bond_scale: Optional[float] = None,
                  edge_sharpness: Optional[float] = None) -> SerializableDictionary:
        data: SerializableDictionary = {}
        data["type"] = "liquorice"
        if scale is not None:
            data["scale"] = scale
        if bond_material is not None:
            data["bond.material"] = bond_material
        if particle_positions is not None:
            data["particle.positions"] = particle_positions
        if particle_colors is not None:
            data["particle.colors"] = particle_colors
        if particle_scales is not None:
            data["particle.scales"] = particle_scales
        if particle_sizes is not None:
            data["particle.sizes"] = particle_sizes
        if particle_rotations is not None:
            data["particle.rotations"] = particle_rotations
        if color is not None:
            data["color"] = color
        if mesh is not None:
            data["mesh"] = mesh
        if material is not None:
            data["material"] = material
        if opacity is not None:
            data["opacity"] = opacity
        if bond_pairs is not None:
            data["bond.pairs"] = bond_pairs
        if bond_scale is not None:
            data["bond.scale"] = bond_scale
        if edge_sharpness is not None:
            data["edge.sharpness"] = edge_sharpness
        return data

    @classmethod
    def noodles(cls,
                scale: Optional[float] = None,
                particle_positions: Optional[List[Vector3]] = None,
                particle_colors: Optional[List[SerializableColor]] = None,
                particle_scales: Optional[List[float]] = None,
                bond_pairs: Optional[List[BondPair]] = None,
                spline_segments: Optional[List[SplineSegment]] = None,
                particle_sizes: Optional[List[Vector3]] = None,
                particle_rotations: Optional[List[Quaternion]] = None,
                color: Optional[SerializableColor] = None,
                mesh: Optional[SerializableMesh] = None,
                material: Optional[SerializableMaterial] = None,
                opacity: Optional[float] = None,
                edge_sharpness: Optional[float] = None) -> SerializableDictionary:
        data: SerializableDictionary = {}
        data["type"] = "noodles"
        if scale is not None:
            data["scale"] = scale
        if particle_positions is not None:
            data["particle.positions"] = particle_positions
        if particle_colors is not None:
            data["particle.colors"] = particle_colors
        if particle_scales is not None:
            data["particle.scales"] = particle_scales
        if bond_pairs is not None:
            data["bond.pairs"] = bond_pairs
        if spline_segments is not None:
            data["spline_segments"] = spline_segments
        if particle_sizes is not None:
            data["particle.sizes"] = particle_sizes
        if particle_rotations is not None:
            data["particle.rotations"] = particle_rotations
        if color is not None:
            data["color"] = color
        if mesh is not None:
            data["mesh"] = mesh
        if material is not None:
            data["material"] = material
        if opacity is not None:
            data["opacity"] = opacity
        if edge_sharpness is not None:
            data["edge.sharpness"] = edge_sharpness
        return data

    @classmethod
    def peptide_planes(cls,
                       particle_positions: Optional[List[Vector3]] = None,
                       particle_colors: Optional[List[SerializableColor]] = None,
                       scale: Optional[float] = None,
                       particle_residues: Optional[List[int]] = None,
                       particle_names: Optional[List[str]] = None,
                       residue_count: Optional[int] = None,
                       residue_chains: Optional[List[int]] = None,
                       particle_scales: Optional[List[float]] = None,
                       particle_sizes: Optional[List[Vector3]] = None,
                       particle_rotations: Optional[List[Quaternion]] = None,
                       color: Optional[SerializableColor] = None,
                       mesh: Optional[SerializableMesh] = None,
                       material: Optional[SerializableMaterial] = None,
                       opacity: Optional[float] = None,
                       bond_pairs: Optional[List[BondPair]] = None,
                       bond_scale: Optional[float] = None,
                       edge_sharpness: Optional[float] = None,
                       cycles: Optional[List[List[int]]] = None) -> SerializableDictionary:
        data: SerializableDictionary = {}
        data["type"] = "peptide planes"
        if particle_positions is not None:
            data["particle.positions"] = particle_positions
        if particle_colors is not None:
            data["particle.colors"] = particle_colors
        if scale is not None:
            data["scale"] = scale
        if particle_residues is not None:
            data["particle.residues"] = particle_residues
        if particle_names is not None:
            data["particle.names"] = particle_names
        if residue_count is not None:
            data["residue.count"] = residue_count
        if residue_chains is not None:
            data["residue.chains"] = residue_chains
        if particle_scales is not None:
            data["particle.scales"] = particle_scales
        if particle_sizes is not None:
            data["particle.sizes"] = particle_sizes
        if particle_rotations is not None:
            data["particle.rotations"] = particle_rotations
        if color is not None:
            data["color"] = color
        if mesh is not None:
            data["mesh"] = mesh
        if material is not None:
            data["material"] = material
        if opacity is not None:
            data["opacity"] = opacity
        if bond_pairs is not None:
            data["bond.pairs"] = bond_pairs
        if bond_scale is not None:
            data["bond.scale"] = bond_scale
        if edge_sharpness is not None:
            data["edge.sharpness"] = edge_sharpness
        if cycles is not None:
            data["cycles"] = cycles
        return data

    @classmethod
    def spheres(cls,
                particle_scale: Optional[float] = None,
                particle_material: Optional[SerializableMaterial] = None,
                outline_material: Optional[SerializableMaterial] = None,
                particle_mesh: Optional[SerializableMesh] = None,
                outline_mesh: Optional[SerializableMesh] = None,
                outline_depth: Optional[float] = None,
                outline_width: Optional[float] = None,
                particle_positions: Optional[List[Vector3]] = None,
                particle_colors: Optional[List[SerializableColor]] = None,
                particle_scales: Optional[List[float]] = None,
                scale: Optional[float] = None,
                particle_sizes: Optional[List[Vector3]] = None,
                particle_rotations: Optional[List[Quaternion]] = None,
                color: Optional[SerializableColor] = None,
                mesh: Optional[SerializableMesh] = None,
                material: Optional[SerializableMaterial] = None,
                opacity: Optional[float] = None) -> SerializableDictionary:
        data: SerializableDictionary = {}
        data["type"] = "spheres"
        if particle_scale is not None:
            data["particle.scale"] = particle_scale
        if particle_material is not None:
            data["particle.material"] = particle_material
        if outline_material is not None:
            data["outline.material"] = outline_material
        if particle_mesh is not None:
            data["particle.mesh"] = particle_mesh
        if outline_mesh is not None:
            data["outline.mesh"] = outline_mesh
        if outline_depth is not None:
            data["outline.depth"] = outline_depth
        if outline_width is not None:
            data["outline.width"] = outline_width
        if particle_positions is not None:
            data["particle.positions"] = particle_positions
        if particle_colors is not None:
            data["particle.colors"] = particle_colors
        if particle_scales is not None:
            data["particle.scales"] = particle_scales
        if scale is not None:
            data["scale"] = scale
        if particle_sizes is not None:
            data["particle.sizes"] = particle_sizes
        if particle_rotations is not None:
            data["particle.rotations"] = particle_rotations
        if color is not None:
            data["color"] = color
        if mesh is not None:
            data["mesh"] = mesh
        if material is not None:
            data["material"] = material
        if opacity is not None:
            data["opacity"] = opacity
        return data

    @classmethod
    def spline(cls,
               particle_positions: Optional[List[Vector3]] = None,
               sequences_particles: Optional[List[List[int]]] = None,
               particle_colors: Optional[List[SerializableColor]] = None,
               particle_scales: Optional[List[float]] = None,
               scale: Optional[float] = None,
               particle_sizes: Optional[List[Vector3]] = None,
               particle_rotations: Optional[List[Quaternion]] = None,
               color: Optional[SerializableColor] = None,
               mesh: Optional[SerializableMesh] = None,
               material: Optional[SerializableMaterial] = None,
               opacity: Optional[float] = None,
               spline_segments: Optional[List[SplineSegment]] = None,
               edge_sharpness: Optional[float] = None) -> SerializableDictionary:
        data: SerializableDictionary = {}
        data["type"] = "spline"
        if particle_positions is not None:
            data["particle.positions"] = particle_positions
        if sequences_particles is not None:
            data["sequences.particles"] = sequences_particles
        if particle_colors is not None:
            data["particle.colors"] = particle_colors
        if particle_scales is not None:
            data["particle.scales"] = particle_scales
        if scale is not None:
            data["scale"] = scale
        if particle_sizes is not None:
            data["particle.sizes"] = particle_sizes
        if particle_rotations is not None:
            data["particle.rotations"] = particle_rotations
        if color is not None:
            data["color"] = color
        if mesh is not None:
            data["mesh"] = mesh
        if material is not None:
            data["material"] = material
        if opacity is not None:
            data["opacity"] = opacity
        if spline_segments is not None:
            data["spline_segments"] = spline_segments
        if edge_sharpness is not None:
            data["edge.sharpness"] = edge_sharpness
        return data
