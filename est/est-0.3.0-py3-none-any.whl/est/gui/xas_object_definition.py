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
__date__ = "03/07/2019"

from silx.gui.dialog.DataFileDialog import DataFileDialog
from silx.io.url import DataUrl
from silx.gui import qt
from est.core.io import read as read_xas, read_frm_file
from est.io import InputType
import logging
from est.core.types import Dim
from est.gui.unit.energy import EnergyUnitSelector
from est.core.utils.symbol import MU_CHAR
from typing import Iterable
from silx.io.spech5 import SpecFile

_logger = logging.getLogger(__name__)


class _InputType(qt.QWidget):
    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QHBoxLayout())
        self.layout().addWidget(qt.QLabel("input type:"))
        self._inputTypeCB = qt.QComboBox(parent=self)
        for input_type in InputType.values():
            self._inputTypeCB.addItem(input_type)
        self.layout().addWidget(self._inputTypeCB)

        # expose API
        self.currentChanged = self._inputTypeCB.currentIndexChanged

    def getInputType(self):
        """Return the current input type"""
        return InputType.from_value(self._inputTypeCB.currentText())

    def setInputType(self, input_type):
        _input_type = InputType.from_value(input_type)
        idx = self._inputTypeCB.findText(_input_type.value)
        assert idx >= 0
        self._inputTypeCB.setCurrentIndex(idx)


class XASObjectWindow(qt.QMainWindow):
    def __init__(self, parent):
        qt.QMainWindow.__init__(self, parent)
        self.setWindowFlags(qt.Qt.Widget)
        self._mainWindow = XASObjectDialog(self)
        self.setCentralWidget(self._mainWindow)

        self._plotDW = qt.QDockWidget(self)
        self.addDockWidget(qt.Qt.BottomDockWidgetArea, self._plotDW)
        self._plotDW.setFeatures(qt.QDockWidget.DockWidgetMovable)
        self._plot = _ToggleableSpectrumPlot(self)
        self._plotDW.setWidget(self._plot)

        # connect signal / slot
        self._mainWindow.editingFinished.connect(self.loadXasObject)

    def getMainWindow(self):
        return self._mainWindow

    def setDatFile(self, file_path):
        self._mainWindow.setDatFile(file_path=file_path)

    def setXmuFile(self, file_path):
        self._mainWindow.setXmuFile(file_path=file_path)

    def setCsvFile(self, file_path):
        self._mainWindow.setCsvFile(file_path=file_path)

    def setEnergyColName(self, name):
        self._mainWindow.setEnergyColName(name)

    def setAbsColName(self, name):
        self._mainWindow.setAbsColName(name)

    def setMonitorColName(self, name):
        self._mainWindow.setMonitorColName(name)

    def setScanTitle(self, name):
        self._mainWindow.setScanTitle(name)

    def setCurrentType(self, input_type):
        self._mainWindow.setCurrentType(input_type=input_type)

    def setSpectraUrl(self, url):
        self._mainWindow.setSpectraUrl(url=url)

    def setEnergyUrl(self, url):
        self._mainWindow.setEnergyUrl(url=url)

    def setEnergyUnit(self, unit):
        self._mainWindow.setEnergyUnit(unit=unit)

    def setDimensions(self, dims):
        self._mainWindow.setDimensions(dims=dims)

    def setConfigurationUrl(self, url):
        self._mainWindow.setConfigurationUrl(url)

    def getConfigurationUrl(self):
        return self._mainWindow.getConfigurationUrl()

    def getAdvanceHdf5Information(self):
        return self._mainWindow.getAdvanceHdf5Information()

    def loadXasObject(self):
        """Load XasObject from information contained in the GUI
        and update plot"""
        self._plot.clear()
        try:
            xas_obj = self._mainWindow.buildXASObject()
        except Exception as e:
            _logger.info(str(e))
        else:
            if xas_obj is not None:
                self._plot.setXasObject(xas_obj=xas_obj)

    def buildXASObject(self):
        return self._mainWindow.buildXASObject()


class _ToggleableSpectrumPlot(qt.QWidget):
    _BUTTON_ICON = qt.QStyle.SP_ToolBarVerticalExtensionButton

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent=parent)
        self.setLayout(qt.QGridLayout())
        self._toggleButton = qt.QPushButton(self)
        self.layout().addWidget(self._toggleButton, 0, 1, 1, 1)

        self._plot = _SpectrumPlot(parent=self)
        self.layout().addWidget(self._plot, 1, 0, 1, 2)
        # set up
        self._setButtonIcon(show=True)

        # Signal / slot connection
        self._toggleButton.clicked.connect(self.toggleSpectrumPlot)

    def toggleSpectrumPlot(self):
        visible = not self._plot.isVisible()
        self._setButtonIcon(show=visible)
        self._plot.setVisible(visible)

    def _setButtonIcon(self, show):
        style = qt.QApplication.instance().style()
        # return a QIcon
        icon = style.standardIcon(self._BUTTON_ICON)
        if show is False:
            pixmap = icon.pixmap(32, 32).transformed(qt.QTransform().scale(1, -1))
            icon = qt.QIcon(pixmap)
        self._toggleButton.setIcon(icon)

    def setXasObject(self, xas_obj):
        self._plot.setXasObject(xas_obj=xas_obj)

    def clear(self):
        self._plot.clear()


class _SpectrumPlot(qt.QWidget):
    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QHBoxLayout())
        from est.gui.XasObjectViewer import SpectrumViewer

        self._plot = SpectrumViewer(self)
        from est.gui.XasObjectViewer import _plot_spectrum

        self._plot.addCurveOperation(_plot_spectrum)
        self._plot.setWindowFlags(qt.Qt.Widget)
        # self._plot.setVisible(True)
        self.layout().addWidget(self._plot)

        # expose API
        self.addXMarker = self._plot._plotWidget.addXMarker

    def setXasObject(self, xas_obj):
        self._plot.setXasObject(xas_obj=xas_obj)

    def clear(self):
        self._plot.setXasObject(None)


class XASObjectDialog(qt.QWidget):
    """
    Interface used to select inputs for defining a XASObject
    """

    editingFinished = qt.Signal()

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QGridLayout())
        spacer = qt.QWidget(parent=self)
        spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        self.layout().addWidget(spacer, 0, 0)
        self._inputType = _InputType(parent=self)
        self.layout().addWidget(self._inputType, 0, 1)

        # single spectrum (.csv, .xmu)
        self._singleSpectrumDialog = _XASObjectFrmSingleSpectrum(parent=self)
        self.layout().addWidget(self._singleSpectrumDialog, 1, 0, 1, 2)
        # .h5 file
        self._h5Dialog = _XASObjFrmH5(parent=self)
        self.layout().addWidget(self._h5Dialog, 2, 0, 1, 2)
        # spec file
        self._specDialog = _XASObjectFrmSpec(parent=self)
        self.layout().addWidget(self._specDialog, 3, 0, 1, 2)

        spacer = qt.QWidget(parent=self)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self.layout().addWidget(spacer, 99, 0)

        # connect signal / slot
        self._inputType.currentChanged.connect(self._updateWidgetVisibility)
        self._inputType.currentChanged.connect(self._editingIsFinished)
        for diag in (self._singleSpectrumDialog, self._specDialog):
            diag._inputLe.editingFinished.connect(self._editingIsFinished)
        self._specDialog._dimensionWidget.sigInputChanged.connect(
            self._editingIsFinished
        )
        self._specDialog._scanTitleName.currentIndexChanged.connect(
            self._editingIsFinished
        )
        self._specDialog._inputLe.editingFinished.connect(self._updateSpecFile)
        self._h5Dialog.editingFinished.connect(self._editingIsFinished)

        # expose API
        self.getCurrentType = self._inputType.getInputType
        self.setCurrentType = self._inputType.setInputType
        self.setEnergyColName = self._specDialog.setEnergyColName
        self.getEnergyColName = self._specDialog.getEnergyColName
        self.setAbsColName = self._specDialog.setAbsColName
        self.getAbsColName = self._specDialog.getAbsColName
        self.setMonitorColName = self._specDialog.setMonitorColName
        self.getMonitorColName = self._specDialog.getMonitorColName
        self.setScanTitle = self._specDialog.setScanTitle
        self.getScanTitle = self._specDialog.getScanTitle
        self.setDatFile = self._specDialog.setFileSelected
        self.getDatFile = self._specDialog.getFileSelected
        self.setXmuFile = self._singleSpectrumDialog.setFileSelected
        self.setCsvFile = self._singleSpectrumDialog.setFileSelected
        self.setSpectraUrl = self._h5Dialog.setSpectraUrl
        self.getSpectraUrl = self._h5Dialog.getSpectraUrl
        self.setEnergyUrl = self._h5Dialog.setEnergyUrl
        self.getEnergyUrl = self._h5Dialog.getEnergyUrl
        self.setEnergyUnit = self._h5Dialog.setEnergyUnit
        self.getEnergyUnit = self._h5Dialog.getEnergyUnit
        self.setConfigurationUrl = self._h5Dialog.setConfigurationUrl
        self.getConfigurationUrl = self._h5Dialog.getConfigurationUrl
        self.getDimensions = self._h5Dialog.getDimensions
        self.setDimensions = self._h5Dialog.setDimensions

        # default setting
        self._updateWidgetVisibility()

    def getAdvanceHdf5Information(self):
        return self._h5Dialog.advanceInfo

    def _updateSpecFile(self, *args, **kwargs):
        self._specDialog._loadInfoFromSpecFile(self.getDatFile())

    def _updateWidgetVisibility(self):
        self._singleSpectrumDialog.setVisible(
            self._inputType.getInputType()
            in (InputType.xmu_spectrum, InputType.csv_spectrum)
        )
        self._h5Dialog.setVisible(
            self._inputType.getInputType() == InputType.hdf5_spectra
        )
        self._specDialog.setVisible(
            self._inputType.getInputType() == InputType.dat_spectrum
        )

    def buildXASObject(self):
        if self.getCurrentType() == InputType.dat_spectrum:
            specDiag = self._specDialog
            columns = specDiag.getColumnSelected()
            return read_frm_file(
                file_path=specDiag.getFileSelected(),
                energy_unit=specDiag.getEnergyUnit(),
                columns_names=columns,
            )
        elif self.getCurrentType() in (
            InputType.xmu_spectrum,
            InputType.csv_spectrum,
        ):
            spectrumDiag = self._singleSpectrumDialog
            return read_frm_file(
                file_path=spectrumDiag.getFileSelected(),
                energy_unit=spectrumDiag.getEnergyUnit(),
            )
        elif self.getCurrentType() == InputType.hdf5_spectra:
            spectra_url = self._h5Dialog.getSpectraUrl()
            energy_url = self._h5Dialog.getEnergyUrl()
            energy_unit = self._h5Dialog.getEnergyUnit()

            def check_url(url_path, name):
                if url_path in (None, ""):
                    raise ValueError(" ".join(("No", name, "url defined")))
                if isinstance(url_path, DataUrl):
                    url = url_path
                else:
                    url = DataUrl(path=url_path)
                if not url.is_valid():
                    raise ValueError(
                        " ".join(
                            (
                                name,
                                "url is invalid. Does the file / path still exists ?",
                            )
                        )
                    )

            check_url(spectra_url, "spectra")
            check_url(energy_url, "energy / channel")
            xas_obj = read_xas(
                spectra_url=self._h5Dialog.getSpectraUrl(),
                channel_url=self._h5Dialog.getEnergyUrl(),
                energy_unit=energy_unit,
                config_url=self._h5Dialog.getConfigurationUrl(),
                dimensions=self._h5Dialog.getDimensions(),
            )
            attr_names = "I0", "I1", "I2", "mu_ref"
            attr_values = (
                self._h5Dialog.advanceInfo.getI0Url(),
                self._h5Dialog.advanceInfo.getI1Url(),
                self._h5Dialog.advanceInfo.getI2Url(),
                self._h5Dialog.advanceInfo.getMuRefUrl(),
            )
            for attr_name, attr_value in zip(attr_names, attr_values):
                if attr_value is not None:
                    xas_obj.attach_3d_array(attr_name, attr_value)
            return xas_obj
        else:
            raise ValueError("unmanaged input type")

    def _editingIsFinished(self, *args, **kwargs):
        self.editingFinished.emit()


class _XASObjectFrmSingleSpectrum(qt.QWidget):
    """
    Interface used to define a XAS object from a single .dat file
    """

    class FileQLineEdit(qt.QLineEdit):
        """QLineEdit to handle a file path"""

        def dropEvent(self, event):
            if event.mimeData().hasFormat("text/uri-list"):
                for url in event.mimeData().urls():
                    self.setText(str(url.path()))

        def supportedDropActions(self):
            """Inherited method to redefine supported drop actions."""
            return qt.Qt.CopyAction | qt.Qt.MoveAction

        def dragEnterEvent(self, event):
            if event.mimeData().hasFormat("text/uri-list"):
                event.accept()
                event.setDropAction(qt.Qt.CopyAction)
            else:
                qt.QWidget.dragEnterEvent(self, event)

        def dragMoveEvent(self, event):
            if event.mimeData().hasFormat("text/uri-list"):
                event.setDropAction(qt.Qt.CopyAction)
                event.accept()
            else:
                qt.QWidget.dragMoveEvent(self, event)

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QGridLayout())

        # select file
        self.layout().addWidget(qt.QLabel("file", self), 0, 0, 1, 1)
        self._inputLe = self.FileQLineEdit("", self)
        self.layout().addWidget(self._inputLe, 0, 1, 1, 1)
        self._selectPB = qt.QPushButton("select", self)
        self.layout().addWidget(self._selectPB, 0, 2, 1, 1)

        # select energy
        self.layout().addWidget(qt.QLabel("energy unit", self), 1, 0, 1, 1)
        self._energyUnitSelector = EnergyUnitSelector(parent=self)
        self.layout().addWidget(self._energyUnitSelector, 1, 1, 1, 1)

        # spacer
        spacer = qt.QWidget(parent=self)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self.layout().addWidget(spacer, 999, 0, 1, 1)

        # signal / slot connection
        self._selectPB.pressed.connect(self._selectFile)

    def getFileSelected(self):
        return self._inputLe.text()

    def _getNameFilters(self):
        return ["spectrum (*.xmu, *.csv)", "All Files (*)"]

    def _selectFile(self, *args, **kwargs):
        old = self.blockSignals(True)
        dialog = qt.QFileDialog(self)
        dialog.setFileMode(qt.QFileDialog.ExistingFile)
        dialog.setNameFilters(self._getNameFilters())

        if not dialog.exec_():
            dialog.close()
            return

        fileSelected = dialog.selectedFiles()
        if len(fileSelected) == 0:
            return
        else:
            assert len(fileSelected) == 1
            self.setFileSelected(fileSelected[0])

        self.blockSignals(old)

    def setFileSelected(self, file_path):
        self._inputLe.setText(file_path)

    def getEnergyUnit(self):
        return self._energyUnitSelector.getUnit()

    def setEnergyUnit(self, unit):
        return self._energyUnitSelector.setUnit(unit=unit)


class _XASObjectFrmSpec(_XASObjectFrmSingleSpectrum):
    def __init__(self, parent):
        super().__init__(parent)

        self.layout().addWidget(qt.QLabel("scan title"), 2, 0, 1, 1)
        self._scanTitleName = qt.QComboBox(self)
        self.layout().addWidget(self._scanTitleName, 2, 1, 1, 1)
        # dimension definition
        self._dimensionWidget = _SpecColNames(parent=self)
        self.layout().addWidget(self._dimensionWidget, 3, 0, 1, 2)

    def _getNameFilters(self):
        return ["spec files (*.dat)", "All Files (*)"]

    def setScanTitle(self, scan_title):
        index = self._scanTitleName.findText(scan_title)
        if index >= 0:
            self._scanTitleName.setCurrentIndex(index)

    def getScanTitle(self):
        return self._scanTitleName.currentText()

    def setEnergyColName(self, name):
        self._dimensionWidget.setEnergyColName(name)

    def getEnergyColName(self):
        return self._dimensionWidget.getEnergyColName()

    def setAbsColName(self, name):
        self._dimensionWidget.setAbsColName(name)

    def getAbsColName(self):
        return self._dimensionWidget.getAbsColName()

    def setMonitorColName(self, name):
        self._dimensionWidget.setMonitorColName(name)

    def getMonitorColName(self):
        return self._dimensionWidget.getMonitorColName()

    def getColumnSelected(self):
        col_names = self._dimensionWidget.getColumnSelected()
        col_names["scan_title"] = self.getScanTitle()
        return col_names

    def _loadInfoFromSpecFile(self, file_path):
        old = self.blockSignals(True)
        try:
            self._dimensionWidget.setFile(file_path)
            spec_file = SpecFile(file_path)
            titles = set()
            for scan in spec_file:
                titles.add(scan.scan_header_dict["S"])
            titles = sorted(titles)
            for title in titles:
                self._scanTitleName.addItem(title)
        except Exception as e:
            _logger.warning(e)
        self.blockSignals(old)

    def setFileSelected(self, file_path):
        super().setFileSelected(file_path=file_path)
        self._loadInfoFromSpecFile(file_path=file_path)


class _URLSelector(qt.QWidget):
    def __init__(self, parent, name, layout=None, position=None):
        qt.QWidget.__init__(self, parent)
        self.name = name
        if layout is None:
            layout = self.setLayout(qt.QGridLayout())
            position = (0, 0)
        layout.addWidget(qt.QLabel(name + ":", parent=self), position[0], position[1])
        self._qLineEdit = qt.QLineEdit("", parent=self)
        layout.addWidget(self._qLineEdit, position[0], position[1] + 1)
        self._qPushButton = qt.QPushButton("select", parent=self)
        layout.addWidget(self._qPushButton, position[0], position[1] + 2)

        # connect signal / slot
        self._qPushButton.clicked.connect(self._selectFile)

    def _selectFile(self, *args, **kwargs):
        dialog = DataFileDialog(self)

        if not dialog.exec_():
            dialog.close()
            return None

        if dialog.selectedUrl() is not None:
            self._qLineEdit.setText(dialog.selectedUrl())

    def getUrlPath(self):
        url = self._qLineEdit.text()
        if url == "":
            return None
        else:
            return DataUrl(path=url)

    def setUrlPath(self, url):
        if isinstance(url, DataUrl):
            url = url.path()
        self._qLineEdit.setText(url)


class _XASObjFrmH5(qt.QTabWidget):
    """
    Interface used to define a XAS object from h5 files and data path
    """

    editingFinished = qt.Signal()
    """signal emitted when edition is finished"""

    def __init__(self, parent=None):
        qt.QTabWidget.__init__(self, parent)
        # Mandatory information
        self._basicInformation = _MandatoryXASObjFrmH5(self)
        self.addTab(self._basicInformation, "basic information")
        # Optional information
        self._advanceInformation = _OptionalRefsXASObjFrmH5(self)
        self.addTab(self._advanceInformation, "advanced information")

        # connect signal / slot
        self._basicInformation.editingFinished.connect(self._editingIsFinished)
        self._advanceInformation.editingFinished.connect(self._editingIsFinished)

        # expose API
        self.setDimensions = self._basicInformation.setDimensions
        self.getDimensions = self._basicInformation.getDimensions
        self.setConfigurationUrl = self._basicInformation.setConfigurationUrl
        self.getConfigurationUrl = self._basicInformation.getConfigurationUrl
        self.setEnergyUrl = self._basicInformation.setEnergyUrl
        self.getEnergyUrl = self._basicInformation.getEnergyUrl
        self.setSpectraUrl = self._basicInformation.setSpectraUrl
        self.getSpectraUrl = self._basicInformation.getSpectraUrl
        self.setEnergyUnit = self._basicInformation.setEnergyUnit
        self.getEnergyUnit = self._basicInformation.getEnergyUnit

    @property
    def advanceInfo(self):
        return self._advanceInformation

    def _editingIsFinished(self, *args, **kwargs):
        self.editingFinished.emit()


class _OptionalRefsXASObjFrmH5(qt.QWidget):
    """Widget containing optional information that we can associate to
    spectrum.
    """

    editingFinished = qt.Signal()
    """signal emitted when edition is finished"""

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QGridLayout())
        # I0
        self._I0Selector = _URLSelector(
            parent=self, name="I0 url", layout=self.layout(), position=(0, 0)
        )
        # I1
        self._I1Selector = _URLSelector(
            parent=self, name="I1 url", layout=self.layout(), position=(1, 0)
        )
        # I2
        self._I2Selector = _URLSelector(
            parent=self, name="I2 url", layout=self.layout(), position=(2, 0)
        )
        # mu ref
        self._muRefSelector = _URLSelector(
            parent=self,
            name="{} ref".format(MU_CHAR),
            layout=self.layout(),
            position=(3, 0),
        )

        # connect signal / slot
        self._I0Selector._qLineEdit.textChanged.connect(self._editingIsFinished)
        self._I1Selector._qLineEdit.textChanged.connect(self._editingIsFinished)
        self._I2Selector._qLineEdit.textChanged.connect(self._editingIsFinished)
        self._muRefSelector._qLineEdit.textChanged.connect(self._editingIsFinished)

    def _editingIsFinished(self, *args, **kwargs):
        self.editingFinished.emit()

    def getI0Url(self):
        return self._I0Selector.getUrlPath()

    def setI0Url(self, url):
        self._I0Selector.setUrlPath(url)

    def getI1Url(self):
        return self._I1Selector.getUrlPath()

    def setI1Url(self, url):
        self._I1Selector.setUrlPath(url)

    def getI2Url(self):
        return self._I2Selector.getUrlPath()

    def setI2Url(self, url):
        self._I2Selector.setUrlPath(url)

    def getMuRefUrl(self):
        return self._muRefSelector.getUrlPath()

    def setMuRefUrl(self, url):
        self._muRefSelector.setUrlPath(url)


class _MandatoryXASObjFrmH5(qt.QWidget):
    """Widget containing mandatory information"""

    editingFinished = qt.Signal()
    """signal emitted when edition is finished"""

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QGridLayout())
        # spectra url
        self._spectraSelector = _URLSelector(
            parent=self, name="spectra url", layout=self.layout(), position=(0, 0)
        )

        self._bufWidget = qt.QWidget(parent=self)
        self._bufWidget.setLayout(qt.QHBoxLayout())
        spacer = qt.QWidget(parent=self)
        spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        self._bufWidget.layout().addWidget(spacer)
        self._dimensionSelection = _SpectraDimensions(parent=self._bufWidget)
        self._bufWidget.layout().addWidget(self._dimensionSelection)
        self.layout().addWidget(self._bufWidget, 1, 1)

        # energy / channel url
        self._energySelector = _URLSelector(
            parent=self,
            name="energy /channel url",
            layout=self.layout(),
            position=(2, 0),
        )
        self._energyUnit = EnergyUnitSelector(parent=self)
        self.layout().addWidget(self._energyUnit, 2, 3, 1, 1)
        # configuration url
        self._configSelector = _URLSelector(
            parent=self, name="configuration url", layout=self.layout(), position=(3, 0)
        )

        # connect signal / slot
        self._spectraSelector._qLineEdit.textChanged.connect(self._editingIsFinished)
        self._energySelector._qLineEdit.textChanged.connect(self._editingIsFinished)
        self._configSelector._qLineEdit.textChanged.connect(self._editingIsFinished)
        self._dimensionSelection.sigDimensionChanged.connect(self._editingIsFinished)
        self._energyUnit.currentIndexChanged.connect(self._editingIsFinished)

        # expose APi
        self.setDimensions = self._dimensionSelection.setDimensions
        self.getDimensions = self._dimensionSelection.getDimensions

    def getSpectraUrl(self):
        """

        :return: the DataUrl of the spectra
        :rtype: DataUrl
        """
        return self._spectraSelector.getUrlPath()

    def getEnergyUrl(self):
        """

        :return: the DataUrl of energy / channel
        :rtype: DataUrl
        """
        return self._energySelector.getUrlPath()

    def getConfigurationUrl(self):
        """

        :return: the DataUrl of the configuration
        :rtype: DataUrl
        """
        return self._configSelector.getUrlPath()

    def setSpectraUrl(self, url):
        self._spectraSelector.setUrlPath(url)

    def setEnergyUrl(self, url):
        self._energySelector.setUrlPath(url)

    def setConfigurationUrl(self, url):
        self._configSelector.setUrlPath(url)

    def _editingIsFinished(self, *args, **kwargs):
        self.editingFinished.emit()

    def getDimensionsInfo(self):
        """

        :return: return the information regarding each dimensions
                 (dim0, dim1, dim2)
        :rtype: tuple
        """
        return self._dimensionSelection.getDimensions()

    def getEnergyUnit(self):
        return self._energyUnit.getUnit()

    def setEnergyUnit(self, unit):
        self._energyUnit.setUnit(unit=unit)


class _QColumnComboBox(qt.QComboBox):
    def __init__(self, parent):
        qt.QComboBox.__init__(self, parent)

    def setColumnsNames(self, colums_names: Iterable):
        for column_name in colums_names:
            self.addItem(column_name)

    def setColumnName(self, name):
        index = self.findText(name)
        if index >= 0:
            self.setCurrentIndex(index)
        else:
            _logger.info("Unable to find name: {}".format(name))

    def getColumnName(self):
        return self.currentText()


class _QDimComboBox(qt.QComboBox):
    def __init__(self, parent):
        qt.QComboBox.__init__(self, parent)
        self.addItem(Dim.DIM_0.value)
        self.addItem(Dim.DIM_1.value)
        self.addItem(Dim.DIM_2.value)

    def setDim(self, dim):
        dim = Dim.from_value(dim)
        assert dim in (Dim.DIM_0, Dim.DIM_1, Dim.DIM_2)
        index = self.findText(dim.value)
        assert index >= 0
        self.setCurrentIndex(index)

    def getDim(self):
        return Dim.from_value(self.currentText())


class _SpectraDimensions(qt.QWidget):
    sigDimensionChanged = qt.Signal()
    """Signal emitted when dimension change"""

    def __init__(self, parent):
        qt.QWidget.__init__(self, parent=parent)
        self.setLayout(qt.QFormLayout())
        self._dim0 = _QDimComboBox(parent=self)
        self.layout().addRow("dim 0", self._dim0)
        self._dim1 = _QDimComboBox(parent=self)
        self.layout().addRow("dim 1", self._dim1)
        self._dim2 = _QDimComboBox(parent=self)
        self.layout().addRow("dim 2", self._dim2)

        # set up
        self._dim0.setDim(Dim.DIM_2)
        self._dim1.setDim(Dim.DIM_1)
        self._dim2.setDim(Dim.DIM_0)

        # connect Signal / Slot
        self._dim0.currentTextChanged.connect(self._insureDimUnicity)
        self._dim1.currentTextChanged.connect(self._insureDimUnicity)
        self._dim2.currentTextChanged.connect(self._insureDimUnicity)

    def _insureDimUnicity(self):
        last_modified = self.sender()
        if last_modified is self._dim0:
            get_second, get_third = self._dim1, self._dim2
        elif last_modified is self._dim1:
            get_second, get_third = self._dim0, self._dim2
        elif last_modified is self._dim2:
            get_second, get_third = self._dim0, self._dim1
        else:
            raise RuntimeError("Sender should be in dim0, dim1, dim2")

        assert last_modified != get_second
        assert last_modified != get_third
        assert type(last_modified) == type(get_second) == type(get_third)
        value_set = {Dim.DIM_2, Dim.DIM_0, Dim.DIM_1}
        last_value_set = last_modified.getDim()
        value_set.remove(last_value_set)

        old_1 = last_modified.blockSignals(True)
        old_2 = get_second.blockSignals(True)
        old_3 = get_third.blockSignals(True)
        if get_second.getDim() in value_set:
            value_set.remove(get_second.getDim())
            get_third.setDim(value_set.pop())
        elif get_third.getDim() in value_set:
            value_set.remove(get_third.getDim())
            get_second.setDim(value_set.pop())
        else:
            get_second.setDim(value_set.pop())
            get_third.setDim(value_set.pop())

        last_modified.blockSignals(old_1)
        get_second.blockSignals(old_2)
        get_third.blockSignals(old_3)
        self.sigDimensionChanged.emit()

    def getDimensions(self):
        """

        :return: return the information regarding each dimensions
                 (dim0, dim1, dim2)
        :rtype: tuple
        """
        return (
            self._dim0.currentText(),
            self._dim1.currentText(),
            self._dim2.currentText(),
        )

    def setDimensions(self, dims):
        """

        :param dims: tuple containing (dim0, dim1, dim2)
        :type: tuple
        """
        assert isinstance(dims, tuple)
        assert len(dims) == 3
        self._dim0.setDim(dims[0])
        self._dim1.setDim(dims[1])
        self._dim2.setDim(dims[2])


class _SpecColNames(qt.QWidget):
    sigInputChanged = qt.Signal()
    """Signal emitted when dimension change"""

    def __init__(self, parent):
        qt.QWidget.__init__(self, parent=parent)
        self.setLayout(qt.QFormLayout())
        self._energyColNamCB = _QColumnComboBox(parent=self)
        self.layout().addRow("energy col name", self._energyColNamCB)
        self._absColNamCB = _QColumnComboBox(parent=self)
        self.layout().addRow("absorption col name", self._absColNamCB)
        self._monitorColNamCB = _QColumnComboBox(parent=self)
        self._monitorColNamCB.setEnabled(False)
        self._useMonitorCB = qt.QCheckBox("monitor col name")
        self.layout().addRow(self._useMonitorCB, self._monitorColNamCB)

        # connect Signal / Slot
        self._energyColNamCB.currentIndexChanged.connect(self._propagateSigChanged)
        self._absColNamCB.currentIndexChanged.connect(self._propagateSigChanged)
        self._monitorColNamCB.currentIndexChanged.connect(self._propagateSigChanged)
        self._useMonitorCB.toggled.connect(self._monitorColNamCB.setEnabled)
        self._useMonitorCB.toggled.connect(self._propagateSigChanged)

    def _propagateSigChanged(self):
        self.sigInputChanged.emit()

    def getColumnSelected(self) -> dict:
        """

        :return: return the information regarding each energy and mu
        :rtype: dict
        """
        return {
            "energy": self._energyColNamCB.currentText(),
            "mu": self._absColNamCB.currentText(),
            "monitor": self.getMonitorColName(),
        }

    def getMonitorColName(self):
        if self.useMonitor():
            return self._monitorColNamCB.currentText()
        else:
            return None

    def useMonitor(self):
        return self._useMonitorCB.isChecked()

    def setEnergyColName(self, name):
        self._energyColNamCB.setColumnName(name)

    def getEnergyColName(self):
        return self._energyColNamCB.getColumnName()

    def setAbsColName(self, name):
        self._absColNamCB.setColumnName(name)
        if isinstance(name, str):
            self._useMonitorCB.setChecked(True)

    def getAbsColName(self):
        return self._absColNamCB.getColumnName()

    def setMonitorColName(self, name):
        self._monitorColNamCB.setColumnName(name)

    def setFile(self, file_path):
        old = self.blockSignals(True)
        prev_energy = self._energyColNamCB.currentText()
        prev_absorption = self._absColNamCB.currentText()
        prev_monitor = self._monitorColNamCB.currentText()
        self._energyColNamCB.clear()
        self._absColNamCB.clear()
        self._monitorColNamCB.clear()

        spec_file = SpecFile(file_path)
        col_names = set()
        for scan in spec_file:
            col_names.update(scan.labels)
        # sort column name
        col_names = sorted(col_names)
        self._energyColNamCB.setColumnsNames(col_names)
        self._absColNamCB.setColumnsNames(col_names)
        self._monitorColNamCB.setColumnsNames(col_names)
        self._energyColNamCB.setColumnName(prev_energy)
        self._absColNamCB.setColumnName(prev_absorption)
        self._monitorColNamCB.setColumnName(prev_monitor)
        self.blockSignals(old)
