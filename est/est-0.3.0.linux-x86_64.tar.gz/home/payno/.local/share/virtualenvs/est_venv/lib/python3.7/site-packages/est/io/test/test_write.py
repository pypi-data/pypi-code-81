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


import unittest
import urllib
import tempfile
import os
import shutil
from est.core.types import Spectrum, XASObject
from silx.io.utils import h5py_read_dataset
import h5py

try:
    from est.io.utils.larch import read_ascii
    from est.core.process.larch.pre_edge import Larch_pre_edge
except ImportError:
    has_larch = False
else:
    has_larch = True


@unittest.skipIf(has_larch is False, "xraylarch not installed")
class TestWriteProcess(unittest.TestCase):
    """
    Insure saving processes works
    """

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
        self.xas_obj = XASObject(spectra=(self.spectrum,), energy=self.spectrum.energy)
        self.output_file = os.path.join(self.outputdir, "output.h5")

    def tearDown(self):
        shutil.rmtree(self.outputdir)

    def testProcess(self):
        self.assertTrue(self.spectrum.pre_edge is None)
        self.assertTrue(self.spectrum.e0 is None)
        process = Larch_pre_edge()
        process.process(self.xas_obj)
        self.assertTrue(self.spectrum.pre_edge is not None)
        self.assertTrue(self.spectrum.e0 is not None)
        # check process
        self.xas_obj.dump(self.output_file)
        self.assertTrue(os.path.exists(self.output_file))
        with h5py.File(self.output_file, "r") as h5f:
            scan = h5f["scan1"]
            pre_edge_process = scan["xas_process_1"]
            # check general informqtion
            self.assertTrue("class_instance" in pre_edge_process)
            self.assertTrue("date" in pre_edge_process)
            self.assertTrue("processing_order" in pre_edge_process)
            self.assertTrue("program" in pre_edge_process)
            self.assertTrue("version" in pre_edge_process)
            self.assertEqual(
                h5py_read_dataset(pre_edge_process["program"]), "larch_pre_edge"
            )
            # check results
            self.assertTrue("results" in pre_edge_process)
            results_grp = pre_edge_process["results"]
            self.assertTrue("Mu" in results_grp)
            mu_grp = results_grp["Mu"]
            self.assertTrue("units" in mu_grp.attrs)
            self.assertTrue("units_latex" in mu_grp.attrs)

            # check plots
            self.assertTrue("plots" in pre_edge_process)
            plot_0_grp = pre_edge_process["plots"]["plot_0"]
            self.assertTrue("Mu" in plot_0_grp)
            self.assertTrue("energy" in plot_0_grp)
            self.assertTrue("units" in plot_0_grp["Mu"].attrs)
            self.assertTrue("units_latex" in plot_0_grp["Mu"].attrs)
            self.assertTrue("title" in plot_0_grp.attrs)
            self.assertTrue("title_latex" in plot_0_grp.attrs)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestWriteProcess,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
