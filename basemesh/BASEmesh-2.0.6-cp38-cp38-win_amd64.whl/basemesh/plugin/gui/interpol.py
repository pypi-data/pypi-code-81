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

"""Python implementation of the mesh interpolation GUI."""

import os
from typing import Any, List, Optional, Tuple, Union
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QCheckBox, QComboBox, QGroupBox, QLineEdit,
                             QListWidget, QListWidgetItem, QPushButton,
                             QRadioButton, QTabWidget, QTextEdit)
from qgis.core import (QgsMapLayerType, QgsMeshLayer,  # type: ignore
                       QgsProject, QgsRasterLayer)
from qgis.gui import QgisInterface  # type: ignore
from ...abc import ElevationSource
from ...core import Mesh
from ...feedback import Feedback
from ...interpolation import calculate_element_elevation, interpolate_mesh
from ..raster import RasterDataWrapper
from .base import DialogBase

# This is a custom type hint used to refer to mesh layers and tuples of a
# raster layer and its corresponding band index.
_ElevLayer = List[Union[QgsMeshLayer, Tuple[QgsRasterLayer, int]]]


class InterpolDialog(DialogBase):
    """GUI implementaiton of the interpolation utility."""

    # NOTE: Qt widgets just have a ton of attributes - too bad!
    # pylint: disable=too-many-instance-attributes
    # Qt also uses camelCase for its attributes - too bad!
    # pylint: disable=invalid-name

    ui_file = 'ui_interpol.ui'
    help_file = 'help_interpol.md'

    def __init__(self, iface: QgisInterface) -> None:
        """Connect signal callbacks and populate widgets."""
        super().__init__(iface)  # Initialize DialogBase

        # NOTE: The following are attribute type hints used to inform supported
        # IDEs of the attribute types defined in the Qt UI file. This code is
        # executed during runtime, but does not do anything as far as the
        # Python interpreter is concerned.
        self.inputGroup: QGroupBox
        self.layer: QComboBox
        self.tabWidget: QTabWidget
        self.useMeshSource: QRadioButton
        self.meshSource: QComboBox
        self.useRasterSource: QRadioButton
        self.rasterSource: QComboBox
        self.rasterBand: QComboBox
        self.selectedList: QListWidget
        self.availableList: QListWidget
        self.help: QTextEdit
        self.outputGroup: QGroupBox
        self.format: QComboBox
        self.filePath: QLineEdit
        self.fileBrowseBtn: QPushButton
        self.addToMap: QCheckBox
        self.cancelBtn: QPushButton
        self.runBtn: QPushButton
        self.closeBtn: QPushButton

        self._use_advanced = False
        self.load_help(self.help)

        # Populate list widgets
        self._layers_cache: _ElevLayer = []
        self._set_available_layers()  # Populate list widgets

        # Populate combo boxes
        self.add_mesh_layers(self.layer, self.meshSource)
        self.add_raster_layers(self.rasterSource)

        # Hook up callbacks
        self.tabWidget.currentChanged.connect(self._tab_switched)
        self.rasterSource.currentIndexChanged.connect(
            self._update_raster_bands)
        self.fileBrowseBtn.clicked.connect(
            self.browse_for_output('2dm', self.filePath, 'computational-mesh'))

        # Manually trigger some callbacks to pre-populate the combo boxes
        self.rasterSource.currentIndexChanged.emit(0)

    def accept(self) -> None:
        """Evaluate the user's chosen settings and run the tool.

        This function runs when the user confirms their settings, its
        name may not be changed as it is tied directly into the default
        QDialog slot.
        """
        # Input layer
        target_layer = self.layer.currentData()

        # NOTE: The following list contains the elevation sources to be used
        # for interpolation in descending order of priority.
        sources: List[ElevationSource] = []

        # Advanced mode
        if self._use_advanced:
            for list_item in self._get_list_selection():
                # Mesh layer
                if isinstance(list_item, QgsMeshLayer):
                    layer: QgsMeshLayer = list_item
                    filename = layer.source()
                    sources.append(Mesh.open(filename))
                # Raster layer
                else:
                    layer, band_index = list_item
                    sources.append(RasterDataWrapper(layer, band_index))

        # Basic mode
        else:
            # Use elevation mesh
            if self.useMeshSource.isChecked():
                layer = self.meshSource.currentData()
                sources = [Mesh.open(layer.source())]
            # Use raster data
            else:
                layer = self.rasterSource.currentData()
                band_index = self.rasterBand.currentData()
                sources = [RasterDataWrapper(layer, band_index)]

        # Output
        output_path = self.filePath.text()
        format_value = self.format.currentIndex()
        output_bm2 = output_bm3 = False
        if format_value != 1:
            output_bm2 = True
        if format_value >= 1:
            output_bm3 = True
        add_file_to_map = self.addToMap.isChecked()

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
            # Add file to map
            if error is None and add_file_to_map:
                name, _ = tuple(os.path.basename(output_path).rsplit('.', 1))
                layer = QgsMeshLayer(output_path, name, 'mdal')
                QgsProject.instance().addMapLayer(layer)
            self._set_lockout(False)
            if error is not None:
                self._push_status((0.0, 'Error', False))
                self.print_error(error)

        self._set_lockout(True)
        self.run_worker(target_layer, sources, output_path, output_bm2,
                        output_bm3, after=after, cancel_btn=self.cancelBtn)

    @staticmethod
    def worker(feedback: Feedback, target_layer: QgsMeshLayer,
               sources: List[_ElevLayer], output_path: str,
               output_bm2: bool, output_bm3: bool) -> None:
        """Perform the operation triggered by the dialog.

        This method is static as it will be carried out by a separate
        thread.

        Parameters
        ----------
        feedback : Feedback
            The feedback object use to communicate with the parent
            thread; this will be auto-filled internally
        target_layer : QgsMeshLayer
            The mesh layer to interpolate
        sources : List[ElevationSource]
            The elevation sources to use for interpolation
        output_path : str
            The output path of the interpolated mesh
        output_bm2 : bool
            Whether to interpolate nodes (BASEMENT v2.8)
        output_bm3 : bool
            Whether to interpolate elements (BASEMENT v3.x)

        Raises
        ------
        ValueError
            Raised if neither output format is True
        """
        if not any((output_bm2, output_bm3)):
            raise ValueError('At least one output format required')

        # Load input mesh file
        with feedback.busy('Loading quality mesh...'):
            interpol_mesh = Mesh.open(target_layer.source())

        # Interpolate nodes
        if output_bm2:
            if output_bm3:
                feedback.set_scaling(0.5)
            feedback.update(0.0, 'Interpolating mesh nodes...')
            interpolate_mesh(
                interpol_mesh, *sources, feedback=feedback)  # type: ignore

        # Interpolate elements
        if output_bm3:
            if output_bm2:
                feedback.set_scaling(0.5, 0.5)
            feedback.update(0.0, 'Interpolating mesh elements...')
            # Calculate element elevations
            elevations = calculate_element_elevation(
                interpol_mesh, *sources, feedback=feedback)  # type: ignore
            # Update element materials
            for element in interpol_mesh.elements:
                element.materials = *element.materials, elevations[element.id_]

        # Save output mesh file
        with feedback.busy('Saving computational mesh...'):
            interpol_mesh.save(output_path, 2 if output_bm3 else 1)

        feedback.clear_scaling()
        feedback.update(1.0, 'Done')

    def _get_list_selection(self) -> _ElevLayer:
        """Return the selected layers from the "Advanced" tab lists."""
        return_list = []
        for index in range(self.selectedList.count()):
            item = self.selectedList.item(index)
            layer_index: int = item.data(Qt.UserRole)
            return_list.append(self._layers_cache[layer_index])
        return return_list

    def _set_available_layers(self) -> None:
        """Add all elevation sources to the available layers list."""
        # Clear the lists
        avail_list = self.availableList
        avail_list.clear()
        self.selectedList.clear()
        self._layers_cache = []
        # Add all mesh layers, as well as any raster bands
        for layer in self.iface.mapCanvas().layers():
            if layer.type() == QgsMapLayerType.MeshLayer:
                if not layer.source().endswith('.2dm'):
                    # NOTE: Only 2DM meshes supported for now
                    continue
                new_item = QListWidgetItem(layer.name())
                new_item.setData(Qt.UserRole, len(self._layers_cache))
                self._layers_cache.append(layer)
                avail_list.addItem(new_item)
            elif layer.type() == QgsMapLayerType.RasterLayer:
                for index in range(layer.bandCount()):
                    band_name = layer.bandName(index)
                    new_item = QListWidgetItem(f'{layer.name()} • {band_name}')
                    new_item.setData(Qt.UserRole, len(self._layers_cache))
                    self._layers_cache.append((layer, index))
                    avail_list.addItem(new_item)

    def _set_lockout(self, is_locked: bool) -> None:
        """Lock out the GUI while running the tool.

        Parameters
        ----------
        is_locked : bool
            Whether to lock or unlock the GUI
        """
        self.inputGroup.setEnabled(not is_locked)
        self.tabWidget.setEnabled(not is_locked)
        self.outputGroup.setEnabled(not is_locked)
        self.closeBtn.setEnabled(not is_locked)
        self.runBtn.setEnabled(not is_locked)
        self.cancelBtn.setEnabled(is_locked)

    def _tab_switched(self, tab_index: int) -> None:
        """Switch between simple and advanced tabs.

        Parameters
        ----------
        tab_index : int
            The index of the tab that was switched to
        """
        # Basic tab
        if tab_index == 0 and self._use_advanced:
            self._use_advanced = False
        # Advanced tab
        elif tab_index == 1 and not self._use_advanced:
            self._use_advanced = True

    def _update_raster_bands(self) -> None:
        """Refresh the raster layer band combo box.

        This removes all items from the basic tab's raster band combo
        box and populates it with the bands found for the currently
        selected raster layer.
        """
        raster_layer = self.rasterSource.currentData()
        band_box = self.rasterBand
        band_box.clear()
        if raster_layer is None:
            return
        for index in range(raster_layer.bandCount()):
            band_name = raster_layer.bandName(index)
            band_box.addItem(band_name)
            band_box.setItemData(band_box.count()-1, index)
