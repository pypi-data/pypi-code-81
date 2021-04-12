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

"""Legacy BASEmesh geometry converter module.

This module defines processing algorithms that convert the geometries
in BASEmesh v1.4 to their respective BASEmesh v2 format.
"""

from typing import Any, Dict, List, Optional
from qgis.core import (QgsFeature, QgsFeatureSink, QgsField,  # type: ignore
                       QgsLineString, QgsPoint, QgsProcessing,
                       QgsProcessingAlgorithm, QgsProcessingContext,
                       QgsProcessingException, QgsProcessingFeedback,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterField,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterVectorLayer, QgsVectorLayer,
                       QgsWkbTypes)
from ....algorithms import point_within_range
from ....types import Point3D
from ..utils import parse_docstring


class LegacyLineTo3DLine(QgsProcessingAlgorithm):
    """Converts 2D lines to 3D lines using an auxiliary point layer.

    The elevation of the vertices of each line in the input layer will
    be set to those of the corresponding point in the points layer.

    The snapping tolerance parameter can be used to account for poorly
    aligned points. It will not deduplicate the input lines or perform
    any form of clean-up.

    This can be used to convert input data used for BASEmesh 1.X to the
    format expected by BASEmesh 2.
    """

    # Parameter literals

    INPUT_LINES_LAYER = 'INPUT_LINES_LAYER'
    INPUT_POINTS_LAYER = 'INPUT_POINTS_LAYER'
    INPUT_POINTS_FIELD = 'INPUT_POINTS_FIELD'
    PRECISION = 'PRECISION'
    OUTPUT = 'OUTPUT'

    # Constructor

    @classmethod
    def createInstance(cls) -> 'LegacyLineTo3DLine':
        """Return a new copy of the algorithm."""
        return cls()

    # QGIS properties

    @staticmethod
    def name() -> str:
        """Return the unique algorithm name."""
        return 'convertersconvertlegacylayerline'

    @staticmethod
    def displayName() -> str:
        """Return the user-facing algorithm name."""
        return 'Convert legacy layer (Line)'

    @staticmethod
    def group() -> str:
        """Return the localised name of the algorithm group."""
        return 'Converters'

    @staticmethod
    def groupId() -> str:
        """Return the unique group ID for the algorithm."""
        return 'converters'

    @classmethod
    def shortHelpString(cls) -> str:
        """Return a short help string for the algorithm."""
        return parse_docstring(cls.__doc__)

    def initAlgorithm(self, _: Optional[Dict[str, Any]] = None) -> None:
        """Define the algorithm's inputs and outputs."""
        # Input lines layer
        self.addParameter(QgsProcessingParameterVectorLayer(
            name=self.INPUT_LINES_LAYER,
            description='2D input line layer',
            types=[QgsProcessing.TypeVectorLine]))
        # Input points layer
        self.addParameter(QgsProcessingParameterVectorLayer(
            name=self.INPUT_POINTS_LAYER,
            description='2D input point layer',
            types=[QgsProcessing.TypeVectorPoint]))
        # Input points field
        self.addParameter(QgsProcessingParameterField(
            name=self.INPUT_POINTS_FIELD,
            description='Elevation attribute of the points layer',
            parentLayerParameterName=self.INPUT_POINTS_LAYER,
            type=QgsProcessingParameterField.Numeric))
        # Snapping tolerance
        self.addParameter(QgsProcessingParameterNumber(
            name=self.PRECISION,
            description='Snapping tolerance (exponent)',
            defaultValue=-6,
            minValue=-10,
            maxValue=0))
        # Output
        self.addParameter(QgsProcessingParameterFeatureSink(
            name=self.OUTPUT,
            description='3D output line layer',
            type=QgsProcessing.TypeVectorLine))

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

        Raises
        ------
        QgsProcessingException
            Raised if a line vertex does not match any input point
        """
        lines_layer: QgsVectorLayer = self.parameterAsVectorLayer(
            parameters, self.INPUT_LINES_LAYER, context)
        points_layer: QgsVectorLayer = self.parameterAsVectorLayer(
            parameters, self.INPUT_POINTS_LAYER, context)
        points_field: QgsField = self.parameterAsFields(
            parameters, self.INPUT_POINTS_FIELD, context)[0]
        exponent = int(self.parameterAsDouble(
            parameters, self.PRECISION, context))
        precision = 10 ** exponent
        sink, dest_id = self.parameterAsSink(
            parameters, self.OUTPUT, context, fields=lines_layer.fields(),
            geometryType=QgsWkbTypes.LineStringZ, crs=lines_layer.crs())

        # Read input points
        anchors: List[Point3D] = []
        feat: QgsFeature
        for feat in points_layer.getFeatures():
            # Report status
            if feedback.isCanceled():
                break

            point = feat.geometry().asPoint()
            attr_index = feat.fields().indexFromName(points_field)
            elevation = float(feat.attributes()[attr_index])
            anchors.append((*point, elevation))  # type: ignore

        # Process lines

        feature_count = lines_layer.featureCount()

        old_feat: QgsFeature
        for index, old_feat in enumerate(lines_layer.getFeatures()):
            # Report status
            if feedback.isCanceled():
                break
            feedback.setProgress(int(100*feature_count/(index+1)))

            # Iterate over the points in the (poly-) line
            line_string: List[QgsPoint] = []
            vertex: QgsPoint
            for vertex in old_feat.geometry().vertices():

                # Match point to anchors
                point_2d = vertex.x(), vertex.y()
                found_point: Optional[Point3D] = None
                for anchor in anchors:
                    if point_within_range(point_2d, anchor[:2], precision):
                        found_point = vertex.x(), vertex.y(), anchor[2]
                        break
                if found_point is None:
                    raise QgsProcessingException(
                        f'Unable to match line vertex {point_2d} to an '
                        'elevated point given the precision')

                line_string.append(QgsPoint(*point))

            # Add the 3D line string
            new_feat = QgsFeature()
            new_feat.setGeometry(QgsLineString(line_string))
            new_feat.setAttributes(old_feat.attributes())
            sink.addFeature(new_feat, QgsFeatureSink.FastInsert)

        feedback.setProgress(100)

        return {self.OUTPUT: dest_id}


class LegacyPointTo3DPoint(QgsProcessingAlgorithm):
    """Converts 2D points with elevation attributes to 3D points.

    This algorithm reads each point in the input layer and creates a
    corresponding point in the output.

    The X and Y coordinates are copied from the source point, the Z
    coordinate will be read from the attribute provided.

    This can be used to convert input data used for BASEmesh 1.X to the
    format expected by BASEmesh 2.
    """

    # Parameter literals

    INPUT_LAYER = 'INPUT_LAYER'
    INPUT_FIELD = 'INPUT_FIELD'
    OUTPUT = 'OUTPUT'

    # Constructor

    @classmethod
    def createInstance(cls) -> 'LegacyPointTo3DPoint':
        """Return a new copy of the algorithm."""
        return cls()

    # QGIS properties

    @staticmethod
    def name() -> str:
        """Return the unique algorithm name."""
        return 'convertersconvertlegacylayerpoint'

    @staticmethod
    def displayName() -> str:
        """Return the user-facing algorithm name."""
        return 'Convert legacy layer (Point)'

    @staticmethod
    def group() -> str:
        """Return the localised name of the algorithm group."""
        return 'Converters'

    @staticmethod
    def groupId() -> str:
        """Return the unique group ID for the algorithm."""
        return 'converters'

    @classmethod
    def shortHelpString(cls) -> str:
        """Return a short help string for the algorithm."""
        return parse_docstring(cls.__doc__)

    def initAlgorithm(self, _: Optional[Dict[str, Any]] = None) -> None:
        """Define the algorithm's inputs and outputs."""
        # Input layer
        self.addParameter(QgsProcessingParameterVectorLayer(
            name=self.INPUT_LAYER,
            description='2D input point layer',
            types=[QgsProcessing.TypeVectorPoint]))
        # Input field
        self.addParameter(QgsProcessingParameterField(
            name=self.INPUT_FIELD,
            description='Elevation attribute of the input layer',
            parentLayerParameterName=self.INPUT_LAYER,
            type=QgsProcessingParameterField.Numeric))
        # Output
        self.addParameter(QgsProcessingParameterFeatureSink(
            name=self.OUTPUT,
            description='3D output point layer',
            type=QgsProcessing.TypeVectorPoint))

    def processAlgorithm(self, parameters: Dict[str, Any],
                         context: QgsProcessingContext,
                         feedback: QgsProcessingFeedback) -> Dict[str, Any]:
        """Execute the algorithm using the given parameters."""
        input_layer: QgsVectorLayer = self.parameterAsVectorLayer(
            parameters, self.INPUT_LAYER, context)
        input_field: QgsField = self.parameterAsFields(
            parameters, self.INPUT_FIELD, context)[0]
        sink, dest_id = self.parameterAsSink(
            parameters, self.OUTPUT, context, fields=input_layer.fields(),
            geometryType=QgsWkbTypes.PointZ, crs=input_layer.crs())

        # Retrieve a list of all 3D points in the layer
        feature_count = input_layer.featureCount()

        old_feat: QgsFeature
        for index, old_feat in enumerate(input_layer.getFeatures()):
            # Report status
            if feedback.isCanceled():
                break
            feedback.setProgress(int(100*feature_count/(index+1)))

            # Process old feature
            point = old_feat.geometry().asPoint()
            attr_index = old_feat.fields().indexFromName(input_field)
            elevation = old_feat.attributes()[attr_index]

            # Add new feature
            new_feat = QgsFeature()
            new_feat.setGeometry(QgsPoint(*point, elevation))
            new_feat.setAttributes(old_feat.attributes())
            sink.addFeature(new_feat, QgsFeatureSink.FastInsert)

        feedback.setProgress(100)

        return {self.OUTPUT: dest_id}
