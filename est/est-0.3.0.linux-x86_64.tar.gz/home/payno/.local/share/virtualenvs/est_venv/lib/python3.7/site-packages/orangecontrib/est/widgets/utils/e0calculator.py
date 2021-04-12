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
__date__ = "02/10/2018"

import logging

from Orange.widgets import gui
from Orange.widgets.widget import OWWidget
from Orange.widgets.widget import Input, Output
import Orange.data
from orangecontrib.est.utils import Converter
from silx.gui import qt
import functools

import est.core.process.setconfig
from est.core.types import XASObject
from est.gui.e0calculator import E0Calculator, E0ComputationMethod

_logger = logging.getLogger(__file__)


class E0calculatorOW(OWWidget):
    """
    Widget used to make compute E0 from the dataset.
    """

    name = "e0 calculator"
    id = "orange.widgets.xas.utils.e0calculator"
    description = "Compute E0 from a region of the dataset"
    icon = "icons/e0.svg"

    priority = 25
    category = "esrfWidgets"
    keywords = [
        "E0",
        "Energy",
        "dataset",
        "data",
        "selection",
        "ROI",
        "Region of Interest",
    ]

    process_function = est.core.process.setconfig._xas_set_config

    want_main_area = True
    resizing_enabled = True
    compress_signal = False
    allows_cycle = False

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

        self._widget = E0Calculator(parent=self)
        layout = gui.vBox(self.mainArea, "data selection").layout()
        layout.addWidget(self._widget)

        # add the buttons
        style = qt.QApplication.instance().style()
        icon = style.standardIcon(qt.QStyle.SP_DialogApplyButton)

        self._buttons = qt.QDialogButtonBox(parent=self)
        self._useMedian = qt.QPushButton(icon, "use median", self)
        self._buttons.addButton(self._useMedian, qt.QDialogButtonBox.ActionRole)
        self._useMean = qt.QPushButton(icon, "use mean", self)
        self._buttons.addButton(self._useMean, qt.QDialogButtonBox.ActionRole)
        layout.addWidget(self._buttons)

        # connect signal / slot
        self._useMean.released.connect(
            functools.partial(self.validateMethodToUse, E0ComputationMethod.MEAN)
        )
        self._useMedian.released.connect(
            functools.partial(self.validateMethodToUse, E0ComputationMethod.MEDIAN)
        )

        # set up
        self._buttons.hide()

    def validateMethodToUse(self, method):
        """Define the method to use and close the dialog"""
        method = E0ComputationMethod.from_value(method)
        assert method in (None, E0ComputationMethod.MEDIAN, E0ComputationMethod.MEAN)
        self._methodToUse = method
        self.validate()

    def getE0(self):
        if self._methodToUse is None:
            return None
        else:
            return self._widget.getE0(method=self._methodToUse)

    @Inputs.data_table
    def processFrmDataTable(self, data_table):
        if data_table is None:
            return
        self.process(Converter.toXASObject(data_table=data_table))

    @Inputs.xas_obj
    def process(self, xas_obj):
        if xas_obj is None:
            return
        self._widget.setXasObject(xas_obj=xas_obj)
        self._buttons.show()
        self.show()

    def validate(self):
        """
        callback when the ROI has been validated
        """
        if self._widget.getXasObject() is None:
            return

        try:
            xas_obj = self._widget.getXasObject()
            prop = xas_obj.configuration
            prop["e0"] = self.getE0()
            xas_obj.configuration = prop
            _logger.info("e0 define: {}".format(str(self.getE0())))
            self.Outputs.res_xas_obj.send(xas_obj)
        except Exception as e:
            _logger.error(e)
        else:
            OWWidget.accept(self)
