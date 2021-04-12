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
import shutil
import tempfile
import unittest
import h5py
from silx.io.url import DataUrl
from est.core.io import read as read_xas
from est.core.types import Spectrum, XASObject
from est.core.types import Spectra
from est.core.utils import spectra as spectra_utils
from est.core.types import Dim

try:
    import PyMca5
except ImportError:
    has_pymca = False
else:
    has_pymca = True
    from PyMca5.PyMcaDataDir import PYMCA_DATA_DIR
    from est.core.process.pymca.normalization import pymca_normalization
    from est.io.utils.spec import read_spectrum


@unittest.skipIf(has_pymca is False, "PyMca5 is not installed")
class TestNormalizationSingleSpectrum(unittest.TestCase):
    """Make sure the process is processing correctly on a spectrum"""

    def setUp(self):
        data_file = os.path.join(PYMCA_DATA_DIR, "EXAFS_Cu.dat")
        energy, mu = read_spectrum(
            data_file,
            energy_col_name="Column 1",
            absorption_col_name="Column 2",
        )
        self.spectrum = Spectrum(energy=energy, mu=mu)
        self.xas_obj = XASObject(
            spectra=(self.spectrum,), energy=energy, dim1=1, dim2=1
        )

    def testWithXASObjAsInput(self):
        res = pymca_normalization(xas_obj=self.xas_obj)
        self.assertTrue(isinstance(res, XASObject))
        self.assertTrue(isinstance(res.spectra, (Spectra)))
        res_spectrum = res.spectra.data.flat[0]
        self.assertTrue(isinstance(res_spectrum, Spectrum))
        self.assertTrue("NormalizedMu" in res_spectrum)
        self.assertTrue("NormalizedEnergy" in res_spectrum)
        self.assertTrue("NormalizedSignal" in res_spectrum)

    def testWithDictAsInput(self):
        res = pymca_normalization(xas_obj=self.xas_obj.to_dict())
        self.assertTrue(isinstance(res, XASObject))
        self.assertTrue("NormalizedMu" in res.spectra.data.flat[0])
        self.assertTrue("NormalizedEnergy" in res.spectra.data.flat[0])
        self.assertTrue("NormalizedSignal" in res.spectra.data.flat[0])


@unittest.skipIf(has_pymca is False, "PyMca5 is not installed")
class TestNormalizationMultipleSpectrum(unittest.TestCase):
    """Make sure the process is processing correctly on a XASObject spectra"""

    def setUp(self):
        self.energy, self.spectra = spectra_utils.create_dataset(shape=(256, 20, 10))
        self.output_dir = tempfile.mkdtemp()
        spectra_path = "/data/NXdata/data"
        channel_path = "/data/NXdata/Channel"
        filename = os.path.join(self.output_dir, "myfile.h5")
        with h5py.File(filename, "a") as f:
            f[spectra_path] = self.spectra
            f[channel_path] = self.energy

        self.xas_obj = read_xas(
            spectra_url=DataUrl(
                file_path=filename, data_path=spectra_path, scheme="silx"
            ),
            channel_url=DataUrl(
                file_path=filename, data_path=channel_path, scheme="silx"
            ),
            dimensions=(Dim.DIM_2, Dim.DIM_1, Dim.DIM_0),
        )

    def tearDown(self):
        shutil.rmtree(path=self.output_dir)

    def testWithXASObjAsInput(self):
        res = pymca_normalization(xas_obj=self.xas_obj)
        self.assertTrue(isinstance(res, XASObject))
        for spectrum in self.xas_obj.spectra.data.flat:
            self.assertTrue("NormalizedMu" in spectrum)
            self.assertTrue("NormalizedEnergy" in spectrum)
            self.assertTrue("NormalizedSignal" in spectrum)

    def testWithDictAsInput(self):
        pass


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestNormalizationSingleSpectrum, TestNormalizationMultipleSpectrum):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
