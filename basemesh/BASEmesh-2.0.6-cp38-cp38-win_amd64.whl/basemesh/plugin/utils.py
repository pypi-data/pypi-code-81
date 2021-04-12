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

"""Shared utilities for common QGIS operations."""

import os
import warnings
from typing import Callable, Dict, List, Optional, Set, Tuple, Union
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QComboBox
from qgis.core import (QgsApplication, QgsFeature, QgsField,  # type: ignore
                       QgsMapLayer, QgsPoint, QgsProject, QgsVectorLayer,
                       QgsWkbTypes)
from qgis.gui import QgsMapCanvas  # type: ignore
from ..algorithms import split_line
from ..core import Mesh
from ..feedback import Feedback
from ..stringdefs import resolve_string_defs
from ..triangle import HoleMarker, RegionMarker
from ..types import Line2D, Line3D, LineString2D, Point2D, Point3D


def add_layers(canvas: QgsMapCanvas, combo_box: QComboBox, *args: QComboBox,
               filter_: Optional[Callable[[QgsMapLayer], bool]] = None,
               icon: Optional[QIcon] = None) -> None:
    """Add layers from the canvas to the given combo box.

    Parameters
    ----------
    canvas : QgsMapCanvas
        The QGIS layer canvas to process
    combo_box : QComboBox
        The combo box to populate
    filter_ : Callable[[QgsMapLayer], bool], optional
        The function used to select valid layers, by default None
    icon : QIcon, optional
        The layer icon to use for the combo box, by default None
    """
    # Create dummy filter if no filter was provided
    if filter_ is None:
        def yes_man(layer: QgsMapCanvas) -> bool:
            _ = layer  # Value intentionally discarded
            return True
        filter_ = yes_man
    # Add the combo box items
    for layer in canvas.layers():
        if filter_(layer):
            for c_box in (combo_box, *args):
                if icon is None:
                    c_box.addItem(layer.name())
                else:
                    c_box.addItem(icon, layer.name())
                # This value can be retrieved using QComboBox.currentData,
                # saving us having to manually match the layer by name later.
                c_box.setItemData(c_box.count()-1, layer)


def extract_lines(layer: QgsVectorLayer, use_z: bool = True,
                  divcon_field: QgsField = None) -> Set[Union[Line2D, Line3D]]:
    """Process the given layer and return any lines found.

    Depending on the use_z flag, the returned set will contain 2D or 3D
    lines.

    Parameters
    ----------
    layer : QgsVectorLayer
        The layer to process
    use_z : bool, optional
        Whether to return 3D or 2D lines, by default True
    divcon_field : QgsField, optional
        A dividing constraint field used to pre-segmentise lines before
        returning, by default None

    Returns
    -------
    Set[Union[Tuple[Tuple[float, float], Tuple[float, float]],
              Tuple[Tuple[float, float, float],
                    Tuple[float, float, float]]]]
        The lines found in the given layer

    Raises
    ------
    ValueError
        Raised if use_z is True for a 2D layer
    """
    if use_z and not layer_is_3d(layer):
        raise ValueError(f'Layer {layer.name()} is not a 3D layer')
    line_strings = []

    # Get individual line strings
    feature: QgsFeature
    point: Union[Point2D, Point3D]
    for feature in layer.getFeatures():
        line_string = []
        vertex: QgsPoint
        for vertex in feature.geometry().vertices():
            if use_z:
                point = vertex.x(), vertex.y(), vertex.z()
            else:
                point = vertex.x(), vertex.y()
            line_string.append(point)

        line_string = _process_divcon(line_string, feature, divcon_field)

        line_strings.append(tuple(line_string))

    # Break up line strings into unique line segments
    lines = set()
    for line_str in line_strings:
        for index, vertex in enumerate(line_str[:-1]):
            next_vertex = line_str[index+1]
            # Ignore duplicates regardless of orienation
            if not ((vertex, next_vertex) in lines
                    or (next_vertex, vertex) in lines):
                lines.add((vertex, next_vertex))
    return lines  # type: ignore


def extract_points(layer: QgsVectorLayer, use_z: bool = True
                   ) -> Set[Union[Point2D, Point3D]]:
    """Process the given geometry and return any unique points.

    If use_z is True, the returned points will return elevation
    information.

    Parameters
    ----------
    layer : QgsVectorLayer
        The layer to process
    use_z : bool, optional
        Whether to include elevation information in the returned set,
        by default True

    Returns
    -------
    Set[Union[Tuple[float, float], Tuple[float, float, float]]]
        The set of unique points found in the layer

    Raises
    ------
    ValueError
        Raised if use_z is True for a 2D layer
    """
    if use_z and not layer_is_3d(layer):
        raise ValueError(f'Layer {layer.name()} is not a 3D layer')
    points: Set[Union[Point2D, Point3D]] = set()

    feature: QgsFeature
    point: Union[Point2D, Point3D]
    for feature in layer.getFeatures():
        # NOTE: As of 3.10, QgsGeometry.asPoint() always returns a QgsPointXY
        # instances. Iterating over the feature vertices yields us QgsPoint
        # instead.
        vertex: QgsPoint
        for vertex in feature.geometry().vertices():
            if use_z:
                point = vertex.x(), vertex.y(), vertex.z()
            else:
                point = vertex.x(), vertex.y()
            points.add(point)
    return points


def get_plugin_dir() -> str:
    """Return the base directory of the QGIS plugin."""
    profile_dir = os.path.dirname(QgsApplication.qgisUserDatabaseFilePath())
    return os.path.join(profile_dir, 'python', 'plugins', 'basemesh')


def get_project_dir() -> str:
    """Return the current project directory.

    If the project has not yet been saved, the user documents folder is
    returned instead.
    """
    current_project = QgsProject.instance()
    # Return the project directory if it has been saved
    project_dir = str(current_project.absolutePath())
    if project_dir:
        return project_dir
    # Otherwise, return the user documents folder
    if os.name == 'nt':
        user_docs = os.path.expandvars('%USERPROFILE%')
    elif os.name == 'posix':
        user_docs = os.path.expanduser('~')
    else:
        raise RuntimeError(f'Unsupported OS: {os.name}')
    user_docs = os.path.join(user_docs, 'Documents')
    return user_docs


def get_project_title() -> str:
    """Return the current project title.

    If the current project does not have a title specified, its base
    name (i.e. file name without extension) will be used instead.
    If the file has not been saved, the default title "Project1" is
    returned instead.
    """
    project = QgsProject().instance()
    # Return the project's title, if it exists
    if project.title():
        return str(project.title())
    # If not title has been specified, use the project's base name instead
    if project.baseName():
        return str(project.baseName())
    # Use the default file name instead
    default_name = 'Project1'
    project.setTitle(default_name)
    return default_name


def layer_is_3d(layer: QgsVectorLayer) -> bool:
    """Return whether the given layer contains elevation data.

    Parameters
    ----------
    layer : QgsVectorLayer
        The layer to check

    Returns
    -------
    bool
        Whether the layer contains elevation data
    """
    wkb_type = layer.dataProvider().wkbType()
    return bool(QgsWkbTypes.hasZ(wkb_type))


def _process_divcon(line_string: List[Union[Point2D, Point3D]],
                    feat: QgsFeature, divcon_field: QgsField = None
                    ) -> List[Union[Point2D, Point3D]]:
    """Process the dividing constraints in the given line string.

    Parameters
    ----------
    line_string : List[Union[Tuple[float, float],
                             Tuple[float, float, float]]]
        The line string to segmentise
    feat : QgsFeature
        The QGIS feature to check for field values
    divcon_field : QgsField, optional
        The QGIS field to use for segmentisation, by default None

    Returns
    -------
    List[Union[Tuple[float, float], Tuple[float, float, float]]]
        The segmentised line string
    """
    # If no dividing constraint field has been specified, do nothing
    if divcon_field is None:
        return line_string

    # Ensure the dividing constraint field has a sensible value
    attr_index = feat.fields().indexFromName(divcon_field.name())
    segments = int(feat.attributes()[attr_index])
    if segments < 2:
        # No segment -> no splitting required
        return line_string

    # Split every line in the line string into (divcon) elements
    return split_line(line_string, segments)  # type: ignore


def process_markers(layer: QgsVectorLayer, *, area_field: QgsField = None,
                    hole_field: QgsField = None, matid_field: QgsField = None
                    ) -> Tuple[List[RegionMarker], List[HoleMarker]]:
    """Process the given markers layer and return any markers found.

    Parameters
    ----------
    layer : QgsVectorLayer
        The layer to process
    area_field : QgsField, optional
        The max_area field to use, by default None
    hole_field : QgsField, optional
        The is_hole field to use, by default None
    matid_field : QgsField, optional
        The matid field to use, by default None

    Returns
    -------
    Tuple[List[RegionMarker], List[HoleMarker]]
        A list of region and hole markers found in the layer

    Raises
    ------
    ValueError
        Raised if the input layer is not a point layer
    """
    if layer.geometryType() != QgsWkbTypes.PointGeometry:
        raise ValueError(f'Layer "{layer.name()}" is not a point layer')
    holes = []
    regions = []
    for feat in layer.getFeatures():
        if feat.geometry().type() == QgsWkbTypes.PointGeometry:
            point: QgsPoint = feat.geometry().asPoint()
            pos_x, pos_y = point.x(), point.y()

            # Hole flag
            is_hole = False
            if hole_field is not None:
                attr_index = feat.fields().indexFromName(hole_field.name())
                is_hole = bool(feat.attributes()[attr_index])
                if is_hole:
                    holes.append(HoleMarker(pos_x, pos_y))

            # Maximum area constraint
            max_area = -1.0
            if area_field is not None:
                attr_index = feat.fields().indexFromName(area_field.name())
                max_area = feat.attributes()[attr_index]
            if is_hole and max_area is not None and max_area > 0.0:
                warnings.warn(f'Point {(pos_x, pos_y)} marks a hole, its '
                              f'max area ({max_area}) will have no effect')
            # MATID
            matid = 0
            if matid_field is not None:
                attr_index = feat.fields().indexFromName(matid_field.name())
                matid = feat.attributes()[attr_index]
                if matid is None:
                    matid = 0
            if is_hole and matid is not None:
                warnings.warn(f'Point {(pos_x, pos_y)} marks a hole, its '
                              f'MATID ({matid}) will have no effect')

            if max_area > 0.0 or matid > 0:
                regions.append(RegionMarker(pos_x, pos_y, max_area=max_area,
                                            attribute=matid))
    return regions, holes


def process_string_defs(layer: QgsVectorLayer, id_field: QgsField, mesh: Mesh,
                        precision: float = 0.0, *,
                        feedback: Optional[Feedback] = None
                        ) -> Dict[str, List[int]]:
    """Write the string definitions for the given mesh.

    Parameters
    ----------
    layer : QgsVectorLayer
        The layer containing the string definitions
    id_field : QgsField
        The layer field to use as the string definition name/ID
    mesh : Mesh
        The mesh used to process the line strings
    precision : float, optional
        The maximum distance between a point and its string definition,
        by default 0.0
    feedback : Feedback, optional
        A feedback option used to communicate with the caller, by
        default None

    Returns
    -------
    Dict[str, List[int]]
        A dictionary mapping string definitions to their node IDs
    """
    string_def_lines: Dict[str, LineString2D] = {}
    feature: QgsFeature
    for feature in layer.getFeatures():
        # Get string ID field
        attr_index = feature.fields().indexFromName(id_field.name())
        name = feature.attributes()[attr_index]
        line_string: List[Point2D] = []
        # Add vertices
        vertex: QgsPoint
        for vertex in feature.geometry().vertices():
            line_string.append((vertex.x(), vertex.y()))
        string_def_lines[name] = tuple(line_string)
    return resolve_string_defs(string_def_lines, mesh, precision,
                               feedback=feedback)
