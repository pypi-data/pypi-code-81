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
from est.core.types import Dim

try:
    import PyMca5
except ImportError:
    has_pymca = False
else:
    has_pymca = True
    from PyMca5.PyMcaDataDir import PYMCA_DATA_DIR
    from est.core.process.pymca.exafs import pymca_exafs
    from est.io.utils.spec import read_spectrum
    from est.core.process.pymca.normalization import pymca_normalization

from est.core.types import Spectrum, XASObject


@unittest.skipIf(has_pymca is False, "PyMca5 is not installed")
class TestEXAFSSingleSpectrum(unittest.TestCase):
    """Make sure the process have valid io"""

    def setUp(self):
        data_file = os.path.join(PYMCA_DATA_DIR, "EXAFS_Cu.dat")
        energy, mu = read_spectrum(
            data_file,
            energy_col_name="Column 1",
            absorption_col_name="Column 2",
        )
        spectrum = Spectrum(energy=energy, mu=mu)
        exafs_configuration = {"Knots": {"Values": (1, 2, 5), "Number": 3}}
        configuration = {"EXAFS": exafs_configuration}
        self.input_ = XASObject(
            energy=energy,
            spectra=(spectrum,),
            dim1=1,
            dim2=1,
            configuration=configuration,
        )

        # first process normalization
        self.preproc_input_ = pymca_normalization(xas_obj=self.input_)
        assert "NormalizedBackground" in self.preproc_input_.spectra.data.flat[0]
        for spectrum in self.preproc_input_.spectra.data.flat:
            assert "NormalizedBackground" in spectrum

    def testPyMcaXASAsInput(self):
        res = pymca_exafs(self.preproc_input_)
        self.assertTrue(isinstance(res, XASObject))
        self.assertTrue("EXAFSKValues" in res.spectra.data.flat[0])
        self.assertTrue("EXAFSSignal" in res.spectra.data.flat[0])
        self.assertTrue("PostEdgeB" in res.spectra.data.flat[0])

    def testDictAsInput(self):
        """Test succeed if the input is a dict"""
        assert "NormalizedBackground" in self.preproc_input_.spectra.data.flat[0]
        res = pymca_exafs(self.preproc_input_)
        self.assertTrue(isinstance(res, XASObject))
        self.assertTrue("EXAFSKValues" in res.spectra.data.flat[0])
        self.assertTrue("EXAFSSignal" in res.spectra.data.flat[0])
        self.assertTrue("PostEdgeB" in res.spectra.data.flat[0])


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestEXAFSSingleSpectrum,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
