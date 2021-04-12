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
__date__ = "07/25/2019"

import os
import unittest
import tempfile
import shutil
import urllib.request
from est.core.types import Spectrum, XASObject

try:
    import larch
except ImportError:
    has_larch = False
else:
    has_larch = True
    from est.core.process.larch.xftf import larch_xftf, process_spectr_xftf
    from est.core.process.larch.autobk import process_spectr_autobk
    from est.io.utils.larch import read_ascii


@unittest.skipIf(has_larch is False, "xraylarch not installed")
class TestLarchSpectrum(unittest.TestCase):
    """Make sure computation on one spectrum is valid"""

    def setUp(self):
        self.outputdir = tempfile.mkdtemp()
        xmu_url = "https://raw.githubusercontent.com/xraypy/xraylarch/master/examples/xafs/cu_rt01.xmu"
        self.data_file = os.path.join(self.outputdir, "cu_rt01.xmu")

        with urllib.request.urlopen(xmu_url) as response, open(
            self.data_file, "wb"
        ) as out_file:
            data = response.read()  # a `bytes` object
            out_file.write(data)

        assert os.path.exists(self.data_file)
        energy, mu = read_ascii(self.data_file)
        self.spectrum = Spectrum(energy=energy, mu=mu)
        self.configuration = {
            "window": "hanning",
            "kweight": 2,
            "kmin": 3,
            "kmax": 13,
            "dk": 1,
        }
        # for xftf we need to compute pre edge before
        process_spectr_autobk(self.spectrum, configuration={}, overwrite=True)
        assert hasattr(self.spectrum, "k")
        assert hasattr(self.spectrum, "chi")

    def tearDown(self):
        shutil.rmtree(self.outputdir)

    def testProcess(self):
        process_spectr_xftf(self.spectrum, self.configuration, overwrite=True)
        self.assertTrue(hasattr(self.spectrum, "chir_re"))
        self.assertTrue(hasattr(self.spectrum, "chir_im"))
        self.assertTrue(hasattr(self.spectrum, "chir"))
        self.assertTrue(hasattr(self.spectrum, "chir_mag"))


@unittest.skipIf(has_larch is False, "xraylarch not installed")
class TestLarchSpectra(unittest.TestCase):
    """Make sure computation on spectra is valid (n spectrum)"""

    def setUp(self):
        self.outputdir = tempfile.mkdtemp()
        # Download test file from xraylarch
        xmu_url = "https://raw.githubusercontent.com/xraypy/xraylarch/master/examples/xafs/cu_rt01.xmu"
        self.data_file = os.path.join(self.outputdir, "cu_rt01.xmu")
        with urllib.request.urlopen(xmu_url) as response, open(
            self.data_file, "wb"
        ) as out_file:
            data = response.read()  # a `bytes` object
            out_file.write(data)
        assert os.path.exists(self.data_file)
        # define the xas object
        self.configuration = {"z": 29}
        energy, mu = read_ascii(self.data_file)
        spectrum = Spectrum(energy=energy, mu=mu)
        process_spectr_autobk(spectrum, configuration={}, overwrite=True)
        self.xas_object = XASObject(
            spectra=(spectrum,),
            energy=energy,
            dim1=1,
            dim2=1,
            configuration=self.configuration,
        )
        # for xftf we need to compute pre edge before
        spectrum = self.xas_object.spectra.data.flat[0]
        assert hasattr(spectrum, "k")
        assert hasattr(spectrum, "chi")

    def tearDown(self):
        shutil.rmtree(self.outputdir)

    def testProcessXASObject(self):
        res = larch_xftf(self.xas_object)
        assert isinstance(res, XASObject)
        spectrum = res.spectra.data.flat[0]
        self.assertTrue(hasattr(spectrum, "chir_re"))
        self.assertTrue(hasattr(spectrum, "chir_im"))
        self.assertTrue(hasattr(spectrum, "chir"))
        self.assertTrue(hasattr(spectrum, "chir_mag"))

    def testProcessAsDict(self):
        res = larch_xftf(self.xas_object.to_dict())
        assert isinstance(res, XASObject)
        spectrum = res.spectra.data.flat[0]
        self.assertTrue(hasattr(spectrum, "chir_re"))
        self.assertTrue(hasattr(spectrum, "chir_im"))
        self.assertTrue(hasattr(spectrum, "chir"))
        self.assertTrue(hasattr(spectrum, "chir_mag"))


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestLarchSpectrum, TestLarchSpectra):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
