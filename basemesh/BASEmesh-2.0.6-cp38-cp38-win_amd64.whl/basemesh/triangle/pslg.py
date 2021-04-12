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

"""Objects related to Triangle geometries.

This mainly covers the 2D equivalent of mesh objects like nodes,
line segments and mesh elements.

All objects defined herein are prefixed with "PSLG" to differentiate
them from their 3D equivalents used throughout the rest of BASEmesh.
"""

from collections import OrderedDict
from typing import Any, Dict, List, Optional, Tuple


class PSLGNode:
    """A two-dimensional PSLG node for use in Triangle."""

    __slots__ = ('_attributes', '_id', '_pos_x', '_pos_y')

    def __init__(self, pos_x: float, pos_y: float, **kwargs: Any) -> None:
        """Instantiate a new PSLG node.

        Note that the default initializer is mostly intended for
        specifying the input parameters for triangulation.
        Nodes read from a Triangle .node-file will be parsed by the
        from_string factory method, which will also populate the ID.
        The ID of manually initialized nodes will be None.

        Extra keyword arguments will be stored along with the node and
        can be used to preserve node information during triangulation,
        such as the Z-coordinates of 3D points.

        Parameters
        ----------
        pos_x : float
            X position of the node
        pos_y : float
            Y position of the node
        """
        self._id: Optional[int] = kwargs.pop('_init_set_id', None)
        self._attributes = OrderedDict(
            sorted(kwargs.items(), key=lambda x: x[0].lower()))
        self._pos_x = pos_x
        self._pos_y = pos_y

    @classmethod
    def from_string(cls, string: str, *, use_boundary: bool = False,
                    column_names: Optional[List[str]] = None) -> 'PSLGNode':
        """Parse a Triangle output line and return a node.

        The optional column_names kwarg can be used to restore the
        attribute names stored along with the node. If this list is not
        provided, attribute names will be generated as "Attr_1",
        "Attr_2", etc.

        Parameters
        ----------
        string : str
            The string to parse
        use_boundary : bool, optional
            Whether boundary markers were included in the line; set
            this to True, by default False
        column_names : List[str], optional
            Names used to resolve the positional node attributes in the
            string to named attributes, by default None

        Returns
        -------
        PSLGNode
            The node represented by the string

        Raises
        ------
        ValueError
            Raised if the number of attributes in column_names is less
            than the number of attribute values found
        """
        # NOTE: Node table format:
        # <Node ID> <X> <Y> [<Attr 1> <Attr 2> ...] [<boundary>]
        words = string.split()
        id_ = int(words[0])
        pos = tuple(float(words[i]) for i in range(1, 3))
        attr_values = words[3:-1] if use_boundary else words[3:]
        # Find/set attribute names
        if column_names is None:
            column_names = [f'Attr_{i+1}' for i, _ in enumerate(attr_values)]
        else:
            column_names = sorted(column_names)
            if len(column_names) != len(attr_values):
                raise ValueError(f'{len(column_names)} column names provided '
                                 f'but {len(attr_values)} values encountered')
        attr_dict = {a: attr_values[i] for i, a in enumerate(column_names)}
        # Instantiate and return the node
        instance = cls(pos[0], pos[1], _init_set_id=id_, **attr_dict)
        return instance

    @property
    def attributes(self) -> Dict[str, str]:
        """Return a dict of values that were stored with the node."""
        return self._attributes

    @property
    def id_(self) -> Optional[int]:
        """Return the unique ID for this node.

        Note that this will only return a valid integer for nodes that
        were read from Triangle output files. Manually defined nodes
        will instead return None.
        """
        return self._id

    def as_tuple(self) -> Tuple[float, float]:
        """Return the coordinates of the node as a tuple of floats."""
        return self._pos_x, self._pos_y


class PSLGSegment:
    """A two-dimensional PSLG segment for use in Triangle."""

    __slots__ = ('_end', '_id', '_start')

    def __init__(self, start: PSLGNode, end: PSLGNode, **kwargs: Any) -> None:
        """Initialise a new PSLG segment.

        Note that the default initializer is mostly intended for
        specifying the input parameters for triangulation.
        Segments read from a Triangle .poly-file will be parsed by
        the from_string factory method, which will also populate the
        ID. The ID of manually initialized segments will be None.

        Parameters
        ----------
        start : PSLGNode
            The starting node of the segment
        end : PSLGNode
            The end node of the segment

        Raises
        ------
        ValueError
            Raised if any unexpected keyword arguments are passed
        """
        self._end = end
        self._id: Optional[int] = kwargs.pop('_init_set_id', None)
        self._start = start
        # NOTE: No keyword argeuments beyond the internal initializer are
        # supported
        if kwargs:
            raise ValueError(
                f'Unexpected keyword argument {next(iter(kwargs))}')

    @classmethod
    def from_points(cls, start_point: Tuple[float, ...],
                    end_point: Tuple[float, ...], *,
                    nodes: Optional[List[PSLGNode]] = None) -> 'PSLGSegment':
        """Create a new segment from the given points.

         Note that only the first two dimensions of the input points
        will be honoured, any additional coordinates are ignored.

        As with the default constructor, the ID will always be None.

        Parameters
        ----------
        start_point : Tuple[float, ...]
            The coordinates of the beginning of the line
        end_point : Tuple[float, ...]
            The coordinates of the end of the line
        nodes : List[PSLGNode], optional
            An optional list of nodes to check the start and end point
            against; if they match, they will be used instead of a new
            node being created, by default None

        Returns
        -------
        PSLGSegment
            The segment that was created
        """
        start = None
        end = None
        if nodes is not None:
            # Search the nodes input list for the given input points
            for node in nodes:
                if start_point[:2] == node.as_tuple():
                    start = node
                if end_point[:2] == node.as_tuple():
                    end = node
                # If both points have been matched to nodes, exit the loop
                if start is not None and end is not None:
                    break
        # Create new nodes for any points that could not be matched to existing
        # nodes
        if start is None:
            # Add Z attribute if possible
            if len(start_point) > 2:
                start = PSLGNode(*start_point[:2], pos_z=start_point[2])
            else:
                start = PSLGNode(*start_point[:2])
            if nodes is not None:
                nodes.append(start)
        if end is None:
            # Add Z attribute if possible
            if len(end_point) > 2:
                end = PSLGNode(*end_point[:2], pos_z=end_point[2])
            else:
                end = PSLGNode(*end_point[:2])
            if nodes is not None:
                nodes.append(end)
        return PSLGSegment(start, end)

    @classmethod
    def from_string(cls, string: str, nodes: List[PSLGNode]) -> 'PSLGSegment':
        """Parse a Triangle output line and return a segment.

        Parameters
        ----------
        string : str
            The string to parse
        nodes : List[PSLGNode]
            The sorted list of nodes to link the segment to

        Returns
        -------
        PSLGSegment
            The segment represented by the string
        """
        # NOTE: Segment table format:
        # <Segment ID> <Node #1 ID> <Node #2 ID> [<boundary>]
        words = string.split()
        id_ = int(words[0])
        node_ids = tuple(int(i) for i in range(1, 3))
        segment_nodes = [nodes[i] for i in node_ids]
        # Instantiate and return the segment
        return cls(segment_nodes[0], segment_nodes[1], _init_set_id=id_)

    @property
    def end(self) -> PSLGNode:
        """Return the node defining the end of the segment."""
        return self._end

    @property
    def id_(self) -> Optional[int]:
        """Return the unique ID of this segment.

        Note that this will only return a valid integer for segments
        that were read from Triangle output files. Manually defined
        segments will instead return None.
        """
        return self._id

    @property
    def as_tuple(self) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """Return the start and end point as two tuples of floats."""
        return self.start.as_tuple()[:2], self.end.as_tuple()[:2]

    @property
    def start(self) -> PSLGNode:
        """Return the node defining the start of the segment."""
        return self._start


class PSLGElement:
    """A two-dimensional PSLG element for use in Triangle."""

    __slots__ = ('_id', '_matid', '_node1', '_node2', '_node3')

    def __init__(self, node1: PSLGNode, node2: PSLGNode, node3: PSLGNode,
                 matid: Optional[int] = None, **kwargs: Any) -> None:
        """Initialise a new PSLG element.

        Note that the default initializer is mostly intended for
        specifying the input parameters for triangulation.
        Elements read from a Triangle .ele-file will be parsed by the
        from_string factory method, which will also populate the ID.
        The ID of manually initialized elements will be None.

        Parameters
        ----------
        node1 : PSLGNode
            The first node of the element
        node2 : PSLGNode
            The second node of the element
        node3 : PSLGNode
            The third node of the element
        matid : int, optional
            The material ID for this element, by default None
        """
        self._id: Optional[int] = kwargs.pop('_init_set_id', None)
        self._matid = matid
        self._node1 = node1
        self._node2 = node2
        self._node3 = node3

    @classmethod
    def from_string(cls, string: str, nodes: List[PSLGNode], *,
                    use_matid: bool = True) -> 'PSLGElement':
        """Parse a Triangle output line and return an element.

        If use_matid is True, this will expect a MATID column in the
        line.

        Returns
        -------
        PSLGElement
            The element represented by the string

        Raises
        ------
        ValueError
            Raised if use_matid is True but no MATID could be found
        """
        # NOTE: Element table format:
        # <Element ID> <N#1 ID> <N#2 ID> <N#3 ID> [<Attr>]
        words = string.split()
        id_ = int(words[0])
        node_ids = tuple(int(words[n]) for n in range(1, 4))
        element_nodes = [nodes[i] for i in node_ids]
        if use_matid:
            try:
                attr_dict = {'matid': int(words[4])}
            except IndexError as err:
                raise ValueError('Missing element attribute') from err
        else:
            attr_dict = {}
        # Instantiate and return the element
        instance = cls(element_nodes[0], element_nodes[1], element_nodes[2],
                       _init_set_id=id_, **attr_dict)
        return instance

    @property
    def id_(self) -> Optional[int]:
        """Return the unique ID for this element.

        Note that this will only return a valid integer for elements
        that were read from Triangle output files. Manually defined
        elements will instead return None.
        """
        return self._id

    @property
    def matid(self) -> Optional[int]:
        """Return the material ID of the element."""
        return self._matid

    @property
    def nodes(self) -> Tuple[PSLGNode, PSLGNode, PSLGNode]:
        """Return the nodes defining the element."""
        return self._node1, self._node2, self._node3
