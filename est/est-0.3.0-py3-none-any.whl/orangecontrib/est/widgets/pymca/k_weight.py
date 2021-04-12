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
from silx.gui import qt

import est.core.process.pymca.k_weight
from orangecontrib.est.process import _ProcessForOrangeMixIn, ProcessRunnable
from est.core.types import XASObject
from orangecontrib.est.progress import QProgress
from orangecontrib.est.utils import Converter

_logger = logging.getLogger(__file__)


class KWeightWindow(qt.QMainWindow):
    def __init__(self, parent=None):
        qt.QMainWindow.__init__(self, parent)

        # k wright widget
        self._k_widget = qt.QWidget(parent=self)
        self._k_widget.setLayout(qt.QHBoxLayout())
        self._k_widget.layout().addWidget(qt.QLabel("k weight"))
        self._k_spin_box = qt.QSpinBox(parent=self)
        self._k_spin_box.setRange(0, 3)
        self._k_widget.layout().addWidget(self._k_spin_box)
        dockWidget = qt.QDockWidget(parent=self)
        dockWidget.setWidget(self._k_widget)
        self.addDockWidget(qt.Qt.RightDockWidgetArea, dockWidget)
        dockWidget.setAllowedAreas(qt.Qt.RightDockWidgetArea | qt.Qt.LeftDockWidgetArea)
        dockWidget.setFeatures(qt.QDockWidget.NoDockWidgetFeatures)

        self.setWindowFlags(qt.Qt.Widget)


class KWeightOW(_ProcessForOrangeMixIn, OWWidget):
    """
    Widget used for signal extraction
    """

    name = "k weight"
    id = "orange.widgets.est.pymca.k_weight"
    description = "Progress k weight"
    icon = "icons/k_weight.png"
    priority = 2
    category = "esrfWidgets"
    keywords = ["spectroscopy", "signal", "k", "weight"]

    want_main_area = True
    resizing_enabled = True
    allows_cycle = False

    process_function = est.core.process.pymca.k_weight.PyMca_k_weight

    _kWeightSetting = Setting(int(3))
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
        layout = gui.vBox(self.mainArea, "k weight").layout()
        self._window = KWeightWindow(parent=self)
        layout.addWidget(self._window)

        # progress
        self._progress = gui.ProgressBar(self, 100)

        # manage settings
        if self._kWeightSetting != 3:
            self._window._k_spin_box.setValue(self._kWeightSetting)

        # signal / slot connection
        self._window._k_spin_box.valueChanged.connect(self._updateProcess)

    def _updateProcess(self, *arv, **kwargs):
        self._update_settings()
        if self._latest_xas_obj:
            self.process(self._latest_xas_obj)

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

        # setup the k weight process
        process_obj = QPyMca_k_weight()
        process_obj._advancement.sigProgress.connect(self._setProgressValue)
        process_obj.set_properties(
            {"_kWeightSetting": self._window._k_spin_box.value()}
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

    def _update_settings(self):
        self._kWeightSetting = self._window._k_spin_box.value()

    def _setProgressValue(self, value):
        self._progress.widget.progressBarSet(value)


class QPyMca_k_weight(est.core.process.pymca.k_weight.PyMca_k_weight):
    """
    Normalization able to give advancement using qt.Signal and QThreadPool
    """

    def __init__(self):
        est.core.process.pymca.k_weight.PyMca_k_weight.__init__(self)
        self._advancement = QProgress("normalization")

    def _pool_process(self, xas_obj):
        self.pool = qt.QThreadPool()
        self.pool.setMaxThreadCount(5)
        for spectrum in xas_obj.spectra:
            assert "KWeight" in xas_obj.configuration
            runnable = ProcessRunnable(
                fct=est.core.process.pymca.k_weight.process_spectr_k,
                spectrum=spectrum,
                configuration=xas_obj.configuration,
                callback=self._advancement.increaseAdvancement,
            )
            self.pool.start(runnable)
        self.pool.waitForDone()
