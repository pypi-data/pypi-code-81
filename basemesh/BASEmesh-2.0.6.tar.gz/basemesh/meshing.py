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

"""Mesh generation utility."""

import os
import shutil
import tempfile
from typing import Any, Collection, Dict, Iterable, List, Optional
from . import triangle
from .core import Mesh, MeshNode
from .log import logger

# Name for the node attribute used during elevation meshing via Triangle
_Z_ATTR = 'pos_z'


def elevation_mesh(nodes: Collection[triangle.PSLGNode],
                   segments: Optional[Collection[triangle.PSLGSegment]] = None,
                   *, move_tempfiles: Optional[str] = None,
                   **kwargs: Any) -> Mesh:
    """Triangulate the given input vertices and break lines.

     Generate a mesh using the given vertices. No mesh quality
    constraints will be applied. The output mesh will contain elevation
    information.

    Any excess kwargs are passed on to the Triangle.run() method.

    Parameters
    ----------
    nodes : Collection[triangle.PSLGNode]
        The set of nodes to mesh
    segments : Collection[triangle.PSLGSegment], optional
        Optional line segments connecting the nodes, by default None
    move_tempfiles : str, optional
        A directory. If provided, the temporary Triangle input and
        result files are moved to this directory instead of being
        deleted, by default None

    Returns
    -------
    Mesh
        Triangulated mesh output
    """
    logger.info('Entering elevation meshing utility')

    # Create a temporary directory to run Triangle in
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = str(temp_dir)
        logger.debug('Created temporary working directory: %s', temp_dir)
        # Run triangle
        results = triangle.Triangle().triangulate_nodes(
            nodes, segments=segments, dir_=temp_dir,
            node_attr_keys=[_Z_ATTR], **kwargs)
        # Create a mesh from the triangle result files
        mesh = _mesh_from_triangle(*results, node_attrs=[_Z_ATTR],
                                   use_matid=False,
                                   delete_input=not move_tempfiles)
        # Optionally move the tempfiles out of the temporary directory before
        # its destruction
        if move_tempfiles is not None:
            _move_tempfiles(temp_dir, move_tempfiles)
    logger.debug('Temporary working directory abandoned')

    # Take the elevation information from the node attribute and move the node
    # to its designated elevation. This converts the 2D Triangle result mesh
    # into a 2.5D elevation mesh.
    for node in mesh.nodes:
        node.move(z=float(node.attributes.pop(_Z_ATTR)))
    return mesh


def quality_mesh(nodes: Collection[triangle.PSLGNode],
                 segments: Optional[Collection[triangle.PSLGSegment]] = None,
                 holes: Optional[Iterable[triangle.HoleMarker]] = None,
                 regions: Optional[Iterable[triangle.RegionMarker]] = None, *,
                 conforming_delaunay: bool = True,
                 preserve_boundary: bool = False,
                 min_angle: Optional[float] = None,
                 max_area: Optional[float] = None,
                 move_tempfiles: Optional[str] = None,
                 **kwargs: Any) -> Mesh:
    """Advanced Meshing with mesh quality constraints applied.

    Any excess kwargs are passed on to the Triangle.run() method.

    Parameters
    ----------
    nodes : Collection[triangle.PSLGNode]
        The nodes to mesh
    segments : Collection[triangle.PSLGSegment], optional
        Optional line segments connecting the given nodse, by default
        None
    holes : Iterable[triangle.HoleMarker], optional
        Markers flagging a line-bounded region as a hole, by default
        None
    regions : Iterable[triangle.RegionMarker], optional
        Markers used to  assign attributes to their respective
        line-bounded region, by default None
    conforming_delaunay : bool, optional
        Whether to use conforming delaunay instead of contrained
        delaunay, by default True
    preserve_boundary : bool, optional
        If true, no nodes will be inserted along the mesh boundary, by
        default False
    min_angle : float, optional
        Minimum angle contraints for mesh elements, by default None
    max_area : float, optional
        Global maximum area constraint for mesh elements, by default
        None
    move_tempfiles : str, optional
        A directory. If provided, the temporary Triangle input and
        result files are moved to this directory instead of being
        deleted, by default None

    Returns
    -------
    Mesh
        The triangulated quality mesh

    Raises
    ------
    ValueError
        Raised if no breaklines or input vertices could be inferred
    """
    logger.info('Entering quality meshing utility')

    # Set up triangle flags
    flags: Dict[str, Any] = {'conforming_delaunay': conforming_delaunay,
                             'no_steiner_on_boundary': preserve_boundary}
    if max_area is not None:
        flags['max_area'] = max_area
    if min_angle is not None:
        flags['min_angle'] = min_angle
    flags.update(kwargs)
    # Ensure at least some break lines have been provided
    if not segments:
        raise ValueError('No breaklines or input vertices provided')

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = str(temp_dir)
        logger.debug('Created temporary working directory: %s', temp_dir)
        # Run triangle
        results = triangle.Triangle().triangulate_poly(
            nodes, segments, holes, regions,
            use_matid=bool(regions), dir_=temp_dir, **flags)
        # Create mesh from triangle result files
        mesh = _mesh_from_triangle(*results, use_matid=bool(regions),
                                   delete_input=not move_tempfiles)
        # Optionally move the tempfiles out of the temporary directory before
        # its destruction
        if move_tempfiles is not None:
            _move_tempfiles(temp_dir, move_tempfiles)
    logger.debug('Temporary working directory abandoned')
    return mesh


def _mesh_from_triangle(
        node_file: str, ele_file: str, node_attrs: Optional[List[str]] = None,
        use_matid: bool = True, delete_input: bool = False) -> Mesh:
    """Create a new mesh from Triangle output files.

    Note that the output mesh will not have any elevation information
    associated with its nodes whatsoever. All nodes will have the
    elevation 0.0.

    Parameters
    ----------
    node_file : str
        Path to the Triangle NODE file
    ele_file : str
        Path to the Triangle ELE file
    node_attrs : List[str], optional
        Keys used to match the positional Triangle attributes with
        named attributes, by default None
    use_matid : bool, optional
        Whether to read MATIDs from file, by default True
    delete_input : bool, optional
        Whether to dlete the input files after completion, by default
        False

    Returns
    -------
    Mesh
        A mesh generated from the Triangle output files
    """
    # Read triangle input
    pslg_nodes = triangle.triangle_io.read_nodes(node_file, node_attrs)
    pslg_elements = triangle.triangle_io.read_elements(ele_file, pslg_nodes,
                                                       use_matid=use_matid)

    nodes: Dict[int, MeshNode] = {}
    mesh = Mesh()
    for pslg_ele in pslg_elements:
        # Add element nodes to mesh
        for pslg_node in pslg_ele.nodes:
            assert pslg_node.id_ is not None
            if pslg_node.id_ in nodes.keys():
                continue
            point = (*pslg_node.as_tuple(), 0.0)
            node = mesh.add_node(point, id_=pslg_node.id_,
                                 **pslg_node.attributes)
            nodes[pslg_node.id_] = node
        # Add element
        element_nodes = tuple(
            nodes[n.id_] for n in pslg_ele.nodes)  # type: ignore
        matids = () if not use_matid else (
            (pslg_ele.matid,) if pslg_ele.matid is not None else ())
        mesh.add_element(element_nodes, pslg_ele.id_, *matids)  # type: ignore
    if delete_input:
        os.remove(node_file)
        os.remove(ele_file)
    return mesh


def _move_tempfiles(source_dir: str, target_dir: str) -> None:
    """Move the temporary Triangle files to another directory.

    All Triangle operations are performed in a temporary directory that
    is deleted after meshing. This methods moves them somewhere else
    for instrospection and debugging.

    Parameters
    ----------
    source_dir : str
        The source directory to copy the files from
    target_dir : str
        The target directory to copy the files to
    """
    logger.debug('Moving temporary Triangle files to %s', target_dir)
    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)
        shutil.move(file_path, target_dir)
