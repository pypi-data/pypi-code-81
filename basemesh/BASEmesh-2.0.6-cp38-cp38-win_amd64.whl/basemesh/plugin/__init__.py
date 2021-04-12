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

"""QGIS plugin component of BASEmesh."""

from typing import Optional
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMenu, QToolBar
from qgis.core import QgsApplication  # type: ignore
from qgis.gui import QgisInterface  # type: ignore
from . import resources
from .gui import AboutDialog, ElevMeshDialog, InterpolDialog, QualMeshDialog
from .processing import BasemeshProcessingProvider


class BaseMeshPlugin:
    """The BASEmesh plugin to be loaded into the QGIS application."""

    display_name = 'BASEmesh 2'

    def __init__(self, iface: QgisInterface) -> None:
        """Prepare the plugin for initialisation.

        Note that this is called in preparation for the plugin being
        loaded. The class may be initialised, but the QGIS plugin side
        still requires the initGui() method to be called.

        Parameters
        ----------
        iface : QgisInterface
            The interface to generate the plugin's menu for
        """
        self.iface = iface
        self.menu: Optional[QMenu] = None
        self.toolbar: Optional[QToolBar] = None
        self.provider = BasemeshProcessingProvider()
        # Create actions
        self.about = QAction(
            QIcon(':/plugins/basemesh/plugin/icons/basemesh_icon.svg'),
            'About BASEmesh')
        self.about.setStatusTip(
            'Additional information about BASEmesh, BASEMENT, and Triangle')
        self.about.triggered.connect(self._open_about)
        self.elevmesh = QAction(
            QIcon(':/plugins/basemesh/plugin/icons/elev_meshing.svg'),
            'Elevation meshing')
        self.elevmesh.setStatusTip('Meshing of elevation data')
        self.elevmesh.triggered.connect(self._open_elevmesh)
        self.qualmesh = QAction(
            QIcon(':/plugins/basemesh/plugin/icons/qual_meshing.svg'),
            'Quality meshing')
        self.qualmesh.setStatusTip('Meshing with quality constraints')
        self.qualmesh.triggered.connect(self._open_qualmesh)
        self.interpol = QAction(
            QIcon(':/plugins/basemesh/plugin/icons/interpolation.svg'),
            'Interpolation')
        self.interpol.setStatusTip('Mesh interpolation')
        self.interpol.triggered.connect(self._open_interpol)

    def initGui(self) -> None:
        """GUI initialization procedure.

        This method is called by QGIS to integrate the plugin with the
        QGIS user interface. This includes menu bar items and buttons.
        """
        assert self.toolbar is not None
        toolbar: QToolBar = self.toolbar
        # Create toolbar
        toolbar = self.iface.addToolBar(self.display_name)
        toolbar.setObjectName('basemeshToolBar')
        toolbar.addAction(self.elevmesh)
        toolbar.addAction(self.qualmesh)
        toolbar.addAction(self.interpol)

        # Add plugin menu entry
        assert self.menu is not None
        menu: QMenu = self.menu
        menu = self.iface.pluginMenu().addMenu(
            QIcon(':/plugins/basemesh/plugin/icons/basemesh_icon.svg'),
            self.display_name)
        menu.addAction(self.elevmesh)
        menu.addAction(self.qualmesh)
        menu.addAction(self.interpol)
        menu.addAction(self.about)

        # Hook up processing algorithm provider
        QgsApplication.processingRegistry().addProvider(self.provider)

    def _open_about(self) -> None:
        AboutDialog(self.iface).exec_()

    def _open_elevmesh(self) -> None:
        ElevMeshDialog(self.iface).exec_()

    def _open_interpol(self) -> None:
        InterpolDialog(self.iface).exec_()

    def _open_qualmesh(self) -> None:
        QualMeshDialog(self.iface).exec_()

    def unload(self) -> None:
        """GUI breakdown procedure.

        This method is called when the plugin is unloaded. After this
        function completes, the interface is expected to be as if the
        plugin were never initialized in the first place.
        """
        # Destroy plugin menu entry
        if self.menu is not None:
            self.menu.removeAction(self.elevmesh)
            self.menu.removeAction(self.interpol)
            self.menu.removeAction(self.qualmesh)
            self.menu.removeAction(self.about)
            self.iface.pluginMenu().removeAction(self.menu.menuAction())
        # Remove tool bar
        del self.toolbar

        # Remove processing algorithm provider
        QgsApplication.processingRegistry().removeProvider(self.provider)


def classFactory(iface: QgisInterface) -> 'BaseMeshPlugin':
    """Instantiate and return the BASEmesh plugin object.

    This function is called by QGIS  when loading the plugin and serves
    as the primary endpoint to the QGIS application.

    Parameters
    ----------
    iface : QgisInterface
        The QGIS interface to generate the plugin menu

    Returns
    -------
    BaseMeshPlugin
        The instantiated BASEmesh plugin to be used by QGIS
    """
    return BaseMeshPlugin(iface)
