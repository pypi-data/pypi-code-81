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
import numpy
from silx.io.url import DataUrl
from est.core.io import read as read_xas
from est.core.process.roi import xas_roi
from est.core.utils import spectra as spectra_utils
from est.core.types import Dim


class TestRoi(unittest.TestCase):
    def setUp(self):
        self.energy, self.spectra = spectra_utils.create_dataset(shape=(16, 100, 30))
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

    def testApplyRoi(self):
        """Test output of the roi process"""
        original_spectra = self.xas_obj.spectra.map_to(data_info="mu").copy()
        self.assertEqual(original_spectra.shape, (16, 100, 30))
        roi_dict = {"origin": (20, 50), "size": (10, 20)}
        self.xas_obj.configuration = {"roi": roi_dict}
        res_xas_obj = xas_roi(self.xas_obj)
        self.assertEqual(res_xas_obj.n_spectrum, 20 * 10)
        reduces_spectra = res_xas_obj.spectra.map_to(data_info="mu").copy()
        assert reduces_spectra.shape == (16, 20, 10)
        numpy.testing.assert_array_equal(
            original_spectra[:, 50:70, 20:30], reduces_spectra
        )

    def testWorkflowWithRoi(self):
        """"""
        pass


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestRoi,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
