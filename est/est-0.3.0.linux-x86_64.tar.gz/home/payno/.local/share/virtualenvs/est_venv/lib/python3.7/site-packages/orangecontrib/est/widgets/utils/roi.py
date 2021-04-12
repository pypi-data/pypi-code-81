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
from Orange.widgets.settings import Setting
from Orange.widgets.widget import OWWidget
from Orange.widgets.widget import Input, Output
import Orange.data
from orangecontrib.est.utils import Converter
from silx.gui import qt

import est.core.process.roi
from est.core.types import XASObject
from est.gui.roiselector import ROISelector

_logger = logging.getLogger(__file__)


class RoiSelectionOW(OWWidget):
    """
    Widget used to make the selection of a region of Interest to treat in a
    Dataset.
    """

    name = "ROI definition"
    id = "orange.widgets.xas.utils.roiselection"
    description = "Select data Region Of Interest"
    icon = "icons/image-select-box.svg"

    priority = 10
    category = "esrfWidgets"
    keywords = ["dataset", "data", "selection", "ROI", "Region of Interest"]

    process_function = est.core.process.roi.ROIProcess

    want_main_area = True
    resizing_enabled = True
    compress_signal = False
    allows_cycle = False

    _roi_origin = Setting(tuple())
    _roi_size = Setting(tuple())

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

        self._widget = ROISelector(parent=self)
        layout = gui.vBox(self.mainArea, "data selection").layout()
        layout.addWidget(self._widget)

        # buttons
        types = qt.QDialogButtonBox.Ok
        self._buttons = qt.QDialogButtonBox(parent=self)
        self._buttons.setStandardButtons(types)
        layout.addWidget(self._buttons)

        self._buttons.hide()

        # connect signal / slot
        self._buttons.accepted.connect(self.validate)

        # expose API
        self.setROI = self._widget.setROI
        self.getROI = self._widget.getROI

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
            roi_process = est.core.process.roi.ROIProcess()
            xas_roi = est.core.process.roi._ROI.from_silx_def(self.getROI()).to_dict()
            roi_prop = {"roi": xas_roi}
            roi_process.set_properties(roi_prop)
            # we want to keep the raw data in roi object, to be able to resize
            # the roi (especially increase it size)
            xas_obj = roi_process.process(xas_obj=self._widget.getXasObject())
            self.Outputs.res_xas_obj.send(xas_obj)
        except Exception as e:
            _logger.error(e)
        else:
            OWWidget.accept(self)

    def updateProperties(self):
        # as dim are named tuple we have to cast them to dict
        self._roi_origin = tuple(self._widget.getROI().getOrigin())
        self._roi_size = tuple(self._widget.getROI().getSize())
