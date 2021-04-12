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

"""String definition parsing and writing."""

import os
from typing import Dict, List, Mapping, Optional
from .algorithms import dist_2d, point_on_line
from .core.mesh import Mesh, MeshNode
from .feedback import Feedback
from .types import LineString2D


def _group_nodestrings(string_defs: Mapping[str, LineString2D],
                       mesh: Mesh, precision: float = 0.0, *,
                       feedback: Optional[Feedback] = None) -> Dict[str, List[MeshNode]]:
    """Return a mapping from string definition names to nodes.

    This processes all nodes in the input mesh, checking for
    coincidence with all node strings. It generates a dictionary
    mapping the string definition names to a list of nodes that are
    within range of the string definition line string.

    Parameters
    ----------
    string_defs : Mapping[str, Tuple[Tuple[str, str], ...]]
        A mapping of string definitions to line strings
    mesh : Mesh
        The mesh to process
    precision : float, optional
        The maximum distance for a node to still be considered part of
        a line string, by default 0.0
    feedback : Feedback, optional
        A feedback object used to communicate with the caller, by
        default None

    Returns
    -------
    Dict[str, List[MeshNode]]
        A mapping from string definitions to mesh nodes
    """
    if feedback is not None:
        total = len(mesh.nodes)
        interval = int(total / 100) if total > 100 else 1

    nodes_dict: Dict[str, List[MeshNode]] = {n: [] for n in string_defs}
    for index, node in enumerate(mesh.nodes):
        node_pos = node.as_tuple_2d()
        for name, line_string in string_defs.items():

            # Check each subsegment
            for sub_index, point in enumerate(line_string[:-1]):
                line = point, line_string[sub_index+1]
                if point_on_line(line, node_pos, precision=precision):
                    nodes_dict[name].append(node)
                    break

        if feedback is not None and index % interval == 0:
            feedback.update(feedback.scale(index/total, 0.7))

    return nodes_dict


def resolve_string_defs(string_defs: Dict[str, LineString2D],
                        mesh: Mesh, precision: float = 0.0, *,
                        feedback: Optional[Feedback] = None) -> Dict[str, List[int]]:
    """Resolve the string definitions for the given mesh.

    This returns the list of mesh nodes lying on the given string, in
    order of distance to the first point in the line string.

    Parameters
    ----------
    string_defs : Dict[str, Tuple[Tuple[flost, float], ...]]
        The string definitions to resolve
    mesh : Mesh
        The mesh to process
    precision : float, optional
        The maximum distance for a node to still be considered part of
        a node string, by default 0.0
    feedback : Feedback, optional
        A feedback object used to communicate with the caller, by
        default None

    Returns
    -------
    Dict[str, List[int]]
        A mapping of string definitions to mesh node IDs
    """
    # Group nodes by their matching string definition line string
    nodes_dict: Dict[str, List[MeshNode]] = _group_nodestrings(
        string_defs, mesh, precision, feedback=feedback)

    # Sort string definition nodes based on distance to their start
    _sort_nodes(string_defs, nodes_dict, feedback=feedback)

    # Return string definition dict
    return {k: [n.id_ for n in v] for k, v in nodes_dict.items()}


def _sort_nodes(string_defs: Dict[str, LineString2D],
                nodes_dict: Dict[str, List[MeshNode]], *,
                feedback: Optional[Feedback] = None) -> None:
    """Sort the string definition nodes.

    When the nodes are assigned to their respective line strings(s),
    they are in an unsecified order as determined by the mesh node
    iterator.

    This function sorts them by distance from the first node in the
    string definition line string.

    This mutates the provided nodes_dict mapping.

    Parameters
    ----------
    string_defs : Dict[str, Tuple[Tuple[float, float], ...]]
        The original, ungrouped string definitions
    nodes_dict : Dict[str, List[MeshNode]]
        The grouped string definitions with associated mesh nodes
    feedback : Feedback, optional
        A feedback object used to communicate with the caller, by
        default None
    """
    if feedback is not None:
        total = len(nodes_dict)
        interval = int(total / 100) if total > 100 else 1

    for index, element in enumerate(nodes_dict.items()):
        name, nodes = element

        def rel_dist(node: MeshNode, sd_name: str = name) -> float:
            return dist_2d(string_defs[sd_name][0], node.as_tuple_2d())

        nodes_dict[name] = sorted(nodes, key=rel_dist)

        if feedback is not None and index % interval == 0:
            feedback.update(feedback.scale(index/total, 0.3, 0.7))


def write_string_defs_mesh(string_defs: Dict[str, List[int]],
                           file_path: str) -> None:
    """Append the string definitions into a 2DM mesh file.

    This format is required for BASEMENT 3.

    Parameters
    ----------
    string_defs : Dict[str, List[int]]
        A mapping from string definitions to mesh node IDs
    file_path : str
        The path of the mesh file to append

    Raises
    ------
    FileNotFoundError
        Raised if the mesh file could not be found
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError('Unable to append string defs, path '
                                f'{file_path} does not exist')
    with open(file_path, 'a') as output:
        # HACK: Disabled readability newline for compatibility
        # output.write('\n')
        for name, node_ids in string_defs.items():
            # NOTE: According to the 2DM documentation, no more than 10 words
            # may follow the card identifier ("NS", in this case).
            # Longer node strings therefore have to be split up into multiple
            # cards. The actual end of a given node string is determined by a
            # negative node ID.
            # The insertion of the string definition name after the node string
            # end marker is out of spec.
            output.write('\nNS ')
            for index, node_id in enumerate(node_ids):
                # HACK: Disabled the max-10-tokens rule for BASEMENT
                # compatibility.
                # if (index+1) % 10 == 0:
                #     output.write('\nNS ')
                if index+1 == len(node_ids):
                    # HACK: Removed blank line between node strings
                    output.write(f'-{node_id} {name}')
                    break
                output.write(f'{node_id} ')


def write_string_defs_sidecar(string_defs: Dict[str, List[int]],
                              file_path: str) -> None:
    """Write the string definitions into a separate text file.

    This format is required for BASEMENT 2.8.

    Parameters
    ----------
    string_defs : Dict[str, List[int]]
        A mapping from string definitions to mesh node IDs
    file_path : str
        The path of the sidecar file to write
    """
    # Write string defs
    with open(file_path, 'w') as sd_file:
        for name, node_ids in string_defs.items():
            sd_file.write(f'STRINGDEF {{\n\tname = {name}\n\tnode_ids = (')
            sd_file.write(' '.join(str(i) for i in node_ids))
            sd_file.write(')\n\tupstream_direction = right\n}\n')
