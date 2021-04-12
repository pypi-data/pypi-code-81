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

"""Helper mesh factories.

These factories are still abstract, but provide simplified endpoints
for common factory designs.
"""

import math
from typing import List, Tuple
from ..core.geometry import Node, Segment
from ..types import Point2D
from .core import BasicFactory


class CircularMeshFactory(BasicFactory):
    """A factory for meshes with circular domains.

    This is a subclass of BasicFactory that also generates a circular
    mesh domain as part of its initialiser.

    The user can either subclass this factory to define their elevation
    function or use the elevation_func method to set the function for
    an initialised factory.
    """

    def __init__(self, radius: float, segments: int = 20,
                 midpoint_offset: Point2D = (0.0, 0.0)) -> None:
        """Initialise a mesh factory with a circular domain.

        Note that the domain cannot actually be perfectly circular due
        to the triangulation. Use the segments argument to specify the
        number of edges of the polygon used to approximate a circle to
        the accuracy your model requires.

        Parameters
        ----------
        radius : float
            The radius of the circle
        segments : int, optional
            The number of line segments used to approximate the circle,
            by default 20
        midpoint_offset : Tuple[float, float], optional
            X and Y offsets for the circle's midpoint; use this to
            position the circle, by default (0.0, 0.0)

        Raises
        ------
        ValueError
            Raised if the given radius is less than or equal to zero
        """
        super().__init__()
        if radius <= 0.0:
            raise ValueError('Domain radius must be greater than zero')
        # Create a polygon approximating the given input circle
        vertices = self._polygonise_circle(radius, segments, *midpoint_offset)
        # Convert vertices to nodes
        nodes = [Node(p) for p in vertices]
        # Add the first node a second time to simplify the loop
        nodes.append(nodes[0])
        # Add mesh boundary break lines
        self.segments = []
        for index, node in enumerate(nodes[:-1]):
            self.segments.append(Segment(node, nodes[index+1]))

    @staticmethod
    def _polygonise_circle(radius: float, sides: int = 12,
                           offset_x: float = 0.0,
                           offset_y: float = 0.0) -> List[Point2D]:
        """Return a regular polygon approximating the given circle.

        The polygon's vertices will lie on the circle, its edges will
        therefore intersect the circle.

        Parameters
        ----------
        radius : float
            The radius of the circle
        sides : int, optional
            The number of sides of the polygon, by default 12
        offset_x : float, optional
            Shift the midpoint in the X direction, by default 0.0
        offset_y : float, optional
            Shift the midpoint in the Y direction, by default 0.0

        Returns
        -------
        List[Tuple[float, float]]
            The polygon vertices
        """
        vertices = []
        for index in range(0, sides):
            # Calculate the angle of the given point
            angle = index/sides * 2 * math.pi
            # Get the x and y coordinates for the given angle
            pos_x = (math.sin(angle) * radius) + offset_x
            pos_y = (math.cos(angle) * radius) + offset_y
            # Add the vertex
            vertices.append((pos_x, pos_y))
        return vertices


class RectangularMeshFactory(BasicFactory):
    """A factory for meshes with rectangular domains.

    This is a subclass of BasicFactory that also generates a
    rectangular mesh domain as part of its initialiser.

    The user can either subclass this factory to define their elevation
    function or use the elevation_func method to set the function for
    an initialised factory.
    """

    def __init__(self, width: float, height: float,
                 midpoint_offset: Tuple[float, float] = (0.0, 0.0)) -> None:
        """Initialise the mesh factory.

        Parameters
        ----------
        width : float
            The width of the rectangle (X axis)
        height : float
            The height of the rectange (Y axis)
        midpoint_offset : Tuple[float, float], optional
             X and Y offsets for the rectangle's midpoint; use this to
            position the rectangle, by default (0.0, 0.0)

        Raises
        ------
        ValueError
            Raised if either edge is shorter than or equal to zero
        """
        super().__init__()
        if width <= 0.0 or height <= 0.0:
            raise ValueError('Domain edge length must be greater than zero')
        # Calculate corner vertices
        offset_x, offset_y = midpoint_offset
        min_x = offset_x - width/2
        max_x = offset_x + width/2
        min_y = offset_y - height/2
        max_y = offset_y + height/2
        vertices = [Node((min_x, min_y)), Node((max_x, min_y)),
                    Node((max_x, max_y)), Node((min_x, max_y))]
        # Add the first node a second time to simplify the loop
        vertices.append(vertices[0])
        # Add mesh boundary break lines
        self.segments = []
        for index, node in enumerate(vertices[:-1]):
            self.segments.append(Segment(node, vertices[index+1]))
