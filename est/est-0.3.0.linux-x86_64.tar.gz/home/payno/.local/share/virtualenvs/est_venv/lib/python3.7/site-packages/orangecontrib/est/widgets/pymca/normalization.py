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
from PyMca5.PyMcaGui.physics.xas.XASNormalizationParameters import (
    XASNormalizationParameters,
)
from silx.gui import qt
from silx.gui.plot import LegendSelector
from est.gui.XasObjectViewer import (
    _plot_edge,
    _plot_norm,
    _plot_post_edge,
    _plot_pre_edge,
)
from orangecontrib.est.process import _ProcessForOrangeMixIn
from orangecontrib.est.process import ProcessRunnable
from orangecontrib.est.widgets.container import _ParameterWindowContainer
from orangecontrib.est.progress import QProgress
from orangecontrib.est.utils import Converter
from est.gui.e0calculator import E0CalculatorDialog
from est.core.types import XASObject
from est.gui.XasObjectViewer import XasObjectViewer, ViewType
import est.core.process.pymca.normalization

_logger = logging.getLogger(__file__)


class _XASNormalizationParametersPatched(XASNormalizationParameters):
    """This class will try to patch the XASNormalizationParameters with the
    E0Calculation widget"""

    sigE0CalculationRequested = qt.Signal()
    """Signal emitted when E0 computation is required"""

    def __init__(self, *args, **kwargs):
        XASNormalizationParameters.__init__(self, *args, **kwargs)
        # add E0CalculationWidget if can
        try:
            self.__addE0CalculationDialog()
        except Exception as e:
            _logger.warning("Fail to add the E0CalculationDialog. Reason is", str(e))
        else:
            self._e0CalcPB.pressed.connect(self._launchE0Calculator)

    def setE0(self, e0):
        e0_min = self.e0SpinBox.minimum()
        e0_max = self.e0SpinBox.maximum()
        if not (e0_min <= e0 <= e0_max):
            _logger.warning(
                "given e0 value (%s) is invalid, value should be "
                "between %s and %s" % (e0, e0_min, e0_max)
            )

        params = self.getParameters()
        params["E0Value"] = e0
        params["E0Method"] = "Manual"
        self.setParameters(ddict=params, signal=False)

    def __addE0CalculationDialog(self):
        # check we know where to set the button
        for attr in ("e0SpinBox", "jumpLine", "e0CheckBox"):
            if not hasattr(self, attr):
                raise NameError(
                    "%s not defined - pymca version not " "recognized" % attr
                )
        for widget, widget_index in zip((self.e0SpinBox, self.jumpLine), (3, 5)):
            if self.layout().indexOf(widget) != widget_index:
                raise ValueError("XASNormalizationParameters layout is not recognized.")

        style = qt.QApplication.instance().style()
        icon = style.standardIcon(qt.QStyle.SP_FileDialogContentsView)
        self._e0CalcPB = qt.QPushButton(icon, "", self)
        self.layout().addWidget(self._e0CalcPB, 1, 2)

    def _launchE0Calculator(self, *args, **kwargs):
        self.sigE0CalculationRequested.emit()


class NormalizationWindow(qt.QMainWindow):
    """Widget embedding the pymca parameter window and the display of the
    data currently process"""

    sigE0CalculationRequested = qt.Signal()
    """Signal emitted when E0 computation is required"""

    def __init__(self, parent=None):
        qt.QMainWindow.__init__(self, parent)

        # xas object viewer
        mapKeys = ["mu", "NormalizedMu", "NormalizedSignal", "NormalizedBackground"]
        self.xasObjViewer = XasObjectViewer(mapKeys=mapKeys)
        self.xasObjViewer._spectrumViews[0]._plotWidget.getXAxis().setLabel(
            "Energy (eV)"
        )
        self.xasObjViewer._spectrumViews[0]._plotWidget.getYAxis().setLabel(
            "Absorption (a.u.)"
        )
        self.setCentralWidget(self.xasObjViewer)
        self._pymcaWindow = _ParameterWindowContainer(
            parent=self, parametersWindow=_XASNormalizationParametersPatched
        )
        dockWidget = qt.QDockWidget(parent=self)

        # pymca window
        dockWidget.setWidget(self._pymcaWindow)
        self.addDockWidget(qt.Qt.RightDockWidgetArea, dockWidget)
        dockWidget.setAllowedAreas(qt.Qt.RightDockWidgetArea | qt.Qt.LeftDockWidgetArea)
        dockWidget.setFeatures(qt.QDockWidget.NoDockWidgetFeatures)

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
        for ope in (_plot_edge, _plot_norm, _plot_post_edge, _plot_pre_edge):
            self.xasObjViewer._spectrumViews[0].addCurveOperation(ope)

        self.setWindowFlags(qt.Qt.Widget)

        # expose API
        self.setE0 = self._pymcaWindow._mainwidget.setE0

        # connect signal / slot
        self.xasObjViewer.viewTypeChanged.connect(self._updateLegendView)

        # set up
        self._updateLegendView()

    def getNCurves(self):
        return len(self.xasObjViewer._spectrumViews._plot.getAllCurves())

    def _updateLegendView(self):
        index, viewType = self.xasObjViewer.getViewType()
        self.legendDockWidget.setVisible(viewType is ViewType.spectrum)
        self.xasObjViewer._mapView.keySelectionDocker.setVisible(
            viewType is ViewType.map
        )


class NormalizationOW(_ProcessForOrangeMixIn, OWWidget):
    """
    Widget used for signal extraction
    """

    name = "normalization"
    id = "orange.widgets.est.pymca.normalization"
    description = "Progress spectra normalization"
    icon = "icons/normalization.png"
    priority = 1
    category = "esrfWidgets"
    keywords = ["spectroscopy", "normalization"]

    want_main_area = True
    resizing_enabled = True
    allows_cycle = False

    process_function = est.core.process.pymca.normalization.PyMca_normalization

    _pymcaSettings = Setting(dict())
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
        self._window = NormalizationWindow(parent=self)
        layout = gui.vBox(self.mainArea, "normalization").layout()
        layout.addWidget(self._window)
        self._window.xasObjViewer.setWindowTitle("spectra")

        # expose API
        self.setE0 = self._window.setE0

        # manage settings
        if self._pymcaSettings != dict():
            self._window._pymcaWindow.setParameters(self._pymcaSettings)

        # connect signals / slots
        pymcaWindowContainer = self._window._pymcaWindow
        _sig = pymcaWindowContainer.sigChanged.connect(self._updateProcess)
        if hasattr(pymcaWindowContainer._mainwidget, "sigE0CalculationRequested"):
            pymcaWindowContainer._mainwidget.sigE0CalculationRequested.connect(
                self._getE0FrmDialog
            )

    def _updateProcess(self):
        self._update_settings()
        if self._latest_xas_obj:
            self.process(self._latest_xas_obj)

    def _update_settings(self):
        self._pymcaSettings = self._window._pymcaWindow.getParameters()

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
        # update E0 if necessary
        if "e0" in xas_obj.configuration:
            self.setE0(xas_obj.configuration["e0"])
        self._startProcess()

        # setup the normalization process
        process_obj = QPyMca_normalization()
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

    def _getE0FrmDialog(self):
        """Pop up an instance of E0CalculationDialog and get E0 from it"""
        if self._latest_xas_obj is None:
            return
        dialog = E0CalculatorDialog(xas_obj=self._latest_xas_obj, parent=None)
        if dialog.exec_():
            self.setE0(dialog.getE0())


class QPyMca_normalization(est.core.process.pymca.normalization.PyMca_normalization):
    """
    Normalization able to give advancement using qt.Signal and QThreadPool
    """

    def __init__(self):
        est.core.process.pymca.normalization.PyMca_normalization.__init__(self)
        self._advancement = QProgress("normalization")

    def _pool_process(self, xas_obj):
        self.pool = qt.QThreadPool()
        self.pool.setMaxThreadCount(5)
        for spectrum in xas_obj.spectra:
            runnable = ProcessRunnable(
                fct=est.core.process.pymca.normalization.process_spectr_norm,
                spectrum=spectrum,
                configuration=xas_obj.configuration,
                callback=self._advancement.increaseAdvancement,
            )
            self.pool.start(runnable)
        self.pool.waitForDone()


if __name__ == "__main__":
    from est.core.utils import spectra as spectra_utils
    from est.core.types import XASObject

    def create_dataset():
        dim1, dim2 = 20, 40

        energy, spectra = spectra_utils.create_dataset(
            shape=(256, dim1, dim2), noise=True
        )
        spectra = spectra * 1000
        return XASObject(energy=energy, spectra=spectra, dim1=dim1, dim2=dim2)

    xas_object = create_dataset()
    app = qt.QApplication([])
    widget = NormalizationOW()
    widget.process(xas_object)
    widget.show()
    app.exec_()
