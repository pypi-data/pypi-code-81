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


import logging
import os

from Orange.widgets import gui
from Orange.widgets.settings import Setting
from Orange.widgets.widget import OWWidget
from Orange.widgets.widget import Output
from silx.gui import qt
from silx.io.url import DataUrl

import est.core.io
from est.core.types import XASObject
from est.gui.xas_object_definition import XASObjectWindow

_logger = logging.getLogger(__file__)


_DEBUG = False


class XASInputOW(OWWidget):
    """
    Widget used for signal extraction
    """

    name = "xas input"
    id = "orange.widgets.xas.utils.xas_input"
    description = "Read .dat file and convert it to spectra"
    icon = "icons/input.png"
    priority = 0
    category = "esrfWidgets"
    keywords = ["spectroscopy", "signal", "input", "file"]

    want_main_area = True
    resizing_enabled = True
    allows_cycle = False

    _spec_file_setting = Setting(tuple())
    _spectra_url_setting = Setting(str())
    _energy_url_setting = Setting(str())
    _configuration_url_setting = Setting(str())
    _dimensions_setting = Setting(tuple())
    _energy_unit_settings = Setting(str())
    _I0_url_setting = Setting(str())
    _I1_url_setting = Setting(str())
    _I2_url_setting = Setting(str())
    _mu_ref_url_setting = Setting(str())

    process_function = est.core.io.read_frm_file

    class Outputs:
        res_xas_obj = Output("xas_obj", XASObject)
        # by default we want to avoid sending 'Orange.data.Table' to avoid
        # loosing the XASObject flow process and results.

    def __init__(self):
        super().__init__()
        self._inputWindow = qt.QWidget(parent=self)
        self._inputWindow.setLayout(qt.QGridLayout())

        self._inputDialog = XASObjectWindow(parent=self)
        self._inputWindow.layout().addWidget(self._inputDialog, 0, 0, 1, 2)

        style = qt.QApplication.instance().style()
        icon = style.standardIcon(qt.QStyle.SP_DialogApplyButton)

        # add the apply button
        types = qt.QDialogButtonBox.Ok
        self._buttons = qt.QDialogButtonBox(parent=self)
        self._buttons.setStandardButtons(types)
        self.layout().addWidget(self._buttons)

        spacer = qt.QWidget(parent=self)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self._inputWindow.layout().addWidget(spacer, 2, 0)

        layout = gui.vBox(self.mainArea, "input").layout()
        layout.addWidget(self._inputWindow)

        # deal with setting
        try:
            self._loadSettings()
        except:
            pass

        # expose api
        self.apply = self._emitNewFile

        # signal / slot connection
        self._buttons.accepted.connect(self.hide)
        self._buttons.accepted.connect(self._emitNewFile)
        self._inputDialog.getMainWindow().editingFinished.connect(self._storeSettings)
        self.setFileSelected = self._inputDialog.setDatFile

    def _emitNewFile(self, *args, **kwargs):
        try:
            xas_obj = self._inputDialog.buildXASObject()
        except ValueError as e:
            qt.QMessageBox.warning(self, "", str(e))
        else:
            if _DEBUG is True and xas_obj.n_spectrum > 100:
                from est.core.process.roi import ROIProcess, _ROI

                roiProcess = ROIProcess()
                roiProcess.setRoi(origin=(0, 0), size=(10, 10))
                xas_obj = roiProcess.process(xas_obj)
            self.Outputs.res_xas_obj.send(xas_obj)

    def _loadSettings(self):
        input_type = est.io.InputType.hdf5_spectra

        if len(self._spec_file_setting) == 0:
            input_spec_file = None
            input_energy_col_name = None
            input_abs_col_name = None
            input_monitor_col_name = None
            scan_title = None
        else:
            (
                input_spec_file,
                input_energy_col_name,
                input_abs_col_name,
                input_monitor_col_name,
                scan_title,
            ) = self._spec_file_setting
        if input_spec_file is not None:
            if input_spec_file.endswith(".xmu"):
                input_type = est.io.InputType.xmu_spectrum
                self._inputDialog.setXmuFile(input_spec_file)
            else:
                input_type = est.io.InputType.dat_spectrum
                self._inputDialog.setDatFile(input_spec_file)
                if input_energy_col_name is not None:
                    self._inputDialog.setEnergyColName(input_energy_col_name)
                if input_abs_col_name is not None:
                    self._inputDialog.setAbsColName(input_abs_col_name)
                if scan_title is not None:
                    self._inputDialog.setScanTitle(scan_title)
                if input_monitor_col_name is not None:
                    self._inputDialog.setMonitorColName(input_monitor_col_name)

        def load_url(url_path, setter):
            if url_path != "":
                if isinstance(url_path, DataUrl):
                    url = url_path
                else:
                    url = DataUrl(url_path)

                try:
                    if url and url.is_valid():
                        setter(url.path())
                except ... as e:
                    logging.info("fail to load ", url_path)

        load_url(self._spectra_url_setting, self._inputDialog.setSpectraUrl)
        load_url(self._energy_url_setting, self._inputDialog.setEnergyUrl)
        load_url(self._configuration_url_setting, self._inputDialog.setConfigurationUrl)

        advanceHDF5Info = self._inputDialog.getAdvanceHdf5Information()
        load_url(self._I0_url_setting, advanceHDF5Info.setI0Url)
        load_url(self._I1_url_setting, advanceHDF5Info.setI1Url)
        load_url(self._I2_url_setting, advanceHDF5Info.setI2Url)
        load_url(self._mu_ref_url_setting, advanceHDF5Info.setMuRefUrl)

        if len(self._dimensions_setting) == 3:
            self._inputDialog.setDimensions(self._dimensions_setting)
        else:
            assert len(self._dimensions_setting) == 0
        self._inputDialog.getMainWindow().setEnergyUnit(self._energy_unit_settings)

        # set up
        self._inputDialog.setCurrentType(input_type)

    def _storeSettings(self):
        # handle single file input
        self._spec_file_setting = (
            self._inputDialog.getMainWindow().getDatFile(),
            self._inputDialog.getMainWindow().getEnergyColName(),
            self._inputDialog.getMainWindow().getAbsColName(),
            self._inputDialog.getMainWindow().getMonitorColName(),
            self._inputDialog.getMainWindow().getScanTitle(),
        )

        # handle spectra
        spectra_url = self._inputDialog.getMainWindow().getSpectraUrl()
        if spectra_url is not None:
            spectra_url = spectra_url.path()
        self._spectra_url_setting = spectra_url
        # handle energy
        energy_url = self._inputDialog.getMainWindow().getEnergyUrl()
        if energy_url is not None:
            assert energy_url.is_valid()
            energy_url = energy_url.path()
        self._energy_url_setting = energy_url
        # handle configuration
        configuration_url = self._inputDialog.getMainWindow().getConfigurationUrl()
        if configuration_url is not None:
            configuration_url = configuration_url.path()
        self._configuration_url_setting = configuration_url
        # save settings
        self._dimensions_setting = self._inputDialog.getMainWindow().getDimensions()
        # save energy
        self._energy_unit_settings = str(
            self._inputDialog.getMainWindow().getEnergyUnit()
        )
        # handle extra information like I0...
        advanceHDF5Info = self._inputDialog.getAdvanceHdf5Information()
        i0_url = advanceHDF5Info.getI0Url()
        if i0_url is not None:
            self._I0_url_setting = i0_url.path()
        i1_url = advanceHDF5Info.getI1Url()
        if i1_url is not None:
            self._I1_url_setting = i1_url.path()
        i2_url = advanceHDF5Info.getI2Url()
        if i2_url is not None:
            self._I2_url_setting = i2_url.path()
        mu_ref_url = advanceHDF5Info.getMuRefUrl()
        if mu_ref_url is not None:
            self._mu_ref_url_setting = mu_ref_url.path()

    def sizeHint(self):
        return qt.QSize(400, 200)
