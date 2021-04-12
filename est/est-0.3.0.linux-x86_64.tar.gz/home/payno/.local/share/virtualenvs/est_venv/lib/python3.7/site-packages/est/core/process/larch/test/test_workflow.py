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
import numpy
from est.core.types import Spectrum

try:
    import larch
except ImportError:
    has_larch = False
else:
    has_larch = True
    from est.core.process.larch.xftf import larch_xftf, process_spectr_xftf as xftf
    from est.core.process.larch.autobk import process_spectr_autobk as autobk
    from est.core.process.larch.pre_edge import process_spectr_pre_edge as pre_edge
    from est.io.utils.larch import read_ascii


@unittest.skipIf(has_larch is False, "xraylarch not installed")
class TestLarchWorkflows(unittest.TestCase):
    """Test several larch workflow"""

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

    def tearDown(self):
        shutil.rmtree(self.outputdir)

    def testAutobk(self):
        """equivalent treatment as the 'xafs.autobk.par script from larch'"""
        pre_edge(
            spectrum=self.spectrum,
            overwrite=True,
            configuration={"rbkg": 1.0, "kweight": 2},
        )
        autobk(
            spectrum=self.spectrum,
            overwrite=True,
            configuration={
                "kmin": 2,
                "kmax": 16,
                "dk": 3,
                "window": "hanning",
                "kweight": 2,
            },
        )
        xftf(spectrum=self.spectrum, overwrite=True, configuration={"kweight": 2})

    def testXafsft1(self):
        """equivalent treatment as the 'xafs.doc_xafs1.par script from larch'"""
        autobk(
            spectrum=self.spectrum,
            overwrite=True,
            configuration={"rbkg": 1.0, "kweight": 2, "clamp+hi": 10},
        )
        conf, spec_dk1 = xftf(
            spectrum=self.spectrum,
            overwrite=False,
            configuration={
                "kweight": 2,
                "kmin": 3,
                "kmax": 13,
                "window": "hanning",
                "dk": 1,
            },
        )
        conf, spec_dk2 = xftf(
            spectrum=self.spectrum,
            overwrite=False,
            configuration={
                "kweight": 2,
                "kmin": 3,
                "kmax": 13,
                "window": "hanning",
                "dk": 5,
            },
        )
        self.assertNotEqual(spec_dk1, spec_dk2)
        self.assertFalse(numpy.array_equal(spec_dk1.chir_re, spec_dk2.chir_re))


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestLarchWorkflows,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
