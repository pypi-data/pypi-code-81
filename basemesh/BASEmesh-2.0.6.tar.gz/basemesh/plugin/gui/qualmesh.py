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

"""Python implementation of the quality meshing GUI."""

import logging
import os
from typing import Any, Dict, Iterable, List, Optional
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QCheckBox, QComboBox, QGroupBox, QLineEdit,
                             QPlainTextEdit, QPushButton, QRadioButton,
                             QSpinBox, QTextEdit)
from qgis.core import (QgsField, QgsMeshLayer, QgsProject,  # type: ignore
                       QgsVectorLayer)
from qgis.gui import QgisInterface  # type: ignore
from ...core import Lattice
from ...feedback import Feedback
from ...meshing import quality_mesh
from ...stringdefs import write_string_defs_sidecar
from ...triangle import HoleMarker, RegionMarker
from ...types import Line2D, Point2D
from .. import utils
from .base import DialogBase

# NOTE: If the font "Courier New" is unavailable, Qt will pick a different
# monospace font based on the style hint.
_monospace_font = QFont('Courier New')
_monospace_font.setStyleHint(QFont.Monospace)


class QualMeshDialog(DialogBase):
    """GUI implementation of the quality meshing utility."""

    # NOTE: Qt widgets just have a ton of attributes - too bad!
    # pylint: disable=too-many-instance-attributes
    # Qt also uses camelCase for its attributes - too bad!
    # pylint: disable=invalid-name

    ui_file = 'ui_qualmesh.ui'
    help_file = 'help_qualmesh.md'

    def __init__(self, iface: QgisInterface) -> None:
        """Connect signal callbacks and populate widgets."""
        super().__init__(iface)  # Initialize DialogBase

        # NOTE: The following are attribute type hints used to inform supported
        # IDEs of the attribute types defined in the Qt UI file. This code is
        # executed during runtime, but does not do anything as far as the
        # Python interpreter is concerned.
        self.constraintsGroup: QGroupBox
        self.useLines: QCheckBox
        self.linesLayer: QComboBox
        self.useDivCons: QCheckBox
        self.divConsField: QComboBox
        self.usePoints: QCheckBox
        self.pointsLayer: QComboBox
        self.useGlobalMinAngle: QCheckBox
        self.globalMinAngle: QSpinBox
        self.useGlobalMaxArea: QCheckBox
        self.globalMaxArea: QSpinBox
        self.useCustomArgs: QCheckBox
        self.customArgs: QTextEdit
        self.regionsGroup: QGroupBox
        self.regionsLayer: QComboBox
        self.useHole: QCheckBox
        self.holeField: QComboBox
        self.useMatid: QCheckBox
        self.matidField: QComboBox
        self.useMaxArea: QCheckBox
        self.maxAreaField: QComboBox
        self.meshDomainGroup: QGroupBox
        self.keepConvexHull: QRadioButton
        self.shrinkToSegments: QRadioButton
        self.customBoundary: QRadioButton
        self.boundaryLayer: QComboBox
        self.stringDefGroup: QGroupBox
        self.stringDefLayer: QComboBox
        self.stringDefField: QComboBox
        self.includeInMesh: QCheckBox
        self.writeToSidecar: QCheckBox
        self.stringDefBrowseBtn: QPushButton
        self.stringDefPath: QLineEdit
        self.settingsGroup: QGroupBox
        self.logLevel: QComboBox
        self.useSnapping: QCheckBox
        self.snappingTolerance: QSpinBox
        self.outputGroup: QGroupBox
        self.filePath: QLineEdit
        self.fileBrowseBtn: QPushButton
        self.keepTempFiles: QCheckBox
        self.addToMap: QCheckBox
        self.log: QPlainTextEdit
        self.saveLogBtn: QPushButton
        self.clearLogBtn: QPushButton
        self.help: QTextEdit
        self.cancelBtn: QPushButton
        self.runBtn: QPushButton
        self.closeBtn: QPushButton

        self.log.setFont(_monospace_font)
        self.load_help(self.help)

        # Populate combo boxes
        self.add_point_layers(self.regionsLayer, self.pointsLayer)
        self.add_polyline_layers(self.linesLayer, self.stringDefLayer)

        # Hook up callbacks
        self.linesLayer.currentIndexChanged.connect(
            self._update_dividing_constraint)
        self.stringDefLayer.currentIndexChanged.connect(
            self._update_stringdef_field)
        self.saveLogBtn.clicked.connect(
            self.export_log('qualmesh', self.log))
        self.regionsLayer.currentIndexChanged.connect(
            self._update_region_attributes)
        self.stringDefBrowseBtn.clicked.connect(
            self.browse_for_output('txt', self.stringDefPath,
                                   'string-defs'))
        self.fileBrowseBtn.clicked.connect(
            self.browse_for_output('2dm', self.filePath, 'quality-mesh'))

        # Manually trigger some callbacks to pre-populate the combo boxes
        self.linesLayer.currentIndexChanged.emit(0)
        self.regionsLayer.currentIndexChanged.emit(0)
        self.stringDefLayer.currentIndexChanged.emit(0)

    def accept(self) -> None:
        """Evaluate the user's chosen settings and run the tool.

        This function runs when the user confirms their settings, its
        name may not be changed as it is tied directly into the default
        QDialog slot.
        """
        kwargs: Dict[str, Any] = {}

        # Input geometry
        points_data = self.pointsLayer.currentData()
        if self.usePoints.isChecked() and points_data is not None:
            points = list(utils.extract_points(points_data, use_z=False))
        else:
            points = []
        lines_data = self.linesLayer.currentData()
        if self.useLines.isChecked() and lines_data is not None:
            divcon_field: Optional[QgsField] = None
            if self.useDivCons.isChecked():
                divcon_field = self.divConsField.currentData()
            lines = list(utils.extract_lines(lines_data, use_z=False,
                                             divcon_field=divcon_field))
        else:
            lines = []

        # Mesh domain
        if self.shrinkToSegments.isChecked():
            boundary_lines: List[Line2D] = []
        else:
            raise NotImplementedError('Not yet implemented')
        lines.extend(boundary_lines)

        # Region markers
        region_markers: List[RegionMarker] = []
        hole_markers: List[HoleMarker] = []
        if self.regionsGroup.isChecked():
            markers_layer = self.regionsLayer.currentData()
            reg = {}
            if self.useMaxArea.isChecked():
                reg['area_field'] = self.maxAreaField.currentData()
            if self.useMatid.isChecked():
                reg['matid_field'] = self.matidField.currentData()
            if self.useHole.isChecked():
                reg['hole_field'] = self.holeField.currentData()
            region_markers, hole_markers = utils.process_markers(
                markers_layer, **reg)

        # String definitions
        stringdef_layer = self.stringDefLayer.currentData()
        if self.stringDefGroup.isChecked() and stringdef_layer is not None:
            stringdef_field = self.stringDefField.currentData()
            lines.extend(utils.extract_lines(stringdef_layer, use_z=False))
        else:
            stringdef_field = None

        # Precision
        precision = 0.0
        if self.useSnapping.isChecked():
            precision = float(10 ** int(self.snappingTolerance.value()))

        # Parameters
        max_area: float = (self.globalMaxArea.value()
                           if self.useGlobalMaxArea.isChecked() else -1.0)
        min_angle: float = (self.globalMinAngle.value()
                            if self.useGlobalMinAngle.isChecked() else -1.0)
        kwargs['custom_args'] = (self.customArgs.text()
                                 if self.useCustomArgs.isChecked() else '')
        log_level = self.logLevel.currentIndex()
        # NOTE: 0 -> Basic, 1 -> Advanced, 2-4 -> Debug 1-3
        if log_level > 0:
            kwargs['debug_level'] = log_level
            if log_level > 1:
                logging.getLogger('triangle').setLevel(logging.DEBUG)

        # Output
        output_path = self.filePath.text()
        if self.keepTempFiles.isChecked():
            kwargs['move_tempfiles'] = os.path.dirname(output_path)
        else:
            kwargs['move_tempfiles'] = None
        add_file_to_map = self.addToMap.isChecked()

        if min_angle > 0.0:
            kwargs['min_angle'] = min_angle
        if max_area > 0.0:
            kwargs['max_area'] = max_area

        def after(_: Any, error: Optional[BaseException]) -> None:
            """Run after the worker has finished.

            Parameters
            ----------
            _ : Any
                The worker's return value; discarded and unneeded
            error : Optional[BaseException]
                The error that forced the end of execution, by default
                None
            """
            if error is None and add_file_to_map:
                layer_name = os.path.basename(output_path).rsplit('.', 1)[0]
                layer = QgsMeshLayer(output_path, layer_name, 'mdal')
                QgsProject.instance().addMapLayer(layer)
            self._set_lockout(False)
            if error is not None:
                self._push_status((0.0, 'Error', False))
                self.print_error(error)

        self._set_lockout(True)
        if not self.stringDefGroup.isChecked():
            stringdef_layer = None
        self.run_worker(precision, points, lines, output_path, stringdef_layer,
                        stringdef_field, hole_markers, region_markers,
                        self.includeInMesh.isChecked(),
                        self.writeToSidecar.isChecked(),
                        self.stringDefPath.text(), log=self.log,
                        after=after, cancel_btn=self.cancelBtn, **kwargs)

    @staticmethod
    def worker(feedback: Feedback, precision: float, points: Iterable[Point2D],
               lines: Iterable[Line2D], filename: str,
               stringdefs_layer: Optional[QgsVectorLayer],
               stringdefs_field: Optional[QgsField], holes: List[HoleMarker],
               regions: List[RegionMarker], sd_mesh: bool, sd_sidecar: bool,
               sidecar_file: str, **kwargs: Any) -> None:
        """Perform the operation triggered by the dialog.

        This method is static as it will be carried out by a separate
        thread.

        Parameters
        ----------
        feedback : Feedback
            The feedback object use to communicate with the parent
            thread; this will be auto-filled internally
        precision : float
            The precision to use when generating the lattice
        points : Iterable[Tuple[float, float]]
            Input points to triangulate
        lines : Iterable[Tuple[Tuple[float, float],
                         Tuple[float, float]]]
            Input break lines to triangulate
        filename : str
            The output path of the generated mesh
        stringdefs_layer : Optional[QgsVectorLayer]
            The layer containing string definitions
        stringdefs_field : Optional[QgsField]
            The field of the stringdefs layer to use as an identifier
        holes : List[HoleMarker]
            Any hole markers found
        regions : List[RegionMarker]
            Any region markers found
        sd_mesh : bool
            Whether to write string definitions into the mesh itself
        sd_sidecar : bool
            Whether to write string definitions into a sidecare file
        sidecar_file : str
            The name of the sidecar file to write string definitions
            into
        """

        def process_input_data(precision: float, points: Iterable[Point2D],
                               lines: Iterable[Line2D], feedback: Feedback
                               ) -> Lattice:
            """Consolidate the given input geometry into a lattice.

            Parameters
            ----------
            precision : float
                The precision to use when generating the lattice
            points : Iterable[Tuple[float, float]]
                Points to add to the lattice
            lines : Iterable[Tuple[float, float], Tuple[float, float]]
                Lines to add to the lattice
            feedback : Feedback
                The feedback object used to communicate with the parent
                thread

            Returns
            -------
            Lattice
                A lattice containing the processed input data
            """
            # Instantiate lattice. This object will hold and process all of the
            # input geometries.
            lattice = Lattice(precision=precision)

            # Load input points into lattice
            with feedback.busy('Adding geometries to lattice...'):
                print('Reading points...')
                for point in points:
                    lattice.add_node((*point, 0.0), auto_conform=False)
                # Load input line segments into lattice
                print('Reading break lines...')
                for line in lines:
                    nodes = [lattice.add_node((*p, 0.0), auto_conform=False)
                             for p in line]
                    lattice.add_segment(nodes[0], nodes[1], auto_conform=False)

            # Conform input data. This removes duplicates, splits segments, etc.
            print('Conforming input geometries...')
            lattice.conform(feedback=feedback)

            return lattice

        total_steps = '2' if stringdefs_layer is None else '3'

        print('Processing input geometries\n---------------------------')
        feedback.set_prefix(f'Step 1 of {total_steps}: ')
        feedback.set_scaling(0.5)
        lattice = process_input_data(precision, points, lines, feedback)

        print('\n\nRunning Triangle\n----------------\n')
        feedback.set_prefix(f'Step 2 of {total_steps}: ')
        with feedback.busy('Running Triangle'):
            mesh = quality_mesh(*lattice.as_pslg(), holes, regions, **kwargs)

        if stringdefs_layer is not None:
            print('\n\nProcessing string definitions\n'
                  '-----------------------------\n')
            feedback.set_prefix(f'Step 3 of {total_steps}: ')
            feedback.set_scaling(0.5, 0.5)
            feedback.update(0.5, 'Processing string definitions...')
            string_defs = utils.process_string_defs(
                stringdefs_layer, stringdefs_field, mesh, precision,
                feedback=feedback)
            print(f'Found {len(string_defs)} string definitions')
            if sd_mesh:
                print('Writing node strings to mesh file...')
                for name, nodes in string_defs.items():
                    mesh.add_node_string(
                        name, [mesh.get_node_by_id(i) for i in nodes])
            if sd_sidecar:
                print('Writing node strings to sidecar file...')
                write_string_defs_sidecar(string_defs, sidecar_file)

        mesh.save(filename)

        feedback.clear_prefix()
        feedback.clear_scaling()
        feedback.update(1.0, 'Done')

    def _set_lockout(self, is_locked: bool) -> None:
        """Lock out the GUI while running the tool.

        Parameters
        ----------
        is_locked : bool
            Whether to lock or unlock the GUI
        """
        self.constraintsGroup.setEnabled(not is_locked)
        self.regionsGroup.setEnabled(not is_locked)
        self.meshDomainGroup.setEnabled(not is_locked)
        self.stringDefGroup.setEnabled(not is_locked)
        self.settingsGroup.setEnabled(not is_locked)
        self.outputGroup.setEnabled(not is_locked)
        self.runBtn.setEnabled(not is_locked)
        self.closeBtn.setEnabled(not is_locked)
        self.cancelBtn.setEnabled(is_locked)

    def _update_dividing_constraint(self) -> None:
        """Refresh the dividing constraints attribute combo box."""
        breaklines_layer = self.linesLayer.currentData()
        divcon_box = self.divConsField
        divcon_box.clear()
        if breaklines_layer is None:
            return
        for field in breaklines_layer.dataProvider().fields():
            if field.isNumeric() and field.precision() == 0:
                divcon_box.addItem(field.name())
                divcon_box.setItemData(divcon_box.count()-1, field)

    def _update_region_attributes(self) -> None:
        """Refresh the region attribute combo boxes."""
        regions_layer = self.regionsLayer.currentData()
        area_box = self.maxAreaField
        hole_box = self.holeField
        matid_box = self.matidField
        # Clear boxes
        area_box.clear()
        hole_box.clear()
        matid_box.clear()
        if regions_layer is None:
            return
        # Process fields
        for field in regions_layer.dataProvider().fields():
            if not field.isNumeric():
                continue
            area_box.addItem(field.name())
            area_box.setItemData(area_box.count()-1, field)
            if field.precision() == 0:
                hole_box.addItem(field.name())
                hole_box.setItemData(hole_box.count()-1, field)
                matid_box.addItem(field.name())
                matid_box.setItemData(matid_box.count()-1, field)

    def _update_stringdef_field(self) -> None:
        """Refresh the string def name attribute combo box."""
        stringdefs_layer = self.stringDefLayer.currentData()
        sd_box = self.stringDefField
        sd_box.clear()
        if stringdefs_layer is None:
            return
        for field in stringdefs_layer.dataProvider().fields():
            if not field.isNumeric():
                sd_box.addItem(field.name())
                sd_box.setItemData(sd_box.count()-1, field)
