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
    from est.core.process.larch.mback import larch_mback, process_spectr_mback
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
        self.configuration = {"mback": {"z": 29}}

    def tearDown(self):
        shutil.rmtree(self.outputdir)

    def testProcess(self):
        self.assertFalse(hasattr(self.spectrum, "fpp"))
        self.assertFalse(hasattr(self.spectrum, "f2"))
        conf, res_spectrum = process_spectr_mback(self.spectrum, self.configuration)
        self.assertTrue(hasattr(res_spectrum, "fpp"))
        self.assertTrue(hasattr(res_spectrum, "f2"))


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
        self.configuration = {"mback": {"z": 29}}
        energy, mu = read_ascii(self.data_file)
        self.xas_object = XASObject(
            spectra=(Spectrum(energy=energy, mu=mu),),
            energy=energy,
            dim1=1,
            dim2=1,
            configuration=self.configuration,
        )

    def tearDown(self):
        shutil.rmtree(self.outputdir)

    def testProcessXASObject(self):
        res = larch_mback(self.xas_object)
        assert isinstance(res, XASObject)
        spectrum0 = res.spectra.data.flat[0]
        self.assertTrue(hasattr(spectrum0, "fpp"))
        self.assertTrue(hasattr(spectrum0, "f2"))

    def testProcessAsDict(self):
        res = larch_mback(self.xas_object.to_dict())
        assert isinstance(res, XASObject)
        spectrum0 = res.spectra.data.flat[0]
        self.assertTrue(hasattr(spectrum0, "fpp"))
        self.assertTrue(hasattr(spectrum0, "f2"))


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestLarchSpectrum, TestLarchSpectra):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
