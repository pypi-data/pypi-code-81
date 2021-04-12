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
"""Tools for noise calculation"""


__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "18/01/2021"


from silx.gui import qt
from est.gui.XasObjectViewer import SpectrumViewer
from est.gui.XasObjectViewer import _plot_noise_savgol, _plot_norm_noise_savgol
import numpy


class _QOddSpinBox(qt.QSpinBox):
    """
    SpinBox dedicated to odd numbers
    """

    oddValueChanged = qt.Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.valueChanged.connect(self.onValueChanged)
        self.before_value = self.value()

    def onValueChanged(self, i):
        if not self.isValid(i):
            self.setValue(self.before_value)
        else:
            self.oddValueChanged.emit(i)
            self.before_value = i

    def isValid(self, value):
        if (value % 2) == 1:
            return True
        return False


class _SavitskyGolayNoiseOpts(qt.QWidget):
    sigChanged = qt.Signal()
    """signal emitted when parameters change"""

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QFormLayout())

        ## Inputs
        self.layout().addRow(qt.QLabel("Inputs", self))

        # add window size
        self._windowSize = _QOddSpinBox(self)
        self._windowSize.setValue(5)
        self._windowSize.setSingleStep(2)
        self.layout().addRow(qt.QLabel("     - window size", self), self._windowSize)
        self._windowSize.setToolTip(
            "window size to provide to the Savitsky-Golay algorithm"
        )
        # add polynomial order
        self._polynomialOrder = qt.QSpinBox(self)
        self._polynomialOrder.setValue(2)
        self.layout().addRow(
            qt.QLabel("     - polynomial order", self), self._polynomialOrder
        )
        self._polynomialOrder.setToolTip(
            "window size to provide to the Savitsky-Golay algorithm"
        )
        # E start
        self._eStart = qt.QDoubleSpinBox(self)
        self._eStart.setRange(0, 10000000001)
        self._eStart.setSuffix("eV")
        self._eStart.setValue(100)
        self.layout().addRow(qt.QLabel("     - E start", self), self._eStart)

        # E end
        self._eEnd = qt.QDoubleSpinBox(self)
        self._eEnd.setRange(0, 10000000001)
        self._eEnd.setSuffix("eV")
        self._eEnd.setValue(10000000000)
        self.layout().addRow(qt.QLabel("     - E end", self), self._eEnd)

        ## Outputs
        self.layout().addRow(qt.QLabel("Outputs", self))
        # raw data average noise
        self._rawData = qt.QLineEdit("", self)
        self._rawData.setReadOnly(True)
        self.layout().addRow(
            qt.QLabel("     - Raw data average noise (blue)", self), self._rawData
        )
        self._rawData.setToolTip(
            "Raw data average noise is calculated as the difference between "
            "the raw spectrum and the spectrum smoothed with Savitsky-Golay "
            "algorithm (with provided window size and polynomial order)"
        )

        # edge step
        self._edgeStep = qt.QLineEdit("", self)
        self._edgeStep.setReadOnly(True)
        self.layout().addRow(qt.QLabel("     - edge step", self), self._edgeStep)
        self._edgeStep.setToolTip(
            "Edge step is defined during the normalization (pymca) or the "
            "pre-edge step (larch)"
        )

        # normalized noise
        self._normalizedNoise = qt.QLineEdit("", self)
        self._normalizedNoise.setReadOnly(True)
        self.layout().addRow(
            qt.QLabel("     - Normalized noise (red)", self), self._normalizedNoise
        )
        self._normalizedNoise.setToolTip("Average noise divided by edge jump")

        # connect signal / slot
        self._windowSize.oddValueChanged.connect(self._changed)
        self._polynomialOrder.valueChanged.connect(self._changed)

    def getWindowSize(self):
        return self._windowSize.value()

    def setWindowSize(self, size):
        if size < 1:
            return
        self._windowSize.setValue(size)

    def getPolynomialOrder(self):
        return self._polynomialOrder.value()

    def setPolynomialOrder(self, order):
        if order < 1:
            return
        self._polynomialOrder.setValue(order)

    def getEStart(self):
        return self._eStart.value()

    def setEStart(self, e_min):
        if e_min > 0:
            self._eStart.setValue(e_min)

    def getEEnd(self):
        return self._eEnd.value()

    def setEEnd(self, e_max):
        if e_max > 0:
            self._eEnd.setValue(e_max)

    def getParameters(self):
        return {
            "window_size": self.getWindowSize(),
            "polynomial_order": self.getPolynomialOrder(),
            "e_min": self.getEStart(),
            "e_max": self.getEEnd(),
        }

    def setParameters(self, config):
        if "window_size" in config:
            self.setWindowSize(config["window_size"])
        if "polynomial_order" in config:
            self.setPolynomialOrder(config["polynomial_order"])
        if "e_min" in config:
            self.setEStart(config["e_min"])
        if "e_max" in config:
            self.setEEnd(config["e_max"])

    def _changed(self, *args, **kwargs):
        self.sigChanged.emit()

    def setSpectrum(self, spectrum):
        if spectrum.noise_savgol is not None:
            self._rawData.setText("{:.5E}".format(numpy.mean(spectrum.noise_savgol)))
        else:
            self._rawData.clear()
        if hasattr(spectrum, "edge_step"):
            self._edgeStep.setText("{:.3f}".format(spectrum.edge_step))
        else:
            self._edgeStep.setText("?")
        if spectrum.norm_noise_savgol is not None:
            self._normalizedNoise.setText("{:.5E}".format(spectrum.norm_noise_savgol))
        else:
            self._normalizedNoise.clear()


class SavitskyGolayNoise(qt.QMainWindow):
    """
    Widget to tune SavitskyGolayNoise and display the results
    """

    sigChanged = qt.Signal()
    """signal emitted when parameters change"""

    def __init__(self, parent):
        qt.QMainWindow.__init__(self, parent)
        self.setWindowFlags(qt.Qt.Widget)

        # define centre widget
        self._plot = SpectrumViewer()
        self._plot.setYAxisLogarithmic(True)
        for ope in (_plot_noise_savgol, _plot_norm_noise_savgol):
            self._plot.addCurveOperation(ope)
        self.setCentralWidget(self._plot)

        # options
        self._options = _SavitskyGolayNoiseOpts(parent=self)
        self._optionsDW = qt.QDockWidget(self)
        self._optionsDW.setWidget(self._options)
        self._optionsDW.setAllowedAreas(
            qt.Qt.RightDockWidgetArea | qt.Qt.LeftDockWidgetArea
        )
        self.addDockWidget(qt.Qt.RightDockWidgetArea, self._optionsDW)
        self._optionsDW.setFeatures(qt.QDockWidget.DockWidgetMovable)

        # connect signal / plot
        self._options.sigChanged.connect(self._changed)
        self._plot.sigSpectrumChanged.connect(self._updateSpectrumInfo)

    def setXASObj(self, xas_obj):
        self._plot.setXasObject(xas_obj=xas_obj)

    def getParameters(self):
        return self._options.getParameters()

    def setParameters(self, config):
        self._options.setParameters(config=config)

    def getWindowSize(self):
        return self._options.getWindowSize()

    def setWindowSize(self, size):
        self._options.setWindowSize(size=size)

    def getPolynomialOrder(self):
        return self._options.getPolynomialOrder()

    def setPolynomialOrder(self, order):
        self._options.setPolynomialOrder(order=order)

    def _changed(self, *args, **kwargs):
        self.sigChanged.emit()

    def _updateSpectrumInfo(self):
        current_spectrum = self._plot.getCurrentSpectrum()
        if current_spectrum is not None:
            self._options.setSpectrum(spectrum=current_spectrum)
