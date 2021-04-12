# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2017-2019 European Synchrotron Radiation Facility
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
__date__ = "06/26/2019"


import numpy
import os
import unittest
from est.core.types import Spectrum
from est.units import ur
from est.core.types import Dim

try:
    import PyMca5
except ImportError:
    has_pymca = False
else:
    has_pymca = True
    from PyMca5.PyMcaDataDir import PYMCA_DATA_DIR
    from est.io.utils.spec import read_spectrum


class TestSpectrum(unittest.TestCase):
    """Test the spectrum class"""

    @unittest.skipIf(has_pymca is False, "PyMca5 is not installed")
    def test_from_dat(self):
        """check that we can create a Spectrum from a pymca .dat file"""
        data_file = os.path.join(PYMCA_DATA_DIR, "EXAFS_Cu.dat")
        energy, mu = read_spectrum(
            data_file,
            energy_col_name="Column 1",
            absorption_col_name="Column 2",
        )
        spectrum = Spectrum(energy=energy, mu=mu)
        self.assertTrue(spectrum.energy is not None)
        self.assertTrue(spectrum.mu is not None)

    def test_from_numpy_array(self):
        """check that we can create a Spectrum from numpy arrays"""
        energy = numpy.arange(10, 20)
        mu = numpy.arange(10)
        spectrum = Spectrum(energy=energy, mu=mu)
        numpy.testing.assert_array_equal(spectrum.energy, (energy * ur.eV).m)
        numpy.testing.assert_array_equal(spectrum.mu, mu)
        mu_2 = numpy.arange(30, 40)
        spectrum["Mu"] = mu_2
        numpy.testing.assert_array_equal(spectrum.mu, mu_2)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestSpectrum,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
