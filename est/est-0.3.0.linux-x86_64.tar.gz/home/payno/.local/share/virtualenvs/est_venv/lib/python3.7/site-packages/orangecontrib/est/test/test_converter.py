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
__date__ = "08/08/2019"

import unittest
from est.core.types import XASObject
from orangecontrib.est.utils import Converter
from est.core.utils import spectra as spectra_utils
import numpy


class TestConverter(unittest.TestCase):
    """Test conversion of xas_object to Orange.data.Table"""

    def setUp(self):
        self.energy, self.spectra = spectra_utils.create_dataset((128, 20, 1))
        self.xas_object = XASObject(
            energy=self.energy, spectra=self.spectra, dim1=20, dim2=10
        )

    def test_conversion(self):
        """Make sure the conversion to/from Orange.data.Table is safe for energy
        and beam absorption
        """
        xas_object = self.xas_object.copy(create_h5_file=False)
        data_table = Converter.toDataTable(xas_object=xas_object)
        converted_xas_object = Converter.toXASObject(data_table=data_table)
        numpy.testing.assert_array_almost_equal(
            xas_object.energy, converted_xas_object.energy
        )
        numpy.testing.assert_array_almost_equal(
            xas_object.spectra[0].mu, converted_xas_object.spectra[0].mu
        )
        numpy.testing.assert_array_almost_equal(
            xas_object.spectra[5].mu, converted_xas_object.spectra[5].mu
        )
        numpy.testing.assert_array_almost_equal(
            xas_object.spectra[18].mu, converted_xas_object.spectra[18].mu
        )


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestConverter,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite
