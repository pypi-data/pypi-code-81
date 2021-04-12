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

"""Algorithms related to MATID visualisation and modification."""

from typing import Any, Dict, List, Optional, Tuple
from PyQt5.QtCore import QVariant
from qgis import processing  # type: ignore
from qgis.core import (QgsFeature, QgsFeatureSink, QgsField,  # type: ignore
                       QgsFields, QgsGeometry, QgsMeshLayer, QgsPointXY,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterDefinition,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterField,
                       QgsProcessingParameterFileDestination,
                       QgsProcessingParameterMeshLayer,
                       QgsProcessingParameterVectorLayer, QgsProcessing,
                       QgsProcessingContext, QgsProcessingFeedback,
                       QgsTriangle, QgsVectorLayer, QgsWkbTypes)
from ...core.mesh import Mesh, MeshElement
from ...types import Polygon2D
from .utils import parse_docstring


class AssignMaterialID(QgsProcessingAlgorithm):
    """Assign element MATIDs based on containment in a polygon."""

    # Parameter literals

    INPUT_MESH = 'INPUT_MESH'
    INPUT_POLYGON = 'INPUT_POLYGON'
    MATID_FIELD = 'MATID_FIELD'
    OUTPUT = 'OUTPUT'

    # Constructor

    @classmethod
    def createInstance(cls) -> 'AssignMaterialID':
        """Return a new copy of the algorithm."""
        return cls()

    # QGIS properties

    @staticmethod
    def name() -> str:
        """Return the unique algorithm name."""
        return 'assignmaterialid'

    @staticmethod
    def displayName() -> str:
        """Return the user-facing algorithm name."""
        return 'Assign MATID'

    @classmethod
    def shortHelpString(cls) -> str:
        """Return a short help string for the algorithm."""
        return parse_docstring(cls.__doc__)

    def initAlgorithm(self, _: Optional[Dict[str, Any]] = None) -> None:
        """Define the algorithm's inputs and outputs."""
        # Input mesh
        self.addParameter(QgsProcessingParameterMeshLayer(
            name=self.INPUT_MESH,
            description='Mesh layer'))
        # Input polygon
        self.addParameter(QgsProcessingParameterVectorLayer(
            name=self.INPUT_POLYGON,
            description='Input polygons',
            types=[QgsProcessing.TypeVectorPolygon]))
        # Polygon MATID field
        self.addParameter(QgsProcessingParameterField(
            name=self.MATID_FIELD,
            description='MATID field to apply to the mesh',
            parentLayerParameterName=self.INPUT_POLYGON,
            type=QgsProcessingParameterField.Numeric))
        # Output
        self.addParameter(QgsProcessingParameterFileDestination(
            name=self.OUTPUT,
            description='Output mesh layer',
            fileFilter='SMS 2D mesh (*2dm)'))

    def processAlgorithm(self, parameters: Dict[str, Any],
                         context: QgsProcessingContext,
                         feedback: QgsProcessingFeedback) -> Dict[str, Any]:
        """Execute the algorithm using the given parameters.

        Parameters
        ----------
        parameters : Dict[str, Any]
            The parameters defined for this algorithm
        context : QgsProcessingContext
            The context in which the algorithm is run
        feedback : QgsProcessingFeedback
            The feedback object to use for status reporting

        Returns
        -------
        Dict[str, Any]
            The algorithms output parameters
        """
        input_mesh_layer: QgsMeshLayer = self.parameterAsMeshLayer(
            parameters, self.INPUT_MESH, context)
        mesh = Mesh.open(input_mesh_layer.source())
        input_polygon_layer: QgsVectorLayer = self.parameterAsVectorLayer(
            parameters, self.INPUT_POLYGON, context)
        input_field: QgsField = self.parameterAsFields(
            parameters, self.MATID_FIELD, context)[0]
        output_file = self.parameterAsFileOutput(
            parameters, self.OUTPUT, context)

        # Extract polygons
        polygons: List[Tuple[int, Polygon2D]] = []
        feature: QgsFeature
        for feature in input_polygon_layer.getFeatures():
            attr_index = feature.fields().indexFromName(input_field)
            matid = int(feature.attributes()[attr_index])
            polygon = []
            for vertex in feature.geometry().vertices():
                polygon.append((vertex.x(), vertex.y()))
            polygons.append((matid, polygon))  # type: ignore

        # Modify and save the mesh
        elements: List[MeshElement]
        for matid, polygon in polygons:  # type: ignore
            elements = mesh.elements_by_polygon(polygon)  # type: ignore
            for element in elements:
                element.materials = (matid,)
        mesh.save(output_file)

        feedback.setProgress(100)
        return {self.OUTPUT: output_file}


class ExtractMaterialID(QgsProcessingAlgorithm):
    """Create MultiPolygon geometries from the mesh Material IDs.

    This will group the mesh elements by their assigned MATID and write
    a MultiPolgon layer with the corresponding MATID as its attribute.
    """

    # Parameter literals

    INPUT = 'INPUT'
    _TEMP = 'TEMP_OUTPUT'
    OUTPUT = 'OUTPUT'

    # Constructor

    @classmethod
    def createInstance(cls) -> 'ExtractMaterialID':
        """Return a new copy of the algorithm."""
        return cls()

    # QGIS properties

    @staticmethod
    def name() -> str:
        """Return the unique algorithm name."""
        return 'extractmaterialid'

    @staticmethod
    def displayName() -> str:
        """Return the user-facing algorithm name."""
        return 'Extract MATID'

    @classmethod
    def shortHelpString(cls) -> str:
        """Return a short help string for the algorithm."""
        return parse_docstring(cls.__doc__)

    def initAlgorithm(self, _: Optional[Dict[str, Any]] = None) -> None:
        """Define the algorithm's inputs and outputs."""
        # Input layer
        self.addParameter(QgsProcessingParameterMeshLayer(
            name=self.INPUT,
            description='Mesh layer'))
        # Temporary sink
        temp_sink = QgsProcessingParameterFeatureSink(
            name='TEMP_OUTPUT',
            description='Internal sink for intermediate algorithms',
            type=QgsProcessing.TypeVectorPolygon,
            defaultValue='memory:',
            optional=True)
        hidden_flag = QgsProcessingParameterDefinition.FlagHidden
        temp_sink.setFlags(temp_sink.flags() | hidden_flag)
        self.addParameter(temp_sink)
        # Output
        self.addParameter(QgsProcessingParameterFeatureSink(
            name=self.OUTPUT,
            description='Output polygon layer',
            type=QgsProcessing.TypeVectorPolygon))

    def processAlgorithm(self, parameters: Dict[str, Any],
                         context: QgsProcessingContext,
                         feedback: QgsProcessingFeedback) -> Dict[str, Any]:
        """Execute the algorithm using the given parameters.

        Parameters
        ----------
        parameters : Dict[str, Any]
            The parameters defined for this algorithm
        context : QgsProcessingContext
            The context in which the algorithm is run
        feedback : QgsProcessingFeedback
            The feedback object to use for status reporting

        Returns
        -------
        Dict[str, Any]
            The algorithms output parameters
        """
        MATID_FIELD = 'MATID'
        COUNT_FIELD = 'Element count'

        mesh_layer: QgsMeshLayer = self.parameterAsMeshLayer(
            parameters, self.INPUT, context)
        mesh = Mesh.open(mesh_layer.source())

        fields = QgsFields()
        fields.append(QgsField(MATID_FIELD, type=QVariant.Int))
        fields.append(QgsField(COUNT_FIELD, type=QVariant.Int))
        temp_sink, temp_dest_id = self.parameterAsSink(
            parameters, self._TEMP, context, fields=fields,
            geometryType=QgsWkbTypes.MultiPolygon, crs=mesh_layer.crs())

        # Group mesh elements by MATID
        grouped: Dict[int, List[MeshElement]] = {}
        for element in mesh.elements:
            matid = int(element.materials[0])
            try:
                grouped[matid].append(element)
            except KeyError:
                grouped[matid] = [element]

        # Collect geometries for all elements
        for matid, elements in grouped.items():
            element_count = len(elements)
            for element in elements:
                geom = QgsGeometry(QgsTriangle(
                    *[QgsPointXY(*p[:2]) for p in element.points]))
                feat = QgsFeature()
                feat.setGeometry(geom)
                feat.setAttributes([matid, element_count])
                temp_sink.addFeature(feat, QgsFeatureSink.FastInsert)

        feedback.setProgress(50)

        # Dissolve layer
        dissolve_results = processing.run(
            'native:dissolve',
            {'INPUT': temp_dest_id,
             'FIELD': [MATID_FIELD],
             'OUTPUT': parameters[self.OUTPUT]},
            is_child_algorithm=True,
            context=context,
            feedback=feedback)

        return {self.OUTPUT: dissolve_results['OUTPUT']}
