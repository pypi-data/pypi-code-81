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

"""Implementation of the internal mesh representation for BASEmesh."""

import os
import warnings
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple, Union
import numpy as np  # type: ignore
from ..abc import ElevationSource, SpatialCollection, SupportsSpatial
from ..algorithms import (counting_sort, dist_2d, interpolate_triangle,
                          point_in_polygon_concave, point_in_polygon_convex,
                          distance_to_polygon)
from ..containers import SpatialSet
from ..log import logger
from ..types import Point2D, Point3D, Polygon2D, Triangle2D, Triangle3D
from .geometry import Node

try:
    import py2dm
except ModuleNotFoundError:
    import sys
    wheel_dir = os.path.dirname(__file__)
    wheel_dir, _ = os.path.split(wheel_dir)
    whl_typing_extensions = os.path.join(
        wheel_dir, 'packages', 'typing_extensions-3.7.4.3-py3-none-any.whl')
    sys.path.append(whl_typing_extensions)
    whl_py2dm = os.path.join(
        wheel_dir, 'packages', 'py2dm-0.1.0-py3-none-any.whl')
    sys.path.append(whl_py2dm)

    import py2dm


# Type aliases
_NodeOrPt = Union[Tuple['MeshNode', 'MeshNode', 'MeshNode'],
                  Tuple[Point3D, Point3D, Point3D]]


class MeshNode(Node, SupportsSpatial):
    """A node in a mesh.

    This subclasses the Node class and extends it by providing support
    for elements, a reference to the containing mesh, as well as a
    unique node ID.
    """

    __slots__ = ('_attached_elements', '_id', '_mesh')

    def __init__(self, mesh: 'Mesh', point: Point3D,
                 id_: int, **kwargs: Any) -> None:
        """Initialise a new mesh node.

        Note that the preferred means of creating mesh nodes is the
        Mesh.add_node() method.

        Any keyword arguments passed will be stored with the node and
        are accessible through its attributes property.

        Parameters
        ----------
        mesh : Mesh
            The mesh to create the node in
        point : Tuple[float, float, float]
            The location of the node in space
        id_ : int
            The unique ID of the mesh node
        """
        super().__init__(point, **kwargs)  # Initialise Node
        self._mesh = mesh
        self.id_ = id_
        self._attached_elements: Set['MeshElement'] = set()

    @property
    def elements(self) -> Set['MeshElement']:
        """Return a set of mesh elements defined using this node.

        These elements in this set are also the ones that will be
        removed if this node is deleted.
        """
        return self._attached_elements

    @property
    def mesh(self) -> 'Mesh':
        """Return the mesh this node is a part of."""
        return self._mesh

    @property
    def spatial_marker(self) -> Point2D:
        """Return a 2D point representing this object.

        This point will be used by space-aware containers to optimise
        memory layout.
        """
        return self.pos_x, self.pos_y

    def attach_element(self, element: 'MeshElement') -> None:
        """Attach a mesh element to the mesh node.

        This is usually done by the MeshElement initialiser to ensure
        the mesh element can be deleted when its defining node is.

        Parameters
        ----------
        element : MeshElement
            The element to attach
        """
        self._attached_elements.add(element)

    def detach_element(self, element: 'MeshElement') -> None:
        """Detach a mesh element from the mesh node.

        This is used to remove all references to the mesh element upon
        its deletion, allowing the garbage collector to dispose of it.

        Parameters
        ----------
        element : MeshElement
            The element to detach
        """
        self._attached_elements.discard(element)


class MeshElement(SupportsSpatial):
    """A single mesh element, or face, in a mesh."""

    __slots__ = ('id_', 'materials', '_mesh', '_node_1', '_node_2', '_node_3')

    def __init__(self, mesh: 'Mesh',
                 nodes: Tuple[MeshNode, MeshNode, MeshNode],
                 id_: int, *materials: Union[int, float]) -> None:
        """Initialise a new mesh element.

        Note that the preferred means of creating new mesh elements is
        using the Mesh.add_element() method.

        The element will automatically oriented, you do not have to use
        a specific order when passing the mesh nodes.

        Parameters
        ----------
        mesh : Mesh
            The mesh to create this element for
        nodes : Tuple[MeshNode, MeshNode, MeshNode]
            Existing mesh nodes to create the element from
        id_ : int
            The unique ID of the mesh element
        *materials : Union[int, float]
            Any number of material indices for the mesh
        """
        self.id_ = id_
        self.materials = tuple(materials)
        self._mesh = mesh
        self._node_1 = nodes[0]
        self._node_2 = nodes[1]
        self._node_3 = nodes[2]
        nodes[0].attach_element(self)
        nodes[1].attach_element(self)
        nodes[2].attach_element(self)

        # Conform the element
        # NOTE: calling point_in_polygon_convex for an inner point of the
        # triangle will only return True if the triangle uses CCW vertex order.
        if not point_in_polygon_convex(
                self.spatial_marker, self.as_triangle_2d):
            # Swapping two nodes effectively flips the entire element
            self._node_1 = nodes[1]
            self._node_2 = nodes[0]

    @property
    def area(self) -> float:
        """Return the area of the mesh element."""
        # Convert to numpy arrays
        pt_a = np.array(self.points[0])
        pt_b = np.array(self.points[1])
        pt_c = np.array(self.points[2])
        # Get vectors
        vec_ab = pt_b - pt_a
        vec_ac = pt_c - pt_a
        # Get cross product and halve it
        return float(np.cross(vec_ab, vec_ac)) / 2.0

    @property
    def center(self) -> Tuple[float, float, float]:
        """Return the center of mass of the mesh element."""
        avg_x = (self.points[0][0] + self.points[1][0] + self.points[2][0]) / 3
        avg_y = (self.points[0][1] + self.points[1][1] + self.points[2][1]) / 3
        avg_z = (self.points[0][2] + self.points[1][2] + self.points[2][2]) / 3
        return avg_x, avg_y, avg_z

    @property
    def mesh(self) -> 'Mesh':
        """Return the mesh this element is a part of."""
        return self._mesh

    @property
    def nodes(self) -> Tuple[MeshNode, MeshNode, MeshNode]:
        """Return the nodes defining this element."""
        return self._node_1, self._node_2, self._node_3

    @property
    def points(self) -> Triangle3D:
        """Return the tuple of points defining the mesh element."""
        return (self._node_1.as_tuple(), self._node_2.as_tuple(),
                self._node_3.as_tuple())

    @property
    def as_triangle_2d(self) -> Triangle2D:
        """Return the tuple of 2D points representing this element."""
        return (self._node_1.spatial_marker, self._node_2.spatial_marker,
                self._node_3.spatial_marker)

    @property
    def spatial_marker(self) -> Point2D:
        """Return a 2D point representing this object.

        This point will be used by space-aware containers to optimise
        memory layout.
        """
        return self.center[:2]

    def contains(self, point: Union[Point2D, Point3D]) -> bool:
        """Check whether the given point lies within the element.

        If a 3D point was passed, only the first two coordinates will
        be used for containment checking.

        Parameters
        ----------
        point : Union[Tuple[float, float], Tuple[float, float, float]]
            The point to check for containment

        Returns
        -------
        bool
            Whether the point lies within the mesh element
        """
        return point_in_polygon_convex(point[:2], self.as_triangle_2d)

    def interpolate(self, point: Tuple[float, ...]) -> float:
        """Return the interpolated height at a given point.

        Note that the point does not have to lie within the mesh
        element for this. The element's nodes are used to define an
        infinite plane onto which the point is projected.

        If a 3D point was passed, its elevation will be ignored. It is
        only available as an input for convenience.

        Parameters
        ----------
        point : Union[Tuple[float, float], Tuple[float, float, float]]
            The point to interpolate

        Returns
        -------
        float
            The elevation of the input point when projected onto the
            element
        """
        return interpolate_triangle((point[0], point[1]), self.points)


class Mesh(ElevationSource):
    """A two dimensional mesh with node elevations (aka. 2.5D)."""

    __slots__ = ('_elements', '_nodes', 'node_strings')

    def __init__(self) -> None:
        """Initialise a new mesh.

        A mesh instantiated manually is always empty. Use the
        add_node() and add_element() methods to add geometry.
        """
        self._nodes: SpatialSet[MeshNode] = SpatialSet()
        self._elements: SpatialSet[MeshElement] = SpatialSet()
        self.node_strings: Dict[str, List[MeshNode]] = {}

    @classmethod
    def open(cls, filename: str) -> 'Mesh':
        """Read a 2DM mesh file and instantiate a mesh.

        This only honours the "ND" and "E3T" tags, with only up to one
        material ID.

        Returns
        -------
        Mesh
            The mesh as parsed from the 2DM file

        Raises
        ------
        ValueError
            Raised if the given file is not a valid 2DM file
        ValueError
            Raised if a negative node ID is encountered
        ValueError
            Raised if a negative element ID is encountered
        """
        nodes = []
        with py2dm.Reader(filename) as file_:
            mesh = cls()
            for node in file_.iter_nodes():
                mesh_node = mesh.add_node(node.pos, id_=node.id)
                nodes.append(mesh_node)
            for element in file_.iter_elements():
                element_nodes = tuple(nodes[n-1] for n in element.nodes)
                materials = element.materials
                mesh.add_element(
                    element_nodes, element.id, *materials)  # type: ignore
            for node_string in file_.iter_node_strings():
                node_string_nodes = [nodes[n-1] for n in node_string.nodes]
                if node_string.name is None:
                    warnings.warn(f'Node string {node_string} has no name, '
                                  'skipping')
                mesh.add_node_string(
                    node_string.name, node_string_nodes)   # type: ignore
        return mesh

    @property
    def elements(self) -> SpatialCollection[MeshElement]:
        """Return the mesh elements making up the mesh."""
        return self._elements

    @property
    def nodes(self) -> SpatialCollection[MeshNode]:
        """Return the mesh nodes defining its elements.

        Note that the mesh nodes are also available through the mesh
        elements via MeshElement.nodes, which may be faster than
        manually associating nodes and elements.
        """
        return self._nodes

    def add_node(self, point: Point3D, id_: Optional[int] = None,
                 **kwargs: Any) -> MeshNode:
        """Create a new node for the mesh.

        If no mesh ID was provided, a new mesh ID will be chosen based
        on existing nodes in the mesh.

        Parameters
        ----------
        point : Tuple[float, float, float]
            The position of the new node
        id_ : int, optional
            The ID to use for this node, by default None

        Returns
        -------
        MeshNode
            The node that was created; the node will already be added
            to the mesh by the time this method exits
        """
        if id_ is None:
            id_ = self._get_node_id()
        node = MeshNode(self, point, id_, **kwargs)
        self._nodes.add(node)
        return node

    def add_element(self,
                    nodes: Union[Tuple['MeshNode', 'MeshNode', 'MeshNode'],
                                 Tuple[Point3D, Point3D, Point3D]],
                    id_: Optional[int], *materials: Union[int, float]
                    ) -> MeshElement:
        """Add a new element using the given mesh nodes.

        If the given nodes are already part of the current mesh, they
        will be linked to the created element. If they are points, new
        nodes will be created and added to the mesh before adding the
        element.

        If no element ID has been provided, one will be selected based
        on existing elements.

        Parameters
        ----------
        nodes : Union[Tuple[MeshNode, MeshNode, MeshNode],
                      Tuple[Point3D, Point3D, Point3D]]
            The nodes to create the element from
        id_ : int, optional
            The ID of the element, by default None
        *materials : int, optional
            Any number of material indices for the element

        Returns
        -------
        MeshElement
            The mesh element that was created

        Raises
        ------
        ValueError
            Raised when attempting to define an element using nodes
            defined in another mesh
        ValueError
            Raised if any of the input nodes coincide
        """
        # Process input nodes
        element_nodes: Set[MeshNode] = set()
        for node in nodes:
            if isinstance(node, MeshNode):
                # If the node is part of the mesh, re-use it
                if node in self.nodes:
                    element_nodes.add(node)
                # If it isn't, raise an error (no cross-meshing yet)
                else:
                    raise ValueError(
                        f'MeshNode {node} is not part of the mesh')
            else:
                # If the node is a tuple of floats, look for an existing node
                # with the same coordinates
                try:
                    found_node = self.node_at(node)
                except ValueError:
                    # If it doesn't exist yet, create a new node
                    new_node = MeshNode(self, node, self._get_node_id())
                    element_nodes.add(new_node)
                else:
                    # If it does, add the existing mesh node instead
                    element_nodes.add(found_node)

        # Ensure our three nodes span a triangle (i.e. don't coincide)
        if len(set(n.spatial_marker for n in element_nodes)) < 3:
            raise ValueError('Input nodes may not coincide')

        # Add the nodes to the mesh, if required
        for node in element_nodes:
            if node not in self.nodes:
                self._nodes.add(node)

        # Create a new element
        if id_ is None:
            id_ = self._get_element_id()
        nodes_tuple: Tuple[MeshNode, MeshNode, MeshNode] = tuple(
            element_nodes)  # type: ignore
        element = MeshElement(self, nodes_tuple, id_, *materials)
        self._elements.add(element)
        return element

    def add_node_string(self, name: str, nodes: Iterable[MeshNode]) -> None:
        """Add a new node string using the given mesh nodes.

        If the given nodes are not part of the current mesh, an error
        will be raised.

        Parameters
        ----------
        name: str
            The unique name of the node string
        nodes: Iterable[MeshNode]
            The series of nodes making up the node string

        Raises
        ------
        KeyError
            Raised if a node string with the given name already exists
        ValueError
            Raised if the given nodes are not part of the current mesh
        """
        if name in self.node_strings:
            raise KeyError(f'Node string {name} already exists')
        for node in nodes:
            if node.mesh != self:
                raise ValueError(
                    f'Node {node} is not part of the current mesh')
        self.node_strings[name] = list(nodes)

    def element_at(self, point: Union[Point2D, Point3D]) -> MeshElement:
        """Return the element containing the given point.

        If the point lies outside of any mesh elements, a ValueError
        is raised.

        If a 3D point is passed, only the first two coordinates will be
        used for containment checking.

        Parameters
        ----------
        point : Union[Tuple[float, float], Tuple[float, float, float]]
            The point to find the containing element for

        Returns
        -------
        MeshElement
            The mesh element containing the given point

        Raises
        ------
        ValueError
            Raised if the input point does not lie within any mesh
            element
        """
        for element in self.elements.iter_spatial(point[:2]):
            if element.contains(point):
                return element
        raise ValueError(f'Point {point} does not lie within any mesh element')

    def elements_by_polygon(self, polygon: Polygon2D,
                            check_midpoints: bool = True) -> List[MeshElement]:
        """Return any elements contained in the given polygon.

        Disabling the "check_midpoints" flag will cause every corner
        point of the element to be checked instead, which will triple
        the workload.

        Parameters
        ----------
        polygon : Tuple[Tuple[float, float], ...]
            The polygon to filter the elements by
        check_midpoints : bool, optional
            Whether to use the (faster) midpoint-only check, or the
            more accurate edge containment check, by default True

        Returns
        -------
        List[MeshElement]
            A list of mesh elements contained in the polyogn

        Raises
        ------
        ValueError
            Raised if the input polygon has fewer than three vertices
        """
        # Simple check: centroids only
        if check_midpoints:
            return [e for e in self.elements
                    if point_in_polygon_concave(e.center[:2], polygon)]
        # Advanced check: all element vertices must be contained
        return [e for e in self.elements
                if all(point_in_polygon_concave(n.as_tuple_2d(), polygon)
                       for n in e.nodes)]

    def elevation_at(self, point: Union[Point2D, Point3D]) -> float:
        """Return the interpolated elevation at the given point.

        If no mesh element contains the point exactly, it will be
        re-checked using a maximum distance of 1.0e-6.

        If a 3D point is passed, only the first two coordinates will be
        used for containment checking.

        Parameters
        ----------
        point : Union[Tuple[float, float], Tuple[float, float, float]]
            The point to get the elevation for

        Returns
        -------
        float
            The elevation of the mesh at the given point.

        Raises
        ------
        ValueError
            Raised if the point lies outside the mesh
        """
        PRECISION = 1.0e-1  # Maximum distance for non-exact point matches
        try:
            # Try to find an element containing this point
            element = self.element_at(point)
        except ValueError as err:
            # If this fails, try to find the closest element instead. This is
            # necessary as the element_at check fails early and does not check
            # for floating point errors around mesh element edges.
            logger.debug('Unable to find containing element for point %s, '
                         'searching for closest element instead...', point[:2])
            element = self.get_element(point)

            # Calculate the minimum distance between the closest element and
            # the point to check
            triangle_2d = tuple(p[:2] for p in element.points)
            dist = distance_to_polygon(point[:2], triangle_2d)

            if dist < PRECISION:
                # If the point is within the precision tolerance of the
                # element, the element may still be used for interpolation.
                logger.debug('Closest element %s within tolerance (%f <= %f)',
                             element.spatial_marker, dist, PRECISION)
            else:
                # The point is too far away from any element,
                # re-raise the error and try another interpolation source.
                logger.debug('Closest element %s outside of tolerance (%f > '
                             '%f)', element.spatial_marker, dist, PRECISION)
                raise err
        return element.interpolate(point)

    def get_element(self, point: Union[Point2D, Point3D], *,
                    search_effort: float = 1.0) -> MeshElement:
        """Return the element closest to the given point.

        By default, this exhaustively searches the entire mesh. In this
        case, the search is guaranteed to return the closest element.

        The search_effort argument may be used to reduce search effort
        by quitting after X ratio of all elements have been checked,
        then picking the closest one found.
        This is only useful with space-aware containers where only
        searching ~10% of the entire data set might give sufficiently
        high confidence.

        If a 3D point is passed, only the first two coordinates will be
        used for containment checking.

        Parameters
        ----------
        point : Union[Tuple[float, float], Tuple[float, float, float]]
            The point to check
        search_effort : float, optional
            The ratio of the data set to check, by default 1.0

        Returns
        -------
        MeshElement
            The closest element to the given point

        Raises
        ------
        ValueError
            Raised if the search_effort argument valls is equal to or
            less than 0, or if it is greater than 1
        ValueError
            Raised if the mesh is empty
        """
        if search_effort <= 0.0 or search_effort > 1.0:
            raise ValueError('Search effort must fall within the (0.0, 1.0] '
                             f'range (current: {search_effort}')
        if not self.elements:
            raise ValueError('Mesh does not contain any element')

        point_2d: Point2D = point[:2]
        lowest_dist = -1.0
        closest_element: Optional[MeshElement] = None

        for index, element in enumerate(self.elements.iter_spatial(point_2d)):
            # Calculate the distance between the element and the point
            triangle_2d = tuple((p[0], p[1]) for p in element.points)
            dist = distance_to_polygon(point_2d, triangle_2d)

            # Exit early if the point is contained within an element
            if dist < 0.0:
                logger.info('Found containing element %s for point %s',
                            element.spatial_marker, point_2d)
                return element

            # Update closest element
            if lowest_dist < 0.0 or dist < lowest_dist:
                lowest_dist = dist
                closest_element = element

            # Check search effort
            if (index+1) / len(self.elements) > search_effort:
                logger.info(
                    'Exceeded search effort of %f: %d of %d elements checked',
                    search_effort, index+1, len(self.elements))
                break

        assert closest_element is not None
        return closest_element

    def _get_element_id(self) -> int:
        """Return a valid element ID.

        This does not check for holes in the element numbering.

        Returns
        -------
        int
            An available element ID
        """
        return len(self.elements)

    def get_node_by_id(self, id_: int) -> MeshNode:
        """Return the node with the given ID.

        Paramters
        ---------
        id_: int
            The node ID to return

        Raises
        ------
        ValueError
            Raised if the given node ID does not exist
        """
        for node in self._nodes:
            if node.id_ == id_:
                return node
        raise ValueError(f'No node with ID {id_} found')

    def get_node(self, point: Union[Point2D, Point3D], *,
                 search_effort: float = 1.0) -> MeshNode:
        """Return the node closest to the given point.

        By default, this exhaustively searches the entire mesh. In this
        case, the search is guaranteed to return the closest node.

        The search_effort argument may be used to reduce search effort
        by quitting after X ratio of all nodes have been checked, then
        picking the closest one found.
        This is only useful with space-aware containers where only
        searching ~10% of the entire data set might give sufficiently
        high confidence.

        If a 3D point is passed, only the first two coordinates will be
        used for containment checking.

        Parameters
        ----------
        point : Union[Tuple[float, float], Tuple[float, float, float]]
            The point to check
        search_effort : float, optional
            The ratio of the data to check, by default 1.0

        Returns
        -------
        MeshNode
            The closest node to the given point

        Raises
        ------
        ValueError
            Raised if the search_effort argument valls is equal to or
            less than 0, or if it is greater than 1
        ValueError
            Raised if the mesh is empty
        """
        if search_effort <= 0.0 or search_effort > 1.0:
            raise ValueError('Search effort must fall within the (0.0, 1.0] '
                             f'range (current: {search_effort}')
        if not self.nodes:
            raise ValueError('Mesh does not contain any nodes')

        point_2d: Point2D = point[:2]
        lowest_dist = -1.0
        closest_node: Optional[MeshNode] = None
        for index, node in enumerate(self.nodes.iter_spatial(point_2d)):
            dist = dist_2d(node.spatial_marker, point_2d)
            if lowest_dist < 0.0 or dist < lowest_dist:
                lowest_dist = dist
                closest_node = node
            if (index+1) / len(self.nodes) > search_effort:
                logger.info('Exceeded search effort of %f: %d of %d nodes '
                            'checked', search_effort, index+1, len(self.nodes))
                break

        assert closest_node is not None
        return closest_node

    def _get_node_id(self) -> int:
        """Return a valid node ID.

        This does not check for holes in the node numbering.

        Returns
        -------
        int
            An available node ID
        """
        return len(self.nodes)

    def node_at(self, point: Union[Point2D, Point3D]) -> MeshNode:
        """Return the node at the given point.

        If no node is found at the given point, a ValueError is raised.

        This performs an exact check, be wary of floating-point errors.

        To get the closest node to a given point without an exact
        check, use the Mesh.get_node() method instead.

        If a 3D point is passed, only the first two coordinates will be
        used for containment checking.

        Parameters
        ----------
        point : Union[Tuple[float, float], Tuple[float, float, float]]
            The point to check

        Returns
        -------
        MeshNode
            The mesh node at the given point

        Raises
        ------
        ValueError
            Raised if no node was found at the given point
        """
        for node in self.nodes.iter_spatial(point[:2]):
            if node.spatial_marker == point[:2]:
                return node
        raise ValueError(f'No node found at {point}')

    def purge_nodes(self) -> List[MeshNode]:
        """Delete any dangling nodes from the mesh.

        Dangling nodes are nodes that are not referenced by any mesh
        elements.

        Returns
        -------
        List[MeshNode]
            The list of nodes that were removed from the mesh
        """
        purged = [n for n in self.nodes if not n.elements]
        _ = (self.remove_node(n) for n in purged)  # type: ignore
        return purged

    def remove_element(self, element: MeshElement) -> None:
        """Remove an element from the mesh.

        This does not delete the element's defining nodes, only the
        element itself is removed and detached from its defining nodes.

        Parameters
        ----------
        element : MeshElement
            The element to remove

        Raises
        ------
        ValueError
            Raised if the element is not part of this mesh
        """
        try:
            self._elements.remove(element)
        except KeyError as err:
            raise ValueError(
                f'MeshElement {element} is not part of the mesh') from err
        else:
            for node in list(element.nodes):
                node.detach_element(element)

    def remove_node(self, node: MeshNode) -> None:
        """Remove a node from the mesh.

        This also deletes any elements that were defined using the
        deleted node.

        Parameters
        ----------
        node : MeshNode
            The node to delete

        Raises
        ------
        ValueError
            Raised if the node is not part of this mesh
        """
        logger.debug('Deleted node with ID %d, also deleted %d associated '
                     'elements.', node.id_, len(node.elements))
        for element in list(node.elements):
            self.remove_element(element)
        try:
            self._nodes.remove(node)
        except KeyError as err:
            raise ValueError(
                f'MeshNode {node} is not part of the mesh') from err

    def save(self, filename: str, num_materials: Optional[int] = None) -> None:
        """Save the current mesh as a 2DM mesh file.

        Parameters
        ----------
        filename : str
            The file path to save the mesh to
        num_materials : int, optional
            The number of materials to write to disk, by default None
        """
        # This dict is used to keep track of any shifts in the node IDs
        transform_ids: Dict[int, int] = {}

        # Read the num_materials field from the first element if not provided
        num_materials = len(next(iter(self.elements)).materials)

        with py2dm.Writer(filename) as mesh:
            # Specify the number of materials to write and expect
            mesh.num_materials_per_elem(num_materials)
            mesh.write_header()

            # Write nodes
            nodes: List[MeshNode] = counting_sort(
                list(self.nodes), lambda x: x.id_)
            for node in nodes:
                transform_ids[node.id_] = mesh.node(*node.as_tuple())
            mesh.write_nodes()

            # Write elements
            elements: List[MeshElement] = counting_sort(
                list(self.elements), lambda x: x.id_)
            for element in elements:
                node_ids = tuple(transform_ids[n.id_] for n in element.nodes)
                mesh.element(py2dm.Element3T, node_ids,
                             element.materials[:num_materials])
            mesh.write_elements()

            # Write node strings
            for name, nodes in self.node_strings.items():
                node_ids = tuple(transform_ids[n.id_] for n in nodes)
                mesh.node_string(node_ids, name)
            mesh.write_node_strings()

        # BASEMENT 3 compatibility: Remove trailing whitespace
        self._strip_trailing_newline(filename)

    @staticmethod
    def _strip_trailing_newline(filename: str) -> None:
        """Remove any trailing newlines in the given file.

        This is necessary for compatibility with BASEMENT 3. The file
        is truncated in-place.

        Parameters
        ----------
        filename : str
            The file to truncate
        """
        with open(filename, 'rb+') as file_:
            # Jump to the end of the file
            file_.seek(0, os.SEEK_END)
            # This loop reads char by char from the back of the file as long as the
            # characters returned are considered whitespace.
            while not file_.read(1).strip():
                file_.seek(-2, os.SEEK_CUR)
            # The last read bit was non-whitespace; truncate the file
            file_.truncate()
