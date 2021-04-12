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
__date__ = "07/30/2019"


from silx.gui import qt


class _OptionalQDoubleSpinBox(qt.QWidget):
    """
    Simple widget allowing to activate or tnoe the spin box
    """

    sigChanged = qt.Signal()
    """Signal emitted when parameters changed"""

    def __init__(self, parent):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QHBoxLayout())
        self._checkbox = qt.QCheckBox(parent=self)
        self.layout().addWidget(self._checkbox)
        self._spinBox = qt.QDoubleSpinBox(parent=self)
        self.layout().addWidget(self._spinBox)

        # default set up
        self._checkbox.setChecked(True)
        self._spinBox.setMinimum(-999999)
        self._spinBox.setMaximum(999999)
        self._lastValue = None

        # expose API
        self.setMinimum = self._spinBox.setMinimum
        self.setMaximum = self._spinBox.setMaximum

        # connect signal / slot
        self._checkbox.toggled.connect(self._updateSpinBoxStatus)
        self._spinBox.editingFinished.connect(self._valueChanged)

    def getValue(self):
        if self._checkbox.isChecked():
            return self._spinBox.value()
        else:
            return None

    def setValue(self, value):
        self._checkbox.setChecked(value is not None)
        if value is not None:
            self._spinBox.setValue(value)

    def _updateSpinBoxStatus(self, *arg, **kwargs):
        self._spinBox.setEnabled(self._checkbox.isChecked())
        self._valueChanged()

    def _valueChanged(self, *arg, **kwargs):
        if self._lastValue != self.getValue():
            self._lastValue = self.getValue()
            self.sigChanged.emit()


class _OptionalQIntSpinBox(qt.QWidget):
    """
    Simple widget allowing to activate or tnoe the spin box
    """

    sigChanged = qt.Signal()
    """Signal emitted when parameters changed"""

    def __init__(self, parent):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QHBoxLayout())
        self._checkbox = qt.QCheckBox(parent=self)
        self.layout().addWidget(self._checkbox)
        self._spinBox = qt.QSpinBox(parent=self)
        self.layout().addWidget(self._spinBox)

        # default set up
        self._checkbox.setChecked(True)
        self._lastValue = None

        # expose API
        self.setMinimum = self._spinBox.setMinimum
        self.setMaximum = self._spinBox.setMaximum
        self.setRange = self._spinBox.setRange

        # connect signal / slot
        self._checkbox.toggled.connect(self._updateSpinBoxStatus)
        self._spinBox.valueChanged.connect(self._valueChanged)

    def getValue(self):
        if self._checkbox.isChecked():
            return self._spinBox.value()
        else:
            return None

    def setValue(self, value):
        self._checkbox.setChecked(value is not None)
        if value is not None:
            self._spinBox.setValue(value)

    def _updateSpinBoxStatus(self, *arg, **kwargs):
        self._spinBox.setEnabled(self._checkbox.isChecked())
        self._valueChanged()

    def _valueChanged(self, *arg, **kwargs):
        if self._lastValue != self.getValue():
            self._lastValue = self.getValue()
            self.sigChanged.emit()
