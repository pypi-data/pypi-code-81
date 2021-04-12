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

"""Reader and writer functions for triangle input/output formats."""

import datetime
import warnings
from typing import Callable, Collection, Iterable, List, Optional, Set, TypeVar
from .log import logger
from .markers import HoleMarker, RegionMarker
from .pslg import PSLGElement, PSLGNode, PSLGSegment

# Generic type variable used for type-hinting _create_consecutive_list
T = TypeVar('T')


def read_elements(filename: str, nodes: List[PSLGNode],
                  use_matid: bool = True) -> List[PSLGElement]:
    """Read an output ELE file and return a list of elements.

    Parameters
    ----------
    filename : str
        The file to process
    nodes : List[PSLGNode]
        The sorted list of nodes for these elements
    use_matid : bool, optional
        Whether to expect a material ID field, by default True

    Returns
    -------
    List[PSLGElement]
        The list of elements found in the file
    """
    logger.debug('Reading %s', filename)
    with open(filename) as input_file:
        elements: List[PSLGElement] = []
        ele_count: int
        line: str
        for line in input_file:
            line = line.strip()
            # Ignore blank lines
            if line == '':
                continue
            # Ignore comments
            if line.startswith('#'):
                continue
            # File header
            try:
                _ = ele_count
            except NameError:
                ele_count = int(line.split()[0])
                continue
            # File contents
            elements.append(PSLGElement.from_string(
                line, nodes, use_matid=use_matid))
    if len(elements) != ele_count:
        warnings.warn(f'{ele_count} elements expected, got {len(elements)}')
    return elements


def read_nodes(filename: str, attr_names: Optional[List[str]] = None
               ) -> List[PSLGNode]:
    """Read an output NODE file and return a list of nodes.

    Parameters
    ----------
    filename : str
        The file to process
    attr_names : List[str], optional
        If node attributes were specified before triangulation, you can
        use this list to restore the original attribute names, by
        default None

    Returns
    -------
    List[PSLGNode]
        The list of nodes found in the file
    """
    logger.debug('Reading %s', filename)
    with open(filename) as input_file:
        nodes: List[PSLGNode] = []
        node_count: int
        use_boundary: bool

        line: str
        for line in input_file:
            line = line.strip()
            # Ignore blank lines
            if line == '':
                continue
            # Ignore comments
            if line.startswith('#'):
                continue
            # File header
            try:
                _ = node_count
            except NameError:
                words = line.split()
                node_count = int(words[0])
                use_boundary = bool(int(words[3]))
                continue
            # File contents
            nodes.append(PSLGNode.from_string(
                line, use_boundary=use_boundary, column_names=attr_names))
    if len(nodes) != node_count:
        warnings.warn(f'{node_count} nodes expected, got {len(nodes)}')
    return nodes


def write_nodes(filename: str, nodes: Collection[PSLGNode], *,
                ignore_existing_ids: bool = True,
                node_attr_keys: Optional[List[str]] = None) -> None:
    """Write an input NODE file from a set of input nodes.

    By default, this function will assign random node IDs upon writing.
    You can prevent this by setting the ignore_existing_ids kwarg to
    False, which will cause an error if the highest ID exceeds the
    number of provided nodes. This is due to "Triangle" expecting
    consecutive ID numbering without jumps, which cannot be achieved in
    this case.

    Parameters
    ----------
    filename : str
        The file to write
    nodes : Collection[PSLGNode]
        The nodes to write to file
    ignore_existing_ids : bool, optional
        Whether to write the existing node IDs, otherwise they will be
        numbered sequentially upon writing, by default True
    node_attr_keys : List[str], optional
        The list of noe attribute keys to write to file, by default
        None

    Raises
    ------
    ValueError
        Raised if the number of nodes is insufficient to generate a
        consecutive list of ascending node IDs. This can only occur if
        ignore_existing_ids is enabled.
    """
    logger.debug('Writing %s', filename)
    # pylint: disable=import-outside-toplevel
    from . import __version__ as module_version
    # Process the input nodes to consolidate all node attributes
    max_id = 0
    for node in nodes:
        if (not ignore_existing_ids
                and node.id_ is not None
                and node.id_ > max_id):
            max_id = node.id_
    # Check node.id_ count
    if nodes and len(nodes) <= max_id:
        raise ValueError('Unable to retain existing IDs: The highest ID '
                         f'encountered ({max_id}) exceeds the number of nodes '
                         f'provided ({len(nodes)})')

    # Write output file
    with open(filename, 'w') as output_file:
        # Custom file header comment
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        output_file.write(f'# Triangle NODE file\n# Generated {now} using '
                          f'"BASEmesh Triangle Wrapper" v{module_version}\n\n')
        # Node information header
        attr_count = 0 if node_attr_keys is None else len(node_attr_keys)
        output_file.write('# Vertex count | Dimension | Attribute count | '
                          f'Use boundary markers\n{len(nodes)} 2 '
                          f'{attr_count} 0\n')
        # Node table header
        output_file.write('# Vertex ID | X | Y')
        if node_attr_keys:
            output_file.write(f' | {" | ".join(node_attr_keys)}')
        output_file.write('\n')

        # Node table contents
        if ignore_existing_ids:
            # Use arbitrary node order
            sorted_nodes = list(nodes)
        else:
            # Split nodes into fixed ID and random ID
            sorted_nodes = _create_consecutive_list(nodes)
        for index, node in enumerate(sorted_nodes):
            output_file.write(
                f'{index} {node.as_tuple()[0]} {node.as_tuple()[1]}')
            if node_attr_keys:
                attr_list = []
                for attr in node_attr_keys:
                    try:
                        val = float(node.attributes[attr])
                    except KeyError:
                        attr_list.append('0')
                    except ValueError:
                        # Silently ignore any attributes that cannot be
                        # converted to float
                        pass
                    else:
                        if val.is_integer():
                            val = int(val)
                        attr_list.append(str(val))
                output_file.write(f' {" ".join(attr_list)}')
            output_file.write('\n')


def write_poly(filename: str, *, nodes: Optional[Collection[PSLGNode]] = None,
               segments: Optional[Collection[PSLGSegment]] = None,
               holes: Optional[Collection[HoleMarker]] = None,
               regions: Optional[Collection[RegionMarker]] = None,
               node_attr_keys: Optional[List[str]] = None,
               include_area: bool = True,
               include_matid: bool = True,
               ignore_existing_ids: bool = True) -> None:
    """Write an input POLY file from the given input data.

    As segments are also defined through nodes, they may be sufficient
    for triangulation, even without any explicit nodes specified.
    nodes is therefore a kwarg as well, although the total number of
    nodes (both explicitly defined ones and ones inferred through
    segments) must not be zero.

    By default, this function will assign random object IDs upon
    writing. You can prevent this by setting the ignore_existing_ids
    kwarg to False, which will cause an error if the highest ID
    exceeds the number of provided objects. This is due to "Triangle"
    expecting consecutive ID numbering without jumps, which cannot be
    achieved in this case.

    Parameters
    ----------
    filename : str
        The file to write
    nodes : Collection[PSLGNode], optional
        The nodes to write to file, by default None
    segments : Collection[PSLGSegment], optional
        The segments to write to file, by default None
    holes : Collection[HoleMarker], optional
        Any hole markers to include, by default None
    regions : Collection[RegionMarker], optional
        Any region markers to include, by default None
    node_attr_keys : List[str], optional
        The keys in the node attribute dicts to write, by default None
    include_area : bool, optional
        Whether to write region area markers, by default True
    include_matid : bool, optional
        Whether to write region attributes, by default True
    ignore_existing_ids : bool, optional
        Whether to keep existing node IDs or regenerate them, by
        default True

    Raises
    ------
    ValueError
        Raised if no nodes were specified or inferrable via segments
    ValueError
        Raised if the number of objects was insufficient to keep
        existing node IDs when writing
    """
    logger.debug('Writing %s', filename)
    # pylint: disable=import-outside-toplevel
    from . import __version__ as module_version
    # Process the input segments and merge their nodes with the ones provided
    node_set: Set[PSLGNode] = set()
    if segments is not None:
        for segment in segments:
            node_set.update((segment.start, segment.end))
    if nodes is not None:
        node_set.update(nodes)
    if not node_set:
        raise ValueError('No nodes were specified and none could be inferred '
                         'from segments')
    # Process the nodes to consolidate all node attributes
    max_node_id = 0
    for node in node_set:
        if (not ignore_existing_ids
                and node.id_ is not None
                and node.id_ > max_node_id):
            max_node_id = node.id_
    # Check node.id_ count
    if not ignore_existing_ids and node_set and len(node_set) <= max_node_id:
        raise ValueError('Unable to retain existing node IDs: The highest '
                         f'node ID encountered ({max_node_id}) exceeds the '
                         f'number of nodes provided ({len(node_set)})')
    # Check segment ids
    max_segment_id = 0
    if segments is not None:
        for segment in segments:
            if (not ignore_existing_ids
                    and segment.id_ is not None
                    and segment.id_ > max_segment_id):
                max_segment_id = segment.id_
    if segments and len(segments) <= max_segment_id:
        raise ValueError('Unable to retain existing segment IDs: The highest '
                         f'segment ID encountered ({max_segment_id}) exceeds '
                         f'the number of segments provided ({len(segments)})')

    # Write output file
    with open(filename, 'w') as output_file:
        # Custom file header comment
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        output_file.write(f'# Triangle POLY file\n# Generated {now} using '
                          f'"BASEmesh Triangle Wrapper" v{module_version}\n\n')

        # Node information header
        node_key_count = 0 if node_attr_keys is None else len(node_attr_keys)
        output_file.write('# Vertex count | Dimension | Attribute count | '
                          f'Use boundary markers\n{len(node_set)} 2 '
                          f'{node_key_count} 0\n')
        # Node table header
        output_file.write('# Vertex ID | X | Y')
        if node_attr_keys:
            output_file.write(f' | {" | ".join(node_attr_keys)}')
        output_file.write('\n')

        # Node table contents
        if ignore_existing_ids:
            # Use arbitrary node order
            sorted_nodes = list(node_set)
        else:
            sorted_nodes = _create_consecutive_list(node_set)
        for index, node in enumerate(sorted_nodes):
            output_file.write(
                f'{index} {node.as_tuple()[0]} {node.as_tuple()[1]}')
            if node_attr_keys:
                attr_list = []
                for attr in node_attr_keys:
                    try:
                        val = float(node.attributes[attr])
                    except KeyError:
                        attr_list.append('0')
                    except ValueError:
                        # Silently ignore any attributes that cannot be
                        # converted to float
                        pass
                    else:
                        if val.is_integer():
                            val = int(val)
                        attr_list.append(str(val))
                output_file.write(f' {" ".join(attr_list)}')
            output_file.write('\n')

        # Segment information header
        output_file.write('\n# Segment count | Use boundary markers\n')
        if segments:
            output_file.write(str(len(segments)))
        else:
            output_file.write('0')
        output_file.write(' 0\n')
        if segments:
            # Segment table header
            output_file.write('# Segment ID | Start node | End node')
            output_file.write('\n')
            # Segment table contents
            for index, segment in enumerate(segments):
                start_node = sorted_nodes.index(segment.start)
                end_node = sorted_nodes.index(segment.end)
                output_file.write(f'{index} {start_node} {end_node}')
                output_file.write('\n')

        # Hole information header
        output_file.write('\n# Hole count\n')
        if holes:
            output_file.write(str(len(holes)))
        else:
            output_file.write('0')
        output_file.write('\n')

        if holes:
            # Hole table header
            output_file.write('# Hole ID | X | Y\n')
            # Hole table contents
            for index, hole in enumerate(holes):
                output_file.write(
                    f'{index} {hole.as_tuple()[0]} {hole.as_tuple()[1]}\n')

        # Region information header
        output_file.write('\n# Region count\n')
        if regions:
            output_file.write(str(len(regions)))
        else:
            output_file.write('0')
        output_file.write('\n')

        if regions:
            # Region table header
            output_file.write('# Region ID | X | Y')
            if include_matid:
                output_file.write(' | MATID')
            if include_area:
                output_file.write(' | Max area')
            output_file.write('\n')
            # Region table contents
            for index, region in enumerate(regions):
                output_file.write(
                    f'{index} {region.as_tuple()[0]} {region.as_tuple()[1]}')
                if include_matid:
                    output_file.write(f' {region.attribute}')
                if include_area:
                    output_file.write(f' {region.max_area}')
                output_file.write('\n')


def _create_consecutive_list(
        iterable: Iterable[T], *,
        key: Optional[Callable[[T], Optional[int]]] = None) -> List[T]:
    """Process the input list and create a key-sorted copy of it.

    This function will take the elements from the input list and group
    them by the given key, which is expected to be an optional integer.

    It then creates a new list with all non-None key values being
    placed at the appropriate index and the others placed randomly to
    "fill the gaps".

    Parameters
    ----------
    iterable : Iterable[T]
        The iterable to process
    key : Callable[[T], Optional[int]], optional
        Th key to use for sorting; this may return either None or an
        integer key less than the number of elements in the iterable,
        by default None

    Returns
    -------
    List[T]
        A list sorted by the given key
    """
    # Create fallback function if key is undefined
    if key is None:

        def key_(item: T) -> Optional[int]:
            """Return the id of the given object."""
            assert hasattr(item, 'id_')
            val: Optional[int] = item.id_  # type: ignore
            return val

        key = key_
    # Group the input elements into filler and non-filler values
    filler_values = []
    fixed_values = {}
    for item in iterable:
        if key(item) is None:
            filler_values.append(item)
        else:
            fixed_values[key(item)] = item
    # Create a sorted list while filling in the gaps
    output_list = []
    for index, _ in enumerate(iterable):
        if index in fixed_values:
            # Add the item at its appropriate index
            output_list.append(fixed_values[index])
        else:
            # Add a random item to pad the list
            output_list.append(filler_values.pop(0))
    return output_list
