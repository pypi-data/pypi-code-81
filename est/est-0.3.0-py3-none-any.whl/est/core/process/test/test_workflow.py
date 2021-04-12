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
__date__ = "07/08/2019"

import unittest
import os
import tempfile
import shutil
from est.core.types import Spectrum, XASObject
from est.core.io import XASWriter
from est.core.types import Dim

try:
    import larch
except ImportError:
    has_larch = False
else:
    has_larch = True
    from est.core.process.larch.autobk import Larch_autobk
    from est.core.process.larch.pre_edge import Larch_pre_edge
    from est.core.process.larch.xftf import Larch_xftf
try:
    import PyMca5
except ImportError:
    has_pymca = False
else:
    has_pymca = True
    from PyMca5.PyMcaDataDir import PYMCA_DATA_DIR
    from est.io.utils.spec import read_spectrum
    from est.core.process.pymca.normalization import PyMca_normalization
    from est.core.process.pymca.exafs import PyMca_exafs
    from est.core.process.pymca.ft import PyMca_ft
    from est.core.process.pymca.k_weight import PyMca_k_weight


@unittest.skipIf(not has_pymca or not has_larch, "pymca and/or larch not installed")
class TestMeldWorkflow(unittest.TestCase):
    """
    Test the following workflow: read_xmu -> pymca normalize ->
    """

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
        assert self.xas_obj.linked_h5_file is not None
        self.output_dir = tempfile.mkdtemp()
        self.h5_file = os.path.join(self.output_dir, "output_file.h5")
        self.configuration_exafs = {
            "Knots": {"Values": (1, 2, 5), "Number": 3, "Orders": [3, 3, 3]},
            "KMin": 0,
            "KMax": 2.3,
        }

    def tearDown(self):
        shutil.rmtree(self.output_dir)

    def test_workflow_normalize_autobk_kweight_ft(self):
        """Test the following workflow:
        pymca normalize -> larch autobk -> kweight -> pymca ft
        """
        self.xas_obj.configuration = {"EXAFS": self.configuration_exafs}
        # pymca normalization
        out = PyMca_normalization()(xas_obj=self.xas_obj)
        # larch autobk
        out = Larch_autobk()(xas_obj=out)
        # k weight
        kweight_process = PyMca_k_weight()
        kweight_process.setConfiguration({"k_weight": 0})
        out = kweight_process(xas_obj=out)
        # pymca ft
        out = PyMca_ft()(xas_obj=out)

        self.assertTrue(out.spectra.data.flat[0].ft.intensity is not None)
        self.assertTrue(len(out.spectra.data.flat[0].ft.intensity) > 1)

    def test_workflow_preedge_exafs_xftf(self):
        """Test the following workflow:
        larch pre_edge -> pymca exafs -> larch xftf
        """
        # larch pre edge
        out = Larch_pre_edge()(self.xas_obj)
        # pymca exafs
        exafs = PyMca_exafs()

        exafs.setConfiguration(self.configuration_exafs)
        out = exafs(xas_obj=out)
        # for now we cannot link xftf because chi is not set by pymca exafs
        spectrum_0 = out.spectra.data.flat[0]
        self.assertFalse(spectrum_0["EXAFSSignal"] is None)
        self.assertFalse(spectrum_0["EXAFSKValues"] is None)
        self.assertFalse(spectrum_0.chi is None)
        self.assertFalse(spectrum_0.k is None)
        # larch xftf
        out = Larch_xftf()(xas_obj=out)

        writer = XASWriter()
        writer.output_file = self.h5_file
        writer(out)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestMeldWorkflow,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite
