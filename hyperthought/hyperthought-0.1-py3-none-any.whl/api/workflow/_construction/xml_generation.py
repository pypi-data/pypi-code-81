"""
xml_generation.py

Create XML for elements on a single canvas, given suitable JSON inputs.
"""

from collections import defaultdict
from enum import IntEnum
import uuid
from xml.etree.ElementTree import (
    Element, SubElement, tostring
)


BUFFER = 100
MAX_JITTER = BUFFER // 2
JITTER_STEP = 10
PROCESS_WIDTH = 80
PROCESS_HEIGHT = 80
WORKFLOW_WIDTH = 120
WORKFLOW_HEIGHT = 60

# Width delta between adjacent elements in a row or column.
# (Amount to add to get from one element to the next.)
ADD_WIDTH = max(PROCESS_WIDTH, WORKFLOW_WIDTH) + BUFFER
ADD_HEIGHT = max(PROCESS_HEIGHT, WORKFLOW_HEIGHT) + BUFFER

NAME_KEY = 'name'
TYPE_KEY = 'type'
COLUMN_KEY = 'column'
ROW_KEY = 'row'
ID_KEY = 'id'
CLIENT_ID_KEY = 'client_id'
SUCCESSORS_KEY = 'successors'

PROCESS_TYPE = 'process'
WORKFLOW_TYPE = 'workflow'

PROCESS_STYLE = "rounded=0;whiteSpace=wrap;html=1;"
WORKFLOW_STYLE = "shape=process;whiteSpace=wrap;html=1;"
EDGE_STYLE = "edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;jettySize=auto;orthogonalLoop=1;"


# This will only be used for edges and empty cells.
# Nodes need to correspond to database objects, so the client ids will be
# precomputed.
get_client_id = lambda: str(uuid.uuid4())


class _JitterGenerator:
    def __init__(self):
        self._values = []

        for jitter in range(0, MAX_JITTER, JITTER_STEP):
            self._values.append(jitter)
            if jitter: self._values.append(-jitter)

        self._n_values = len(self._values)
        self._current_index = 0

    def next(self):
        value = self._values[self._current_index]
        self._current_index = (self._current_index + 1) % self._n_values
        return value


class _JitterManager:
    """
    Generate jitter values based on least recent use in a given row or column.
    """

    def __init__(self):
        self._generators = {
            'rows': defaultdict(_JitterGenerator),
            'columns': defaultdict(_JitterGenerator)
        }

    def next(self, is_row, row_or_column_number):
        """
        Get the next available jitter value.

        Parameters
        ----------
        is_row : bool
            True if jitter is being generated for a line between rows,
            False otherwise.
        row_or_column_number : int
            The logical row above or column to the left of the line.

        Returns
        -------
        A jitter value.
        """        
        key = 'rows' if is_row else 'columns'
        return self._generators[key][row_or_column_number].next()


def _get_x(logical_column):
    """
    Translate logical to absolute x position for a node.

    This will be the position of the top left corner.
    """
    return BUFFER + ADD_WIDTH * logical_column


def _get_y(logical_row):
    """
    Translate logical to absolute y position for a node.

    This will be the position of the top left corner.
    """
    return BUFFER + ADD_HEIGHT * logical_row


def _get_port_y(node):
    """
    Get the absolute y position of a port for a node.

    Ports (edge connection points) will be halfway from top to bottom.
    """
    if node[TYPE_KEY] == PROCESS_TYPE:
        half_height = PROCESS_HEIGHT // 2
    elif node[TYPE_KEY] == WORKFLOW_TYPE:
        half_height = WORKFLOW_HEIGHT // 2
    else:
        raise Exception(f"Invalid type detected: {node[TYPE_KEY]}")

    return _get_y(logical_row=node[ROW_KEY]) + half_height


def _get_first_edge_x(source_node):
    """
    Get the absolute x position of the first intermediate point in an edge.

    The first point in an edge (one that isn't straight across, that is)
    will to the right of the node, halfway between the between-column buffer.
    (That is, a half-buffer to the left of the next column.)
    """
    return _get_x(logical_column=source_node[COLUMN_KEY] + 1) - BUFFER // 2


def _get_between_edge_y(source_node):
    """
    Get the absolute y position of the second point in an edge connecting
    nodes in non-adjacent columns.

    Edges will always drop to go around in-between columns.

    This will be a half-buffer above the next row down.
    """
    return _get_y(logical_row=source_node[ROW_KEY] + 1) - BUFFER // 2


def _get_last_edge_x(target_node):
    """
    Get the absolute x position of the last intermediate point in an edge.

    The last point in an edge (one that isn't straight across, that is)
    will to the left of the target, halfway between the between-column buffer.
    (That is, a half-buffer to the left of the node's x position.)
    """
    return _get_x(logical_column=target_node[COLUMN_KEY]) - BUFFER // 2


def _create_node(node, parent_id):
    """
    Create an element for a process or workflow.

    Parameters
    ----------
    node : dict
        Input dict containing name, type, and logical coordinates.
    parent_id : dict
        ID of parent element.  (Note that this element will *NOT* contain
        the process in the XML.)

    Returns
    -------
    An XML element representing the process.
    """
    if node[TYPE_KEY] == PROCESS_TYPE:
        style = PROCESS_STYLE
        width = PROCESS_WIDTH
        height = PROCESS_HEIGHT
    elif node[TYPE_KEY] == WORKFLOW_TYPE:
        style = WORKFLOW_STYLE
        width = WORKFLOW_WIDTH
        height = WORKFLOW_HEIGHT
    else:
        raise Exception(f"Invalid type encountered: {node[TYPE_KEY]}")

    cell_element = Element('mxCell', {
        'id': node[CLIENT_ID_KEY],
        'value': node[NAME_KEY],
        'style': style,
        'parent': parent_id,
        'vertex': '1',
    })

    SubElement(cell_element, 'mxGeometry', {
        'x': str(_get_x(logical_column=node[COLUMN_KEY])),
        'y': str(_get_y(logical_row=node[ROW_KEY])),
        'width': str(width),
        'height': str(height),
        'as': 'geometry',
    })

    return cell_element


def _create_edge(source_node, target_node, parent_id, jitter_manager):
    """Create an edge between two nodes in the workflow."""
    cell_element = Element('mxCell', {
        'id': get_client_id(),
        'style': EDGE_STYLE,
        'edge': '1',
        'parent': parent_id,
        'source': source_node[CLIENT_ID_KEY],
        'target': target_node[CLIENT_ID_KEY],
    })

    geometry_element = SubElement(cell_element, 'mxGeometry', {
        'relative': '1',
        'as': 'geometry',
    })

    # Add an array of points as needed.
    # This will always be done, event if the nodes are in the same row and
    # adjacent columns.  The reason is that the line across will not be
    # straight if the nodes have different types.

    source_logical_row = source_node[ROW_KEY]
    source_logical_column = source_node[COLUMN_KEY]
    target_logical_column = target_node[COLUMN_KEY]
    assert source_logical_column < target_logical_column, (
        "The source node for an edge should be to the left of the "
        "target node.")

    # Add the array element.
    array_element = SubElement(geometry_element, 'Array', {'as': 'points'})

    # Add the first point to the array.
    jitter = jitter_manager.next(
        is_row=False,
        row_or_column_number=source_logical_column,
    )
    first_x = _get_first_edge_x(source_node) + jitter
    SubElement(array_element, 'mxPoint', {
        'x': str(first_x),
        'y': str(_get_port_y(source_node)),
    })
    last_y = _get_port_y(target_node)

    if source_logical_column == target_logical_column - 1:
        SubElement(array_element, 'mxPoint', {
            'x': str(first_x),
            'y': str(last_y),
        })
    else:   # Need to cross over columns.
        jitter = jitter_manager.next(
            is_row=True,
            row_or_column_number=source_logical_row,
        )
        second_y = _get_between_edge_y(source_node) + jitter
        SubElement(array_element, 'mxPoint', {
            'x': str(first_x),
            'y': str(second_y),
        })
        jitter = jitter_manager.next(
            is_row=False,
            row_or_column_number=target_logical_column - 1,
        )
        last_x = _get_last_edge_x(target_node) + jitter
        SubElement(array_element, 'mxPoint', {
            'x': str(last_x),
            'y': str(second_y),
        })
        SubElement(array_element, 'mxPoint', {
            'x': str(last_x),
            'y': str(last_y),
        })

    return cell_element


def _create_edges(logical_children, parent_id):
    """Create all edges for the workflow."""
    child_map = {
        child[ID_KEY]: child
        for child in logical_children
    }

    edges = []
    jitter_manager = _JitterManager()

    for source_node in logical_children:
        if SUCCESSORS_KEY not in source_node:
            continue

        for target_id in source_node[SUCCESSORS_KEY]:
            target_node = child_map[target_id]
            edge = _create_edge(
                source_node=source_node,
                target_node=target_node,
                parent_id=parent_id,
                jitter_manager=jitter_manager,
            )
            edges.append(edge)

    return edges
        

def create_xml(logical_children):
    """
    Create XML structure for workflow canvas.

    Parameters
    ----------
    logical_children : list of dict
        Dictionaries for processes/workflows to put on the canvas.
        Expected keys include 'id', 'name', 'type', 'successors', 'row', and
        'column'.

    Return
    ------
    An XML tree containing all needed elements.
    """
    # Scan the children to find maximum row and column.
    # Also add client ids.
    max_row = 0
    max_column = 0

    for child in logical_children:
        if child[ROW_KEY] > max_row:
            max_row = child[ROW_KEY]
        
        if child[COLUMN_KEY] > max_column:
            max_column = child[COLUMN_KEY]

    # Convert from 0-based indexing to counts.
    row_count = max_row + 1
    column_count = max_column + 1

    dx = BUFFER + ADD_WIDTH * column_count
    dy = BUFFER + ADD_HEIGHT * row_count

    graph_element = Element('mxGraphModel', {
        'dx': str(dx),
        'dy': str(dy),
        'grid': '1',
        'gridSize': '10',
        'guides': '1',
        'tooltips': '1',
        'connect': '1',
        'arrows': '1',
        'fold': '1',
        'page': '1',
        'pageScale': '1',
        'pageWidth': '850',
        'pageHeight': '1100',
        'background': '#ffffff'
    })

    root_element = SubElement(graph_element, 'root')

    empty_id = get_client_id()
    SubElement(root_element, 'mxCell', {'id': empty_id})

    parent_id = get_client_id()
    SubElement(root_element, 'mxCell', {
        'id': parent_id,
        'parent': empty_id,
    })

    # Add nodes.
    root_element.extend([
        _create_node(child, parent_id)
        for child in logical_children
    ])

    # Add edges.
    edges = _create_edges(
        logical_children=logical_children,
        parent_id=parent_id,
    )
    root_element.extend(edges)

    # Return the root node.
    return graph_element
