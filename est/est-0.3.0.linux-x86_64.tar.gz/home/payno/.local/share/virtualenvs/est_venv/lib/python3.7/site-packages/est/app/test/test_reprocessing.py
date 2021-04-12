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


import os
import shutil
import tempfile
import unittest
import numpy
from est.core.io import XASWriter
from est.core.types import XASObject
import urllib.request
from est.core.types import Spectrum
from ..reprocessing import exec_
from est.core.types import Dim

try:
    import PyMca5
except ImportError:
    has_pymca = False
else:
    has_pymca = True
    from est.core.process.pymca.exafs import PyMca_exafs
    from est.core.process.pymca.ft import PyMca_ft
    from est.core.process.pymca.k_weight import PyMca_k_weight
    from est.core.process.pymca.normalization import PyMca_normalization
    from est.io.utils.spec import read_spectrum
    from PyMca5.PyMcaDataDir import PYMCA_DATA_DIR
try:
    import larch
except ImportError:
    has_larch = False
else:
    has_larch = True
    from est.core.process.larch.pre_edge import Larch_pre_edge
    from est.core.process.larch.xftf import Larch_xftf
    from est.core.process.larch.autobk import Larch_autobk
    from est.io.utils.larch import read_ascii


@unittest.skipIf(has_pymca is False, "PyMca5 is not installed")
class TestReprocessingPyMca(unittest.TestCase):
    """test reprocessing work for some pymca process"""

    def setUp(self):
        self.output_dir = tempfile.mkdtemp()
        data_file = os.path.join(PYMCA_DATA_DIR, "EXAFS_Cu.dat")
        energy, mu = read_spectrum(
            data_file,
            energy_col_name="Column 1",
            absorption_col_name="Column 2",
        )
        self.spectrum = Spectrum(energy=energy, mu=mu)
        self.xas_obj_ref = XASObject(
            spectra=(self.spectrum,), energy=energy, dim1=1, dim2=1
        )
        self.h5_file = os.path.join(self.output_dir, "output_file.h5")
        out = PyMca_normalization()(xas_obj=self.xas_obj_ref)
        out = PyMca_exafs()(xas_obj=out)
        out = PyMca_k_weight()(xas_obj=out)
        out = PyMca_ft()(xas_obj=out)
        out = PyMca_normalization()(xas_obj=out)

        writer = XASWriter()
        writer.output_file = self.h5_file
        writer(out)
        self.assertTrue(out.spectra.data.flat[0].ft.intensity is not None)
        self.assertEqual(len(out.get_process_flow()), 5)

    def tearDown(self):
        shutil.rmtree(self.output_dir)

    def test(self):
        res_xas_obj = exec_(self.h5_file)
        self.assertEqual(res_xas_obj, self.xas_obj_ref)
        numpy.testing.assert_allclose(
            res_xas_obj.spectra.data.flat[0].ft.intensity,
            self.xas_obj_ref.spectra.data.flat[0].ft.intensity,
        )


@unittest.skipIf(has_larch is False, "Larch is not installed")
class TestReprocessingLarch(unittest.TestCase):
    """test reprocessing work for some larch process"""

    def setUp(self):
        self.output_dir = tempfile.mkdtemp()
        xmu_url = "https://raw.githubusercontent.com/xraypy/xraylarch/master/examples/xafs/cu_rt01.xmu"
        self.data_file = os.path.join(self.output_dir, "cu_rt01.xmu")

        with urllib.request.urlopen(xmu_url) as response, open(
            self.data_file, "wb"
        ) as out_file:
            data = response.read()  # a `bytes` object
            out_file.write(data)

        assert os.path.exists(self.data_file)
        energy, mu = read_ascii(self.data_file)
        self.spectrum = Spectrum(energy=energy, mu=mu)
        spectra = (self.spectrum,)
        self.xas_obj_ref = XASObject(spectra=spectra, energy=energy, dim1=1, dim2=1)
        self.h5_file = os.path.join(self.output_dir, "output_file.h5")

        pre_edge_process = Larch_pre_edge()
        pre_edge_process.set_properties({"rbkg": 1.0, "kweight": 2})
        autobk_process = Larch_autobk()
        autobk_process.set_properties(
            {"kmin": 2, "kmax": 16, "dk": 3, "window": "hanning", "kweight": 2}
        )
        xftf_process = Larch_xftf()
        xftf_process.set_properties({"kweight": 2})

        out = pre_edge_process(xas_obj=self.xas_obj_ref)
        out = autobk_process(xas_obj=out)
        out = xftf_process(xas_obj=out)

        writer = XASWriter()
        writer.output_file = self.h5_file
        writer(out)
        assert len(out.get_process_flow()) is 3

    def tearDown(self):
        shutil.rmtree(self.output_dir)

    def test(self):
        res_xas_obj = exec_(self.h5_file)
        self.assertEqual(res_xas_obj, self.xas_obj_ref)
        numpy.testing.assert_allclose(
            res_xas_obj.spectra.data.flat[0].chir_mag,
            self.xas_obj_ref.spectra.data.flat[0].chir_mag,
        )


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestReprocessingPyMca, TestReprocessingLarch):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
