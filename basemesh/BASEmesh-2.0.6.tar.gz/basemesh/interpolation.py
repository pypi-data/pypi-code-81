# A component of the BASEmesh pre-processing toolkit.
# Copyright (C) 2020  ETH Zürich

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Mesh interpolation tool."""

from typing import Callable, Dict, Optional, Tuple
from .abc import ElevationSource
from .core import Mesh
from .feedback import Feedback
from .types import Triangle2D, Point2D

# Type aliases
_TriangleSampler = Callable[[Triangle2D], Point2D]


def calculate_element_elevation(mesh: Mesh, *args: ElevationSource,
                                default: Optional[float] = None,
                                sampler: Optional[_TriangleSampler] = None,
                                feedback: Optional[Feedback] = None
                                ) -> Dict[int, float]:
    """Calculate and add the element elevation attributes to the mesh.

    This calculates mesh element elevations using a given element
    sampler. The mesh is only used to retrieve the 2D element
    positions, the node elevation is ignored when determining the
    element elevation.

    Parameters
    ----------
    mesh : Mesh
        The mesh to interpolate; its node elevation will be ignored
    *args : ElevationSource
        The elevation sources to use, in descending order of priority
    feedback : Feedback, optional
        A status feedback callable to use for the operation, by default
        None
    default : float, optional
        The default elevation if no value could be retrieved, by
        default None
    sampler : Callable[[Tuple[Tuple[float, float], Tuple[float, float],
                              Tuple[float, float]],
                        Tuple[float, float]]], optional
        The function to use to determine the sampling location for a
        given triangle, by default None

    Returns
    -------
    Dict[int, float]
        A mapping from element ID to elevation

    Raises
    ------
    ValueError
        Raised if no elevation sources were provided
    ValueError
        Raised if no elevation source could produce a value and no
        default value was specified
    """
    if len(args) < 1:
        raise ValueError('At least one elevation source must be provided')
    sources: Tuple[ElevationSource, ...] = tuple(args)

    def triangle_com(triangle: Triangle2D) -> Point2D:
        """Calculate a 2D triangle's centre of mass."""
        avg_x = (triangle[0][0] + triangle[1][0] + triangle[2][0]) / 3.0
        avg_y = (triangle[0][1] + triangle[1][1] + triangle[2][1]) / 3.0
        return avg_x, avg_y

    if sampler is None:
        sampler = triangle_com

    if feedback is not None:
        total = len(mesh.elements)
        interval = int(total / 100) if total > 100 else 1

    # Iterate over all elements in the input mesh
    result_dict: Dict[int, float] = {}
    for index, element in enumerate(mesh.elements):
        sample_point: Point2D = sampler(element.as_triangle_2d)
        height: Optional[float] = None

        # NOTE: This step is identical to the one in interpolate_mesh. It would
        # be nice to have a separate local elevation_at(<sources>) interface to
        # avoid this repetition.

        # Loop over all elevation sources
        for source in sources:
            try:
                # Try to get an elevation from the current source. The
                # ElevationSource ABC requires that a ValueError be raised if
                # the source is unable to produce a value.
                height = source.elevation_at(sample_point)
            except ValueError:
                # If no value could be returned, move on to the next elevation
                # source
                pass
            else:
                # The elevation source provided a height value, quit the loop
                break

        if height is None:
            # If no default height was provided, raise an error
            if default is None:
                raise ValueError(f'Unable to interpolate point {sample_point}')
            # Use the default height if provided
            height = default

        # NOTE: It would be possible to introduce an elevation attribute to the
        # Element object, but this would be confusing considering that node and
        # element elevations are not directly linked or inferrable.
        # To resolve this ambiguity, we would have to add a custom mesh
        # sub class that has only elevation attributes and no node elevation.
        #
        # However, due to the sampler system, this would tie the mesh object to
        # its defining elevation sources, so those would have to stick around
        # as long as the mesh does so we can re-calculate the elevations if the
        # nodes are moved.
        #
        # That too could be mitigated by making this mesh type immutable, but
        # at that point we'd lose mesh editing capability and add a lot of
        # complexity to the object model for no justifiable reason. Therefore,
        # we just calculate the element elevations into a dict and sprinkle
        # them into the 2DM during export.
        #
        # -- LS

        # Record the elevation for this point
        result_dict[element.id_] = height

        if feedback is not None and index % interval == 0:
            feedback.update((index+1)/total)

    return result_dict


def interpolate_mesh(mesh: Mesh, *args: ElevationSource,
                     default: Optional[float] = None,
                     feedback: Optional[Feedback] = None) -> None:
    """Interpolate a mesh using the provided elevation sources.

    This operation modifies the input mesh.

    Parameters
    ----------
    mesh : Mesh
        The mesh to interpolate the nodes of
    *args : ElevationSource
        Any number of elevation sources to use in descending order of
        priority, at least one is required
    default : float, optional
        A fallback value used when no elevation source could produce a
        value for a given point, by default None
    feedback : Feedback, optional
        A feedback callable to communicate with the caller, by default
        None

    Raises
    ------
    ValueError
        Raised if no elevation source has been specified.
    ValueError
        Raised if every elevation source has failed and no default
        value was provided
    """
    if len(args) < 1:
        raise ValueError('At least one elevation source must be provided')
    sources: Tuple[ElevationSource, ...] = tuple(args)

    if feedback is not None:
        total = len(mesh.nodes)
        interval = int(total / 100) if total > 100 else 1

    # Iterate over all nodes in the input mesh
    for index, node in enumerate(mesh.nodes):
        point_xy = node.as_tuple_2d()
        height: Optional[float] = None

        # Loop over all elevation sources
        for source in sources:
            try:
                # Try to get an elevation from the current source. The
                # ElevationSource ABC requires that a ValueError be raised if
                # the source is unable to produce a value.
                height = source.elevation_at(point_xy)
            except ValueError:
                # If no value could be returned, move on to the next elevation
                # source
                pass
            else:
                # The elevation source provided a height value, quit the loop
                break

        if height is None:
            # If no default height was provided, raise an error
            if default is None:
                raise ValueError(f'Unable to interpolate point {point_xy}')
            # Use the default height if provided
            height = default

        # Move the node to the new elevation
        node.move(z=height)

        if feedback is not None and index % interval == 0:
            feedback.update((index+1)/total)
