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


from Orange.widgets import gui
from Orange.widgets.widget import OWWidget
from Orange.widgets.settings import Setting
from Orange.widgets.widget import Input
from silx.gui import qt
from est.core.types import XASObject
import est.core.io
import logging
import h5py

_logger = logging.getLogger(__file__)


class XASOutputOW(OWWidget):
    """
    Widget used for signal extraction
    """

    name = "xas output"
    id = "orange.widgets.xas.utils.xas_output"
    description = "Store process result (configuration)"
    icon = "icons/output.png"
    priority = 5
    category = "esrfWidgets"
    keywords = ["spectroscopy", "signal", "output", "file"]

    want_main_area = True
    resizing_enabled = True
    allows_cycle = False

    _output_file_setting = Setting(str())
    process_function = est.core.io.XASWriter

    class Inputs:
        xas_obj = Input("xas_obj", XASObject, default=True)

    def __init__(self):
        super().__init__()
        self._outputWindow = qt.QWidget(parent=self)
        self._outputWindow.setLayout(qt.QGridLayout())

        self._outputWindow.layout().addWidget(qt.QLabel("file", parent=self))
        self._inputLe = qt.QLineEdit("", parent=self)
        self._outputWindow.layout().addWidget(self._inputLe, 0, 0)
        self._selectPB = qt.QPushButton("select", parent=self)
        self._outputWindow.layout().addWidget(self._selectPB, 0, 1)

        spacer = qt.QWidget(parent=self)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self._outputWindow.layout().addWidget(spacer, 2, 0)

        layout = gui.vBox(self.mainArea, "output").layout()
        layout.addWidget(self._outputWindow)

        # deal with settings
        self.setFileSelected(self._output_file_setting)

        # signal / slot connection
        self._selectPB.pressed.connect(self._selectFile)

    def _selectFile(self, *args, **kwargs):
        old = self.blockSignals(True)
        dialog = qt.QFileDialog(self)
        # dialog.setFileMode(qt.QFileDialog.AnyFile)
        dialog.setAcceptMode(qt.QFileDialog.AcceptSave)
        dialog.setNameFilters(["hdf5 files (*.hdf5, *.hdf, *.h5)"])

        if not dialog.exec_():
            dialog.close()
            return False

        fileSelected = dialog.selectedFiles()
        if len(fileSelected) == 0:
            return False
        else:
            assert len(fileSelected) == 1
            file_ = fileSelected[0]
            if not h5py.is_hdf5(file_):
                file_ += ".h5"
            self.setFileSelected(file_)

        self.blockSignals(old)
        return True

    def setFileSelected(self, file_path):
        self._output_file_setting = file_path
        self._inputLe.setText(file_path)

    def _getFileSelected(self):
        return self._inputLe.text()

    @Inputs.xas_obj
    def process(self, xas_obj):
        if xas_obj is None:
            return
        if isinstance(xas_obj, dict):
            _xas_obj = XASObject.from_dict(xas_obj)
        else:
            _xas_obj = xas_obj

        has_file = self._getFileSelected() != ""
        if not has_file:
            mess = qt.QMessageBox(parent=self)
            mess.setIcon(qt.QMessageBox.Warning)
            mess.setText("No output file defined, please give a file path")
            mess.exec_()
            has_file = self._selectFile()
        if not has_file:
            _logger.error("no valid output file given, skip save")
        else:
            _xas_obj.dump(self._getFileSelected())
