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

"""Generic geometry classes used for Triangle I/O."""

import contextlib
import itertools
import warnings
from collections import OrderedDict
from typing import Any, Dict, List, Optional, Set, Tuple, Union
from ..algorithms import (dist_2d, dist_3d, interpolate_line,
                          line_segments_intersection, line_intersection,
                          point_on_line, point_within_range)
from ..errors import TopologyError
from ..feedback import Feedback
from ..log import logger
from ..triangle import PSLGNode, PSLGSegment
from ..types import Line2D, Line3D, Point2D, Point3D


class Node:
    """A point in space.

    A node is a 3D point with optional attributes used to store
    additional information.
    """

    __slots__ = ('attributes', '_attached_segments', 'pos_x', 'pos_y', 'pos_z')

    def __init__(self, pos: Union[Point2D, Point3D], **kwargs: Any) -> None:
        """Create a new node from the given point.

        Any keyword arguments passed will be treated as attributes and
        stored alongside the node.

        Parameters
        ----------
        pos : Union[Tuple[float, float], Tuple[float, float, float]]
            The position of the node
        """
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        try:
            self.pos_z = pos[2]  # type: ignore
        except IndexError:
            self.pos_z = 0.0
        self.attributes: Dict[str, Any] = OrderedDict(
            sorted(kwargs.items(), key=lambda x: x[0].lower()))
        self._attached_segments: Set['Segment'] = set()

    def __del__(self) -> None:
        """Delete any segments along with their defining node.

        Note that any exceptions raised herein will not interrupt the
        deletion process.
        """
        # Delete any attached geometries along with their defining node
        while self._attached_segments:
            with contextlib.suppress(KeyError):
                _ = self._attached_segments.pop()

    @property
    def attached_segments(self) -> Set['Segment']:
        """Return the set of attached segments."""
        return self._attached_segments

    @property
    def elevation(self) -> float:
        """Return the elevation of the node."""
        return self.pos_z

    def attach_segment(self, segment: 'Segment') -> None:
        """Register the given segment as being attached to the node.

        This is usually done as part of the Segment class's
        initialiser and is used to ensure the segment will be deleted
        with its defining node.

        Parameters
        ----------
        segment : Segment
            The segment instance to attach to the node
        """
        self._attached_segments.add(segment)

    def detach_segment(self, segment: 'Segment') -> None:
        """Unregister the given segment from the node.

        This is usually done to ensure the Segment object can be
        garbage-collected when it is no longer needed, since keeping it
        referenced in a node would prevent its destruction.

        Parameters
        ----------
        segment : Segment
            The segment instance to detach from the node
        """
        self._attached_segments.discard(segment)

    # pylint: disable=invalid-name
    def move(self, x: Optional[float] = None, y: Optional[float] = None,
             z: Optional[float] = None) -> None:
        """Move the node to a new location.

        Any coordinate whos argument is left at None will keep their
        current value.
        Note that this also mvoes any geometries defined through this
        node.

        Parameters
        ----------
        x : float, optional
            New X coordinate of the node, by default None
        y : float, optional
            New Y coordinate of the node, by default None
        z : float, optional
            New Z coordinate of the node, by default None
        """
        if x is not None:
            self.pos_x = x
        if y is not None:
            self.pos_y = y
        if z is not None:
            self.pos_z = z

    def as_tuple(self) -> Tuple[float, float, float]:
        """Return the coordinates of the node as a tuple."""
        return self.pos_x, self.pos_y, self.pos_z

    def as_tuple_2d(self) -> Tuple[float, float]:
        """Return the X and Y coordinates of the node as a tuple."""
        return self.pos_x, self.pos_y


class Segment:
    """A 3D line segment defined through two nodes."""

    __slots__ = ('_node_1', '_node_2')

    def __init__(self, node_1: Node, node_2: Node) -> None:
        """Initialise the line segment from two nodes.

        Note that the nodes will be sorted, the order of the arguments
        is therefore inconsequential.

        Parameters
        ----------
        node_1 : Node
            First input node
        node_2 : Node
            Second input node

        Raises
        ------
        TopologyError
            Raised if the two nodes are coincident or identical
        TopologyError
            Raised if the X and Y coordinates of the input nodes are
            identical, even if their elevation is different
        """
        if node_1 == node_2:
            raise TopologyError(
                'Two separate nodes required to define a segment')
        self._node_1 = node_1
        self._node_2 = node_2
        # Re-order nodes if needed
        if self._nodes_sorted() != (self._node_1, self._node_2):
            self._node_2 = node_1
            self._node_1 = node_2

        self._node_1.attach_segment(self)
        self._node_2.attach_segment(self)
        if self.length_2d == 0:
            raise TopologyError(
                'The 2D projection of the segment has a length of zero')

    def __eq__(self, value: Any) -> bool:
        """Segment equality check.

        This ensures that two segments connecting the same nodes will
        be considered identical regardless of node order.

        Parameters
        ----------
        value : Any
            The value to compare the segment against

        Returns
        -------
        bool
            Whether the two objects are identical
        """
        if not isinstance(value, self.__class__):
            return False
        return self.nodes == value.nodes

    def __hash__(self) -> int:
        """Return the hash for the given segment.

        This uses a coordinate-sorted list for the nodes to ensure two
        segments of opposing direction will hash the same.
        """
        return hash((self._node_1, self._node_2))

    @property
    def length(self) -> float:
        """Return the 3D length of the segment."""
        return dist_3d(*self.as_line())

    @property
    def length_2d(self) -> float:
        """Return the 2D length of the segment."""
        return dist_2d(*self.as_line_2d())

    @property
    def nodes(self) -> Set[Node]:
        """Return the nodes defining this segment.

        The returned set will always have exactly two elements.
        """
        return set((self._node_1, self._node_2))

    def as_line(self) -> Line3D:
        """Return the segment as a tuple of 3D points.

        The returned points are coordinate-sorted.
        """
        n_1 = self._node_1
        n_2 = self._node_2
        return ((n_1.pos_x, n_1.pos_y, n_1.pos_z),
                (n_2.pos_x, n_2.pos_y, n_2.pos_z))

    def as_line_2d(self) -> Line2D:
        """Return the segment as a tuple of 2D points.

        The returned points are coordinate-sorted.
        """
        n_1 = self._node_1
        n_2 = self._node_2
        return (n_1.pos_x, n_1.pos_y), (n_2.pos_x, n_2.pos_y)

    def _nodes_sorted(self) -> Tuple[Node, Node]:
        """Sort the segment's nodes by coordinates.

        This is done to ensure that two segments defined using opposite
        node order end up as the same object.

        Returns
        -------
        Tuple[Node, Node]
            The segment's nodes sorted by its coordinates
        """
        # NOTE: This orients the line so it faces right and up
        pt_a = self._node_1.as_tuple_2d()
        pt_b = self._node_2.as_tuple_2d()
        # Sort using X
        if pt_a[0] < pt_b[0]:
            return self._node_1, self._node_2
        if pt_a[0] > pt_b[0]:
            return self._node_2, self._node_1
        # X coordinate identical -> sort using Y
        if pt_a[1] < pt_b[1]:
            return self._node_1, self._node_2
        return self._node_2, self._node_1

    def split(self, node: Node) -> 'Segment':
        """Split the segment at the given node.

        The current segment is shortened to end at the given node, and
        a new segment starting at the inserted node and ending at the
        current node's original end point is created and returned.

        Returns
        -------
        Segment
            The new segment that was created, leading from the
            inserted node to this Segment's original end point

        Raises
        ------
        TopologyError
            Raised if the given node is coincident with one of the
            segment's defining nodes
        """
        if node in (self._node_1, self._node_2):
            raise TopologyError(
                'Unable to split segment on one of its defining nodes')
        # Store the original end node
        end_node = self._node_2
        self._node_2.detach_segment(self)
        # Move this segment to end at the inserted node
        self._node_2 = node
        self._node_2.attach_segment(self)
        # Create a new segment (this also attaches the segment to the nodes)
        return Segment(node, end_node)


class Lattice:
    """An unstructured 3D collection of nodes and segments."""

    def __init__(self, precision: float = 1e-6) -> None:
        """Instantiate the lattice.

        The precision is used for any non-exact checks for all geometry
        added to the lattice container.

        Parameters
        ----------
        precision : float, optional
            The snapping tolerance for any geometries added, by default
            1e-6
        """
        self._nodes: List[Node] = []
        self.precision = precision
        self._segments: List[Segment] = []

    @property
    def nodes(self) -> List[Node]:
        """Return the list of nodes in the lattice."""
        return self._nodes

    @property
    def segments(self) -> List[Segment]:
        """Return the list of segmetns in the lattice."""
        return self._segments

    def add_node(self, point: Point3D, warn_duplicate: bool = False,
                 auto_conform: bool = True) -> Node:
        """Add a new node to the lattice.

        If a node already exists at the position of the given point, no
        node is created. If warn_duplicate is enabled, a warning will
        be broadcast.

        Parameters
        ----------
        point : Tuple[float, float, float]
            The location of the node to add
        warn_duplicate : bool, optional
            Whether to broadcast a warning if a node already exists at
            this 2D location, by default False
        auto_conform : bool, optional
            Whether to conform the lattice after adding the node, by
            default True

        Returns
        -------
        Node
            The created node, or the existing node if one already
            existed at this location
        """
        for node in self.nodes:
            # If an existing node is close enough
            if point_within_range(node.as_tuple_2d(), point[:2],
                                  max_dist=self.precision):
                if warn_duplicate:
                    warnings.warn(f'Duplicate node at {node.as_tuple_2d()}')
                logger.debug('Found existing node at %s', node.as_tuple_2d())
                return node

        logger.debug('Creating new node at %s', point[:2])
        node = Node(point)
        self.nodes.append(node)
        if auto_conform:
            self.conform()

        return node

    def add_segment(self, node_1: Node, node_2: Node,
                    warn_duplicate: bool = False,
                    auto_conform: bool = True,) -> None:
        """Add a new segment to the lattice.

        If another segment already exists between the given nodes, no
        segment is created. If warn_duplicate is enabled, a warning
        will be broadcast.

        Parameters
        ----------
        node_1 : Node
            The first node defining the segment
        node_2 : Node
            The second node defining the segoment
        warn_duplicate : bool, optional
            Whether to broadcast a warning if a segment already exists
            between these points, by default False
        auto_conform : bool, optional
            Whether to conform the lattice after adding the segment,
            by default True
        """
        # Only create the segment if it is not an exact duplicate
        for segment in self.segments:
            if segment.nodes == set((node_1, node_2)):
                line = tuple(n.as_tuple_2d() for n in segment.nodes)
                if warn_duplicate:
                    warnings.warn(f'Duplicate segment at {line}')
                logger.debug('A segment between %s and %s already exists',
                             line[0], line[1])
                return
        # Only create the segment if it not degenerate
        if node_1 == node_2:
            pos = node_1.as_tuple_2d()
            if warn_duplicate:
                warnings.warn(f'Degenerate segment at {pos}')
            logger.debug('Zero-length segment encountered at %s', pos)
            return

        new_segment = Segment(node_1, node_2)
        logger.debug('Creating new segment at %s',
                     tuple(n.as_tuple_2d() for n in new_segment.nodes))
        if new_segment not in self.segments:
            self.segments.append(new_segment)
        if auto_conform:
            self.conform()

    def as_pslg(self) -> Tuple[List[PSLGNode], List[PSLGSegment]]:
        """Return the contents of the lattice in Triangle format.

        The user is responsible for ensuring their geometry is valid,
        either by taking care when adding geometry or by calling
        Lattice.conform() before calling this function.

        Since Triangle does not support 3D geometries, the node
        elevation will be stored in the "pos_z" attribute of the
        PSLGNode class.

        Returns
        -------
        Tuple[List[PSLGNode], List[PSLGSegment]]
            The nodes and segments representing this lattice
        """
        triangle_nodes: List[PSLGNode] = [
            PSLGNode(*n.as_tuple_2d(), pos_z=n.elevation) for n in self.nodes]
        triangle_segments: List[PSLGSegment] = [
            PSLGSegment.from_points(*l.as_line(), nodes=triangle_nodes)
            for l in self.segments]
        return triangle_nodes, triangle_segments

    def conform(self, *, feedback: Optional[Feedback] = None) -> None:
        """Process the lattice's geometries to make them compliant.

        This involves node deduplication, insertion of nodes at segment
        intersections and splitting segments via nodes.

        Note that this can be a fairly expensive operation for large
        geometries.

        Parameters
        ----------
        feedback : Feedback, optional
            A helper object used to retrieve status information about
            the conformation process, by default None
        """
        # Step 1: Deduplicate nodes
        if feedback is not None:
            feedback.update(msg='Deduplicating nodes...')
            feedback.set_scaling(0.2)
        removed = self.deduplicate_nodes(feedback=feedback)
        print(f'{removed} nodes removed')

        # Step 2: Find intersections
        if feedback is not None:
            feedback.update(msg='Finding intersections...')
            feedback.set_scaling(0.6, 0.2)
        added = self.add_intersection_nodes(feedback=feedback)
        print(f'{added} nodes added')

        # Step 3: Split segments
        if feedback is not None:
            feedback.update(msg='Splitting segments...')
            feedback.set_scaling(0.2, 0.8)
        splits = self.split_segments(feedback=feedback)
        print(f'{splits} segments split')

    def deduplicate_nodes(self, *, feedback: Optional[Feedback] = None) -> int:
        """Remove and duplicate nodes.

        Parameters
        ----------
        feedback : Feedback, optional
            The Feedback object to use for status updates, by default
            None

        Returns
        -------
        int
            The number of nodes removed.
        """
        nodes_to_remove: List[Node] = []
        # Get a list of all unique, unordered pairs of nodes
        combinations: List[Tuple[Node, Node]] = list(
            itertools.combinations(self.nodes, 2))  # type: ignore
        if feedback is not None:
            total = len(combinations)
            interval = int(total / 100) if total > 100 else 1

        element: Tuple[Node, Node]
        for index, element in enumerate(combinations):
            node_a, node_b = element
            pt_a = node_a.as_tuple_2d()
            pt_b = node_b.as_tuple_2d()

            if point_within_range(pt_a, pt_b, max_dist=self.precision):
                logger.info('Removing duplicate node at %s', pt_b)

                # Relink node segments
                # NOTE: list cast used to allow mutation of the underlying set
                for segment in list(node_b.attached_segments):
                    logger.debug('Relinking segment %s', segment.as_line_2d())
                    self.segments.remove(segment)
                    node_b.detach_segment(segment)

                    # Create a copy of the node
                    nodes_list = list(segment.nodes)
                    nodes_list.remove(node_b)
                    other_node = nodes_list[0]
                    segment = Segment(node_a, other_node)
                    self.segments.append(segment)
                    node_a.attach_segment(segment)

                # Mark node segment for deletion
                nodes_to_remove.append(node_b)

            if feedback is not None and index % interval == 0:
                feedback.update((index+1)/total)

        if nodes_to_remove:
            logger.info('Deleting %d duplicate nodes', len(nodes_to_remove))
            _ = (self.nodes.remove(n) for n in nodes_to_remove)  # type: ignore

        # Return the number of deleted nodes
        return len(nodes_to_remove)

    def add_intersection_nodes(self, *, feedback: Optional[Feedback] = None
                               ) -> int:
        """Add a node at each segment intersection point.

        Call split_segments() afterwards to get a non-intersecting
        lattice.

        Parameters
        ----------
        feedback : Feedback, optional
            The Feedback object to use for status updates, by default
            None, by default None

        Returns
        -------
        int
            The number of inserted nodes

        Raises
        ------
        TopologyError
            Raised if two collinear segments are encountered
        """
        combinations = list(itertools.combinations(self.segments, 2))

        if feedback is not None:
            total = len(combinations)
            interval = int(total / 100) if total > 100 else 1

        added_nodes = 0

        for index, tuple_ in enumerate(combinations):
            segment_a, segment_b = tuple_
            line_a = segment_a.as_line_2d()
            line_b = segment_b.as_line_2d()

            if feedback is not None and index % interval == 0:
                feedback.update((index+1)/total)

            if not line_segments_intersection(line_a, line_b,
                                              allow_collinear=False):
                continue

            # Check for coincident endpoints
            if line_a[0] in line_b or line_a[1] in line_b:
                logger.debug('Segments %s and %s share an endpoint (exact), '
                             'not a valid intersection', line_a, line_b)
                continue

            logger.debug('Segments %s and %s intersect, calculating '
                         'intersection point', line_a, line_b)
            try:
                intersection = line_intersection(line_a, line_b)
            except ValueError as err:
                raise TopologyError(f'Collinear line segments found: {line_a} '
                                    f'and {line_b}') from err
            # Ignore endpoint intersections
            is_valid = True
            logger.debug('Checking intersection distance from endpoints')
            for endpoint in (*line_a, *line_b):
                if dist_2d(intersection, endpoint) < self.precision:
                    logger.debug('Segments touching in %s, not a valid '
                                 'intersection', intersection)
                    is_valid = False
                    break
            if not is_valid:
                continue
            logger.info('Segment intersection at %s', intersection)

            # Create an intersection node
            height_a = interpolate_line(intersection, segment_a.as_line())
            height_b = interpolate_line(intersection, segment_b.as_line())
            # Check height difference
            if abs(height_a-height_b) > self.precision:
                warnings.warn(
                    f'Conflicting elevation data for {intersection}: using '
                    f'original height of {height_a} and ignoring other (was '
                    f'{height_b}).\nNote that this causes the line segments '
                    f'{(line_b[0], intersection, line_b[1])} to lose '
                    f'their collinearity.')
            self.add_node((*intersection, height_a), auto_conform=False)
            added_nodes += 1

        return added_nodes

    def split_segments(self, *, feedback: Optional[Feedback] = None) -> int:
        """Split the lattice's segments at the nodes.

        This ensures no node lies in the middle of a segment, and
        segment will lie between two nodes. If a segment is split by
        more than one node, it will be split more than once.

        Parameters
        ----------
        feedback : Feedback, optional
            The Feedback object to use for status updates, by default
            None, by default None, by default None

        Returns
        -------
        int
            The number of splits performed
        """
        if feedback is not None:
            total = len(self.nodes)

        splits_performed = 0

        for index, node in enumerate(self.nodes):
            node_pt = node.as_tuple_2d()
            segment_split = True
            while segment_split:
                segment_split = False

                for segment in self.segments:
                    line = segment.as_line_2d()
                    if (point_on_line(line, node_pt, precision=self.precision)
                            and not node in segment.nodes):
                        new_segment = segment.split(node)
                        self.segments.append(new_segment)
                        segment_split = True
                        splits_performed += 1
                        break

            if feedback is not None:
                feedback.update((index+1)/total)

        return splits_performed
