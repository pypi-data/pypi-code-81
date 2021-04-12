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

"""Python implementation of the elevation meshing GUI."""

import os
from typing import Any, Dict, Iterable, Optional
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QCheckBox, QComboBox, QGroupBox, QLineEdit,
                             QPlainTextEdit, QPushButton, QRadioButton,
                             QSpinBox, QTextEdit)
from qgis.core import QgsMeshLayer, QgsProject  # type: ignore
from qgis.gui import QgisInterface  # type: ignore
from ...core import Lattice
from ...feedback import Feedback
from ...meshing import elevation_mesh
from ...types import Line3D, Point3D
from .. import utils
from .base import DialogBase


# NOTE: If the font "Courier New" is unavailable, Qt will pick a different
# monospace font based on the style hint.
_monospace_font = QFont('Courier New')
_monospace_font.setStyleHint(QFont.Monospace)


class ElevMeshDialog(DialogBase):
    """GUI implementation of the elevation meshing utility."""

    # NOTE: Qt widgets just have a ton of attributes - too bad!
    # pylint: disable=too-many-instance-attributes
    # Qt also uses camelCase for its attributes - too bad!
    # pylint: disable=invalid-name

    ui_file = 'ui_elevmesh.ui'
    help_file = 'help_elevmesh.md'

    def __init__(self, iface: QgisInterface) -> None:
        """Connect signal callbacks and populate widgets.

        Parameters
        ----------
        iface : QgisInterface
            The QGIS interface to create the dialog for
        """
        super().__init__(iface)  # Initialize DialogBase

        # NOTE: The following are attribute type hints used to inform supported
        # IDEs of the attribute types defined in the Qt UI file. This code is
        # executed during runtime, but does not do anything as far as the
        # Python interpreter is concerned.
        self.constraintsGroup: QGroupBox
        self.useLines: QCheckBox
        self.linesLayer: QComboBox
        self.usePoints: QCheckBox
        self.pointsLayer: QComboBox
        self.meshDomainGroup: QGroupBox
        self.keepConvexHull: QRadioButton
        self.shrinkToSegments: QRadioButton
        self.customBoundary: QRadioButton
        self.boundaryLayer: QComboBox
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
        self.status.setText('Ready')

        # Populate combo boxes
        self.linesLayer.clear()
        self.pointsLayer.clear()
        self.boundaryLayer.clear()
        self.add_polyline_layers(self.linesLayer, has_z=True)
        self.add_point_layers(self.pointsLayer, has_z=True)
        self.add_polygon_layers(self.boundaryLayer)

        # Hook up callbacks
        self.fileBrowseBtn.clicked.connect(
            self.browse_for_output('2dm', self.filePath, 'elevation-mesh'))
        self.saveLogBtn.clicked.connect(
            self.export_log('elevmesh', self.log))

        # Disabled features
        self.customBoundary.setEnabled(False)

    def accept(self) -> None:
        """Evaluate the user's chosen settings and run the tool.

        This function runs when the user confirms their settings, its
        name may not be changed as it is tied directly into the default
        QDialog slot.
        """
        kwargs: Dict[str, Any] = {}

        # Input geometry
        lines_data = self.linesLayer.currentData()
        if self.useLines.isChecked() and lines_data is not None:
            lines = list(utils.extract_lines(lines_data))
        else:
            lines = []
        points_data = self.pointsLayer.currentData()
        if self.usePoints.isChecked() and points_data is not None:
            points = list(utils.extract_points(points_data))
        else:
            points = []

        # Mesh domain
        if self.keepConvexHull.isChecked():
            kwargs['keep_convex_hull'] = True
        # Settings
        log_level = self.logLevel.currentIndex()
        kwargs['debug_level'] = log_level
        precision = 0.0
        if self.useSnapping.isChecked():
            precision = float(10 ** self.snappingTolerance.value())
        # Output
        filename = self.filePath.text()
        if self.keepTempFiles.isChecked():
            kwargs['move_tempfiles'] = os.path.dirname(filename)
        add_to_map = self.addToMap.isChecked()

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
            if error is None and add_to_map:
                layer_name = os.path.basename(filename).rsplit('.', 1)[0]
                layer = QgsMeshLayer(filename, layer_name, 'mdal')
                QgsProject.instance().addMapLayer(layer)
            self._set_lockout(False)
            if error is not None:
                self._push_status((0.0, 'Error', False))
                self.print_error(error)

        self._set_lockout(True)
        self.run_worker(precision, points, lines, filename,
                        log=self.log, after=after,
                        cancel_btn=self.cancelBtn, **kwargs)

    @staticmethod
    def worker(feedback: Feedback, precision: float, points: Iterable[Point3D],
               lines: Iterable[Line3D], filename: str, **kwargs: Any) -> None:
        """Perform the actual work of this utility.

        Any keyword arguments are passed on to the elevation_mesh
        function.

        Parameters
        ----------
        feedback : Feedback
            The feedback object use to communicate with the parent
            thread; this will be auto-filled internally
        precision : float
            The precision to use when generating the lattice
        points : Iterable[Tuple[float, float, float]]
            Input points to triangulate
        lines : Iterable[Tuple[float, float, float],
                         Tuple[float, float, float]]
            Input break lines to triangulate
        filename : str
            The output path of the generated mesh
        """

        def process_input_data(precision: float, points: Iterable[Point3D],
                               lines: Iterable[Line3D], feedback: Feedback
                               ) -> Lattice:
            """Consolidate the given input geometry into a lattice.

            Parameters
            ----------
            precision : float
                The precision to use when generating the lattice
            points : Iterable[Tuple[float, float, float]]
                Points to add to the lattice
            lines : Iterable[Tuple[float, float, float],
                            Tuple[float, float, float]]
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
                    lattice.add_node(point, auto_conform=False)
                # Load input line segments into lattice
                print('Reading break lines...')
                for line in lines:
                    nodes = [lattice.add_node(p, auto_conform=False)
                             for p in line]
                    lattice.add_segment(nodes[0], nodes[1], auto_conform=False)

            # Conform input data. This removes duplicates, splits segments, etc.
            print('Conforming input geometries...')
            lattice.conform(feedback=feedback)

            return lattice

        print('Processing input geometries\n---------------------------')
        feedback.set_prefix('Step 1 of 2: ')
        lattice = process_input_data(precision, points, lines, feedback)

        feedback.set_prefix('Step 2 of 2: ')
        print('\n\nRunning Triangle\n----------------\n')
        with feedback.busy('Running Triangle'):
            mesh = elevation_mesh(*lattice.as_pslg(), **kwargs)

        mesh.save(filename, num_materials=0)
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
        self.meshDomainGroup.setEnabled(not is_locked)
        self.settingsGroup.setEnabled(not is_locked)
        self.outputGroup.setEnabled(not is_locked)
        self.closeBtn.setEnabled(not is_locked)
        self.runBtn.setEnabled(not is_locked)
        self.cancelBtn.setEnabled(is_locked)
