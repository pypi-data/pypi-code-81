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
__date__ = "18/01/2021"

import logging

from Orange.widgets import gui
from Orange.widgets.settings import Setting
from Orange.widgets.widget import OWWidget
from Orange.widgets.widget import Input, Output
from orangecontrib.est.progress import QProgress
from orangecontrib.est.process import ProcessRunnable
import Orange.data
import functools
from orangecontrib.est.utils import Converter
from orangecontrib.est.process import _ProcessForOrangeMixIn
from silx.gui import qt
import est.core.process.noise
from est.core.types import XASObject
from est.gui.noise import SavitskyGolayNoise

_logger = logging.getLogger(__file__)


class NoiseOW(_ProcessForOrangeMixIn, OWWidget):
    """
    Widget used to make the selection of a region of Interest to treat in a
    Dataset.
    """

    name = "noise"
    id = "orange.widgets.xas.utils.noise"
    description = "Compute noise using Savitsky-Golay"
    icon = "icons/noise.svg"

    priority = 40
    category = "esrfWidgets"
    keywords = ["dataset", "data", "noise"]

    process_function = est.core.process.noise.NoiseProcess

    want_main_area = True
    resizing_enabled = True
    compress_signal = False
    allows_cycle = False

    window_size = Setting(int(-1))
    polynomial_order = Setting(int(-1))
    e_min = Setting(int(-1))
    e_max = Setting(int(-1))

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

        self._window = SavitskyGolayNoise(parent=self)
        layout = gui.vBox(self.mainArea, "noise").layout()
        layout.addWidget(self._window)

        # buttons
        types = qt.QDialogButtonBox.Ok
        self._buttons = qt.QDialogButtonBox(parent=self)
        self._buttons.setStandardButtons(types)
        layout.addWidget(self._buttons)

        self._buttons.hide()

        # expose API
        self.setWindowSize = self._window.setWindowSize
        self.getWindowSize = self._window.getWindowSize
        self.setPolynomialOrder = self._window.setPolynomialOrder
        self.getPolynomialOrder = self._window.getPolynomialOrder

        # manage settings
        self._window.setParameters(
            {
                "window_size": self.window_size,
                "polynomial_order": self.polynomial_order,
                "e_min": self.e_min,
                "e_max": self.e_max,
            }
        )

        # signal / slot connection
        # connect signals / slots
        self._window.sigChanged.connect(self._updateProcess)

    def _updateProcess(self, *arv, **kwargs):
        self._update_settings()
        if self._latest_xas_obj:
            self.process(xas_obj=self._latest_xas_obj)

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

        # setup the ft process
        process_obj = QNoise()
        process_obj._advancement.sigProgress.connect(self._setProgressValue)
        process_obj.set_properties({"noise": self._window.getParameters()})

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
        self.window_size = self._window.getWindowSize()
        self.polynomial_order = self._window.getPolynomialOrder()
        self.e_min = self._window.getEMin()
        self.e_max = self._window.getEMax()

    def _setProgressValue(self, value):
        self._progress.widget.progressBarSet(value)


class QNoise(est.core.process.noise.NoiseProcess):
    """
    Normalization able to give advancement using qt.Signal and QThreadPool
    """

    def __init__(self):
        est.core.process.noise.NoiseProcess.__init__(self)
        self._advancement = QProgress("noise")

    def _pool_process(self, xas_obj):
        self.pool = qt.QThreadPool()
        self.pool.setMaxThreadCount(5)
        for spectrum in xas_obj.spectra:
            runnable = ProcessRunnable(
                fct=est.core.process.noise.process_noise_savgol,
                spectrum=spectrum,
                configuration=xas_obj.configuration,
                callback=self._advancement.increaseAdvancement,
            )
            self.pool.start(runnable)
        self.pool.waitForDone()
