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

import shutil
import tempfile
import h5py
import numpy
import os
import unittest
from est.core.io import XASWriter
from est.core.io import read as read_xas
from est.core.utils import spectra as spectra_utils
from est.core.types import XASObject
from silx.io.url import DataUrl
from est.core.types import Dim

try:
    import PyMca5
except ImportError:
    has_pymca = False
else:
    has_pymca = True
    from PyMca5.PyMcaDataDir import PYMCA_DATA_DIR


class TestReadWrite(unittest.TestCase):
    """Test read function for spectra and configuration"""

    def setUp(self):
        self.outputdir = tempfile.mkdtemp()
        self.outputfile = os.path.join(self.outputdir, "output_file.h5")

    def tearDown(self):
        shutil.rmtree(self.outputdir)

    @unittest.skipIf(has_pymca is False, "PyMca5 is not installed")
    def testReadSpectrum(self):
        data_file = os.path.join(PYMCA_DATA_DIR, "EXAFS_Cu.dat")
        res = read_xas(
            spectra_url=DataUrl(
                file_path=data_file, scheme="PyMca", data_path="Column 1"
            ),
            channel_url=DataUrl(
                file_path=data_file, scheme="PyMca", data_path="Column 2"
            ),
        )
        self.assertTrue(isinstance(res, XASObject))
        self.assertEqual(res.n_spectrum, 1)
        self.assertTrue("Mu" in res.spectra.data.flat[0])
        self.assertTrue("Energy" in res.spectra.data.flat[0])


class TestNxWriting(unittest.TestCase):
    """Test that the nx process is correctly store ad the output data"""

    def setUp(self):
        self.output_dir = tempfile.mkdtemp()
        energy, spectra = spectra_utils.create_dataset(shape=(256, 20, 10))
        self.xas_obj = XASObject(spectra=spectra, energy=energy, dim1=20, dim2=10)
        self.h5_file = os.path.join(self.output_dir, "output_file.h5")

    def tearDown(self):
        shutil.rmtree(self.output_dir)

    def testWriteRead(self):
        writer = XASWriter()
        writer.output_file = self.h5_file
        writer(self.xas_obj)
        with h5py.File(self.h5_file, "r") as hdf:
            self.assertTrue("scan1" in hdf.keys())
            self.assertTrue("data" in hdf["scan1"].keys())
            self.assertTrue("absorbed_beam" in hdf["scan1"].keys())
            self.assertTrue("monochromator" in hdf["scan1"].keys())

        loaded_xas_obj = XASObject.from_file(self.h5_file, configuration_path=None)
        numpy.testing.assert_allclose(loaded_xas_obj.energy, self.xas_obj.energy)
        numpy.testing.assert_allclose(
            loaded_xas_obj.absorbed_beam(), self.xas_obj.absorbed_beam()
        )


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestReadWrite, TestNxWriting):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
