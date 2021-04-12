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
__date__ = "06/11/2019"


from Orange.widgets.widget import OWWidget
from Orange.widgets.widget import Input, Output
from est.core.types import XASObject
from silx.gui import qt
import logging

_logger = logging.getLogger(__file__)


class SavingPointOW(OWWidget):
    """Widget to save the treatment done up to a specific point in the
    treatment flow.
    """

    name = "saving point"
    id = "orange.widgets.xas.utils.saving_point"
    description = (
        "Save treatment to a specific point and allow user to take"
        " back treatment from this point"
    )
    icon = "icons/saving.png"
    priority = 8
    category = "esrfWidgets"
    keywords = ["spectroscopy", "saving point", "save", "reprocess", "restart"]

    want_main_area = True
    resizing_enabled = False
    allows_cycle = False

    class Inputs:
        xas_obj = Input("xas_obj", XASObject, default=True)

    class Outputs:
        xas_obj = Output("xas_obj", XASObject)

    def __init__(self):
        super().__init__()

        self._last_xas_object = None

        self._buttons = qt.QDialogButtonBox(parent=self)
        self._loadSavingPt = qt.QPushButton("activate saving point", parent=self)
        self._loadSavingPt.setToolTip(
            "Load last data received and past it to " "next processing(s)"
        )
        self._buttons.addButton(self._loadSavingPt, qt.QDialogButtonBox.ActionRole)
        self.layout().addWidget(self._buttons)
        self._loadSavingPt.released.connect(self.reloadLastXasObj)

    @Inputs.xas_obj
    def _accept(self, xas_obj):
        self._last_xas_object = xas_obj.copy(create_h5_file=True)
        self.accept()
        self.Outputs.xas_obj.send(xas_obj)

    def reloadLastXasObj(self):
        """
        Load last saved xas_object and pass it to the next processing points
        """
        if self._last_xas_object is not None:
            self.accept()
            self.Outputs.xas_obj.send(self._last_xas_object.copy(create_h5_file=True))
