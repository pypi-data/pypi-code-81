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
"""Tools to select energy unit"""


__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "31/03/2020"


from silx.gui import qt
from est.units import ur


class EnergyUnitSelector(qt.QComboBox):
    """Simple class to define a unit for energy"""

    def __init__(self, parent=None):
        qt.QComboBox.__init__(self, parent)
        for unit in ("eV", "keV", "J", "kJ"):
            self.addItem(unit)

    def getUnit(self):
        current_unit = self.currentText()
        if current_unit == "eV":
            return ur.eV
        elif current_unit == "keV":
            return ur.keV
        elif current_unit == "J":
            return ur.J
        elif current_unit == "kJ":
            return ur.kJ
        else:
            raise ValueError("current unit is not supported")

    def setUnit(self, unit: str) -> None:
        if unit in ("eV", "keV", "J", "kJ"):
            txt = unit
        elif unit == ur.eV:
            txt = "eV"
        elif unit == ur.keV:
            txt = "keV"
        elif unit == ur.J:
            txt = "J"
        elif unit == ur.kJ:
            txt = "kJ"
        else:
            raise ValueError("Given unit is not managed: {}".format())

        index = self.findText(txt)
        if index >= 0:
            self.setCurrentIndex(index)
