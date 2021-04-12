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
__date__ = "06/11/2019"


import os
import unittest
from est.core.types import XASObject, Spectrum
from est.core.types import Dim

try:
    import PyMca5
except ImportError:
    has_pymca = False
else:
    has_pymca = True
    from PyMca5.PyMcaDataDir import PYMCA_DATA_DIR
    from est.core.process.pymca.exafs import pymca_exafs
    from est.core.process.pymca.ft import pymca_ft
    from est.core.process.pymca.k_weight import pymca_k_weight
    from est.core.process.pymca.normalization import pymca_normalization
    from est.io.utils.spec import read_spectrum


@unittest.skipIf(has_pymca is False, "PyMca5 is not installed")
class TestFTSingleSpectrum(unittest.TestCase):
    """Make sure the process have valid io"""

    def setUp(self):
        data_file = os.path.join(PYMCA_DATA_DIR, "EXAFS_Cu.dat")
        energy, mu = read_spectrum(
            data_file,
            energy_col_name="Column 1",
            absorption_col_name="Column 2",
        )
        self.spectrum = Spectrum(energy=energy, mu=mu)
        self.xas_obj = XASObject(
            energy=energy, spectra=(self.spectrum,), dim1=1, dim2=1
        )
        # preproc xas obj
        self.xas_obj = pymca_normalization(xas_obj=self.xas_obj)
        self.xas_obj = pymca_exafs(xas_obj=self.xas_obj)
        self.xas_obj = pymca_k_weight(xas_obj=self.xas_obj)

    def testPyMcaXASAsInput(self):
        res = pymca_ft(xas_obj=self.xas_obj)
        self.assertTrue(isinstance(res, XASObject))
        self.assertTrue("FTRadius" in res.spectra.data.flat[0]["FT"])
        self.assertTrue("FTImaginary" in res.spectra.data.flat[0]["FT"])
        self.assertTrue("FTIntensity" in res.spectra.data.flat[0]["FT"])

    def testDictAsInput(self):
        res = pymca_ft(xas_obj=self.xas_obj.to_dict())
        self.assertTrue(isinstance(res, XASObject))
        self.assertTrue("FTRadius" in res.spectra.data.flat[0]["FT"])
        self.assertTrue("FTImaginary" in res.spectra.data.flat[0]["FT"])
        self.assertTrue("FTIntensity" in res.spectra.data.flat[0]["FT"])


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestFTSingleSpectrum,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
