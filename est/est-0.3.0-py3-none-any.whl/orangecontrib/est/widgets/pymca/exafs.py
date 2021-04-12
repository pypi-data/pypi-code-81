# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "06/07/2019"


import functools
import logging

from Orange.widgets import gui
from Orange.widgets.settings import Setting
from Orange.widgets.widget import OWWidget
from Orange.widgets.widget import Input, Output
import Orange.data
from est.core.types import XASObject
from PyMca5.PyMcaGui.physics.xas.XASPostEdgeParameters import XASPostEdgeParameters
from silx.gui import qt
from silx.gui.plot import LegendSelector

import est.core.process.pymca.exafs
from orangecontrib.est.process import _ProcessForOrangeMixIn, ProcessRunnable
from est.gui.XasObjectViewer import XasObjectViewer, ViewType
from est.gui.XasObjectViewer import (
    _exafs_signal_plot,
    _exafs_postedge_plot,
    _exafs_knots_plot,
)
from orangecontrib.est.progress import QProgress
from orangecontrib.est.utils import Converter
from ..container import _ParameterWindowContainer


_logger = logging.getLogger(__file__)


class ExafsWindow(qt.QMainWindow):
    def __init__(self, parent=None):
        qt.QMainWindow.__init__(self, parent)
        mapKeys = ["mu", "EXAFS.EXAFSKValues", "EXAFS.EXAFSSignal", "EXAFS.PostEdgeB"]
        self.xasObjViewer = XasObjectViewer(mapKeys=mapKeys)
        self.xasObjViewer._spectrumViews[0]._plotWidget.getXAxis().setLabel("K")
        self.xasObjViewer._spectrumViews[0]._plotWidget.getYAxis().setLabel(
            "Normalized Units"
        )
        self.setCentralWidget(self.xasObjViewer)

        # pymca window
        self._pymcaWindow = _ParameterWindowContainer(
            parent=self, parametersWindow=XASPostEdgeParameters
        )
        dockWidget = qt.QDockWidget(parent=self)
        dockWidget.setWidget(self._pymcaWindow)
        self.addDockWidget(qt.Qt.RightDockWidgetArea, dockWidget)
        dockWidget.setAllowedAreas(qt.Qt.RightDockWidgetArea | qt.Qt.LeftDockWidgetArea)
        dockWidget.setFeatures(qt.QDockWidget.NoDockWidgetFeatures)
        self.setWindowFlags(qt.Qt.Widget)

        # legend selector
        self.legendDockWidget = LegendSelector.LegendsDockWidget(
            parent=self, plot=self.xasObjViewer._spectrumViews[0]._plotWidget
        )
        self.legendDockWidget.setAllowedAreas(
            qt.Qt.RightDockWidgetArea | qt.Qt.LeftDockWidgetArea
        )
        self.legendDockWidget.setFeatures(qt.QDockWidget.NoDockWidgetFeatures)
        self.addDockWidget(qt.Qt.RightDockWidgetArea, self.legendDockWidget)

        # volume key selection
        self.addDockWidget(
            qt.Qt.RightDockWidgetArea, self.xasObjViewer._mapView.keySelectionDocker
        )

        # plot settings
        for ope in (_exafs_signal_plot, _exafs_postedge_plot, _exafs_knots_plot):
            self.xasObjViewer._spectrumViews[0].addCurveOperation(ope)

        self.setWindowFlags(qt.Qt.Widget)

        # connect signal / slot
        self.xasObjViewer.viewTypeChanged.connect(self._updateLegendView)

        # set up
        self._updateLegendView()

    def getNCurves(self):
        return len(self.xasObjViewer.getAllCurves())

    def _updateLegendView(self):
        index, viewType = self.xasObjViewer.getViewType()
        self.legendDockWidget.setVisible(viewType is ViewType.spectrum)
        self.xasObjViewer._mapView.keySelectionDocker.setVisible(
            viewType is ViewType.map
        )


class ExafsOW(_ProcessForOrangeMixIn, OWWidget):
    """
    Widget used for signal extraction
    """

    name = "exafs"
    id = "orange.widgets.est.pymca.exafs"
    description = "Progress signal extraction"
    icon = "icons/exafs.png"
    priority = 3
    category = "esrfWidgets"
    keywords = ["spectroscopy", "signal"]

    want_main_area = True
    resizing_enabled = True
    allows_cycle = False

    process_function = est.core.process.pymca.exafs.PyMca_exafs

    _larchSettings = Setting(dict())
    """Store the configuration of the PyMca XASClass"""

    class Inputs:
        xas_obj = Input("xas_obj", XASObject, default=True)
        # simple compatibility for some Orange widget and especialy the
        # 'spectroscopy add-on'
        data_table = Input("Data", Orange.data.Table)

    class Outputs:
        res_xas_obj = Output("xas_obj", XASObject)
        # by default we want to avoid sending 'Orange.data.Table' to avoid
        # loosing the XASObject flow process and results.

    def __init__(self):
        super().__init__()
        self._latest_xas_obj = None
        self._window = ExafsWindow()
        layout = gui.vBox(self.mainArea, "exafs").layout()
        layout.addWidget(self._window)

        self._window.xasObjViewer._spectrumViews[0]._plotWidget.getXAxis().setLabel("K")
        self._window.xasObjViewer._spectrumViews[0]._plotWidget.getYAxis().setLabel(
            "Normalized Units"
        )

        # manage settings
        if self._larchSettings != dict():
            self._window._pymcaWindow.setParameters(self._larchSettings)

        # signal / slot connection
        self._window._pymcaWindow.sigChanged.connect(self._updateProcess)

    def _updateProcess(self):
        self._update_settings()
        if self._latest_xas_obj:
            self.process(self._latest_xas_obj)

    def _update_settings(self):
        self._larchSettings = self._window._pymcaWindow.getParameters()

    @Inputs.data_table
    def processFrmDataTable(self, data_table):
        if data_table is None:
            return
        self.process(Converter.toXASObject(data_table=data_table))

    @Inputs.xas_obj
    def process(self, xas_obj):
        if xas_obj is None:
            return

        if not self._canProcess():
            _logger.warning(
                "There is some processing on going already, will"
                "not process the new dataset"
            )

        self._latest_xas_obj = xas_obj
        self._startProcess()

        # setup the exafs process
        process_obj = QPyMca_exafs()
        process_obj._advancement.sigProgress.connect(self._setProgressValue)
        process_obj.set_properties(
            {"_pymcaSettings": self._window._pymcaWindow.getParameters()}
        )

        # update the processing thread
        thread = self.getProcessingThread()
        thread.init(process_obj=process_obj, xas_obj=self._latest_xas_obj)
        self._callback_finish = functools.partial(
            self._endProcess, self._latest_xas_obj
        )
        thread.finished.connect(self._callback_finish)
        # start processing
        thread.start(priority=qt.QThread.LowPriority)

    def _setProgressValue(self, value):
        self._progress.widget.progressBarSet(value)


class QPyMca_exafs(est.core.process.pymca.exafs.PyMca_exafs):
    """
    Normalization able to give advancement using qt.Signal and QThreadPool
    """

    def __init__(self):
        est.core.process.pymca.exafs.PyMca_exafs.__init__(self)
        self._advancement = QProgress("normalization")

    def _pool_process(self, xas_obj):
        self.pool = qt.QThreadPool()
        self.pool.setMaxThreadCount(5)
        for spectrum in xas_obj.spectra:
            runnable = ProcessRunnable(
                fct=est.core.process.pymca.exafs.process_spectr_exafs,
                spectrum=spectrum,
                configuration=xas_obj.configuration,
                callback=self._advancement.increaseAdvancement,
            )
            self.pool.start(runnable)
        self.pool.waitForDone()
