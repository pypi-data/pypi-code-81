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
"""Tools to select energy roi"""


__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "27/01/2021"


from silx.gui import qt
from est.gui.xas_object_definition import _SpectrumPlot


class _RoiSettings(qt.QWidget):

    sigValueChanged = qt.Signal()
    """signal emitted when roi value is changed"""

    MAX_VALUE = 999999999

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QFormLayout())
        self._minE = qt.QDoubleSpinBox(self)
        self._minE.setRange(0, _RoiSettings.MAX_VALUE)
        self._minE.setValue(0)
        self.layout().addRow("min E", self._minE)
        self._maxE = qt.QDoubleSpinBox(self)
        self._maxE.setRange(0, _RoiSettings.MAX_VALUE)
        self._maxE.setValue(_RoiSettings.MAX_VALUE)
        self.layout().addRow("max E", self._maxE)

        # connect signal / slot
        self._minE.editingFinished.connect(self._changed)
        self._maxE.editingFinished.connect(self._changed)

    def _changed(self):
        self.sigValueChanged.emit()

    def setRangeE(self, min_E, max_E):
        old = self.blockSignals(True)
        self._minE.setValue(min_E)
        self._maxE.setValue(max_E)
        self.blockSignals(old)
        self.sigValueChanged.emit()

    def getMinE(self):
        return self._minE.value()

    def setMinE(self, value):
        self._minE.setValue(value)

    def getMaxE(self):
        return self._maxE.value()

    def setMaxE(self, value):
        self._maxE.setValue(value)

    def getROI(self):
        return self.getMinE(), self.getMaxE()

    def setROI(self, roi):
        min, max = roi
        self.setMinE(min)
        self.setMaxE(max)

    def hasntBeenModified(self):
        return (self._minE.value() == 0) and (
            self._maxE.value() == _RoiSettings.MAX_VALUE
        )


class EnergyRoiWidget(qt.QMainWindow):
    def __init__(self, parent=None):
        qt.QMainWindow.__init__(self, parent)
        self.setWindowFlags(qt.Qt.Widget)

        # plot
        self._plot = _SpectrumPlot(self)
        self.setCentralWidget(self._plot)

        # roi settings
        self._widget = _RoiSettings(self)
        dockWidget = qt.QDockWidget(parent=self)
        dockWidget.setWidget(self._widget)
        self.addDockWidget(qt.Qt.RightDockWidgetArea, dockWidget)
        dockWidget.setAllowedAreas(qt.Qt.RightDockWidgetArea | qt.Qt.LeftDockWidgetArea)
        dockWidget.setFeatures(qt.QDockWidget.NoDockWidgetFeatures)

        # add Markers
        self._minEMarker = self._plot.addXMarker(
            self._widget.getMinE(),
            legend="from",
            color="red",
            draggable=True,
            text="min E",
        )

        self._maxEMarker = self._plot.addXMarker(
            self._widget.getMaxE(),
            legend="to",
            color="red",
            draggable=True,
            text="max E",
        )

        # expose API
        self.setROI = self._widget.setROI
        self.getROI = self._widget.getROI

        # connect signal / slot
        self._widget.sigValueChanged.connect(self._updateROIAnchors)
        self._getMinMarker().sigDragFinished.connect(self._updateMinValuefrmMarker)
        self._getMaxMarker().sigDragFinished.connect(self._updateMaxValuefrmMarker)

    def setXasObject(self, xas_obj):
        if xas_obj is None:
            self._plot.clear()
        else:
            self._plot.setXasObject(xas_obj)
            if self._widget.hasntBeenModified() and xas_obj.energy is not None:
                self._widget.setRangeE(xas_obj.energy.min(), xas_obj.energy.max())

    def getXasObject(self):
        return self._plot._plot.xas_obj

    def _getMinMarker(self):
        return self._plot._plot._plotWidget._getMarker(self._minEMarker)

    def _getMaxMarker(self):
        return self._plot._plot._plotWidget._getMarker(self._maxEMarker)

    def _updateROIAnchors(self):
        oldMinMarker = self._getMinMarker().blockSignals(True)
        oldMaxMarker = self._getMaxMarker().blockSignals(True)

        self._getMinMarker().setPosition(self._widget.getMinE(), 0)
        self._getMaxMarker().setPosition(self._widget.getMaxE(), 0)

        self._getMinMarker().blockSignals(oldMinMarker)
        self._getMaxMarker().blockSignals(oldMaxMarker)

    def _updateMinValuefrmMarker(self):
        old = self._widget.blockSignals(True)
        self._widget.setMinE(self._getMinMarker().getPosition()[0])
        self._widget.blockSignals(old)

    def _updateMaxValuefrmMarker(self):
        old = self._widget.blockSignals(True)
        self._widget.setMaxE(self._getMaxMarker().getPosition()[0])
        self._widget.blockSignals(old)
