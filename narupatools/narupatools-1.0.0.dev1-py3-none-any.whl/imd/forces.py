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
Code for calculating IMD forces.
"""

from typing import Any, Dict, Protocol, Tuple

import numpy as np

from narupatools.physics.force import (gaussian_force_and_energy,
                                       mass_weighted_forces,
                                       spring_force_and_energy)
from narupatools.physics.rigidbody import center_of_mass
from narupatools.physics.typing import ScalarArray, Vector3Array


class OffsetForceFunction(Protocol):
    """Protocol describing a force on a particle that depends purely on its offset from a given point."""

    def __call__(self, *, offset: np.ndarray, **kwargs: Any) -> Tuple[np.ndarray, float]:
        """
        Calculate the force and energy on a particle at a given offset from the center of a force.

        :param offset: Offset of the particle from the force's center.
        :param kwargs: Optional parameters describing the force.
        :return: A tuple of the force and energy on the given particle.
        """
        ...


CONSTANT_INTERACTION_TYPE = 'constant'
SPRING_INTERACTION_TYPE = 'spring'
GAUSSIAN_INTERACTION_TYPE = 'gaussian'

OFFSET_FORCES: Dict[str, OffsetForceFunction] = {
    GAUSSIAN_INTERACTION_TYPE: gaussian_force_and_energy,  # type: ignore
    SPRING_INTERACTION_TYPE: spring_force_and_energy  # type: ignore
}


def calculate_imd_force(*, positions: Vector3Array, masses: ScalarArray, interaction_type: str,
                        interaction_scale: float, **kwargs: Any) -> Tuple[Vector3Array, float]:
    """
    Calculate the forces and energy to apply for a given interaction.

    :param positions: Positions of particles affected by this interaction.
    :param masses: Masses of particles affected by this interaction.
    :param interaction_type: Type of the interaction. Currently either 'gaussian' or 'spring'.
    :param interaction_scale: Scaling factor of the interaction.
    :return: Tuple of the forces and energy, in matching units to the units of the positions and masses.
    """
    particle_count = len(positions)

    if particle_count > 1:
        center = center_of_mass(positions=positions, masses=masses)
    else:
        center = positions[0]

    if interaction_type == CONSTANT_INTERACTION_TYPE:
        force = np.array(kwargs['force'], dtype=float)
        energy = - np.dot(center, force)
    elif interaction_type in OFFSET_FORCES:
        try:
            potential_method = OFFSET_FORCES[interaction_type]
        except KeyError:
            raise KeyError(f"Unknown interactive force type {interaction_type}.")
        offset = center - np.array(kwargs['position'], dtype=float)
        force, energy = potential_method(offset=offset)
    else:
        raise KeyError(f"Unknown interactive force type {interaction_type}.")

    force *= interaction_scale
    energy *= interaction_scale

    return mass_weighted_forces(force=force, masses=masses), energy
