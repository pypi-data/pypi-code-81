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
"""
unit test for workflow composed of pymca process 
"""
__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "06/11/2019"


import os
import shutil
import tempfile
import unittest
import h5py
import numpy
from silx.io.utils import h5py_read_dataset
from silx.io.dictdump import h5todict
from silx.io.url import DataUrl
from est.core.process.roi import xas_roi, _ROI as XASROI
from est.core.io import XASWriter
from est.core.io import read as read_xas
from est.core.types import XASObject
from est.core.utils import spectra as spectra_utils
from est.core.types import Dim

try:
    import PyMca5
except ImportError:
    has_pymca = False
else:
    has_pymca = True
    from PyMca5.PyMcaDataDir import PYMCA_DATA_DIR
    from est.core.process.pymca.exafs import pymca_exafs, PyMca_exafs
    from est.core.process.pymca.ft import pymca_ft, PyMca_ft
    from est.core.process.pymca.k_weight import pymca_k_weight, PyMca_k_weight
    from est.core.process.pymca.normalization import pymca_normalization
    from est.core.process.pymca.normalization import PyMca_normalization


@unittest.skipIf(has_pymca is False, "PyMca5 is not installed")
class TestStreamSingleSpectrum(unittest.TestCase):
    """Make sure the process have valid io"""

    def setUp(self):
        self.exafs_configuration = {
            "Knots": {"Values": (1, 2, 5), "Number": 3, "Orders": [3, 3, 3]},
            "KMin": 0,
            "KMax": 2.3,
        }

    def test_pymca_process(self):
        data_file = os.path.join(PYMCA_DATA_DIR, "EXAFS_Cu.dat")
        out = read_xas(
            spectra_url=DataUrl(
                file_path=data_file, scheme="PyMca", data_path="Column 2"
            ),
            channel_url=DataUrl(
                file_path=data_file, scheme="PyMca", data_path="Column 1"
            ),
        )
        out.configuration = {"EXAFS": self.exafs_configuration, "SET_KWEIGHT": 0}
        out = pymca_normalization(xas_obj=out)
        out = pymca_exafs(xas_obj=out)
        out = pymca_k_weight(xas_obj=out)
        out = pymca_ft(xas_obj=out)
        assert isinstance(out, XASObject)

    def test_pymca_process_with_dict(self):
        data_file = os.path.join(PYMCA_DATA_DIR, "EXAFS_Cu.dat")
        out = read_xas(
            spectra_url=DataUrl(
                file_path=data_file, scheme="PyMca", data_path="Column 2"
            ),
            channel_url=DataUrl(
                file_path=data_file, scheme="PyMca", data_path="Column 1"
            ),
        )
        out.configuration = {"EXAFS": self.exafs_configuration, "SET_KWEIGHT": 0}
        out = pymca_normalization(xas_obj=out.to_dict())
        out = pymca_exafs(xas_obj=out.to_dict())
        out = pymca_k_weight(xas_obj=out.to_dict())
        out = pymca_ft(xas_obj=out.to_dict())
        assert isinstance(out, XASObject)

    def test_pymca_process_with_cls(self):
        data_file = os.path.join(PYMCA_DATA_DIR, "EXAFS_Cu.dat")
        out = read_xas(
            spectra_url=DataUrl(
                file_path=data_file, scheme="PyMca", data_path="Column 2"
            ),
            channel_url=DataUrl(
                file_path=data_file, scheme="PyMca", data_path="Column 1"
            ),
        )
        out = PyMca_normalization()(xas_obj=out)
        exafs_process = PyMca_exafs()
        exafs_process.setConfiguration(configuration=self.exafs_configuration)
        out = exafs_process(xas_obj=out)
        kweight_process = PyMca_k_weight()
        kweight_process.setConfiguration({"k_weight": 0})
        out = kweight_process(xas_obj=out)
        out = PyMca_ft()(xas_obj=out)
        assert isinstance(out, XASObject)
        self.assertTrue(out.spectra.data.flat[0].ft is not None)
        self.assertTrue(len(out.spectra.data.flat[0].ft.intensity) > 0)

    def test_pymca_with_roi(self):
        energy, spectra = spectra_utils.create_dataset(shape=(256, 20, 10))
        roi = XASROI(origin=(0, 2), size=(5, 1))
        xas_obj = XASObject(
            spectra=spectra, energy=energy, configuration={"roi": roi.to_dict()}
        )
        dict_xas_obj = xas_obj.to_dict()
        self.assertTrue("spectra" in dict_xas_obj.keys())
        self.assertTrue("energy" in dict_xas_obj.keys())
        tmp_obj = XASObject.from_dict(dict_xas_obj)
        numpy.testing.assert_array_equal(
            tmp_obj.energy, tmp_obj.spectra.data.flat[0].energy
        )
        out = xas_roi(dict_xas_obj)
        out.configuration = {"EXAFS": self.exafs_configuration, "SET_KWEIGHT": 0}
        out = pymca_normalization(xas_obj=out)
        out = pymca_exafs(xas_obj=out)
        out = pymca_k_weight(xas_obj=out)
        out = pymca_ft(xas_obj=out)
        assert isinstance(out, XASObject)
        self.assertEqual(out.spectra.shape[0], 1)
        self.assertEqual(out.spectra.shape[1], 5)
        self.assertTrue(out.spectra.data.flat[0].ft is not None)
        self.assertTrue(len(out.spectra.data.flat[0].ft.intensity) > 0)


@unittest.skipIf(has_pymca is False, "PyMca5 is not installed")
class TestWorkflowAndH5LinkedFile(unittest.TestCase):
    """
    Test that the workflow can process and store process in a targeted h5 file
    """

    def setUp(self):
        self.output_dir = tempfile.mkdtemp()
        energy, spectra = spectra_utils.create_dataset(shape=(256, 20, 10))
        roi = XASROI(origin=(0, 2), size=(5, 1))
        self.xas_obj = XASObject(
            spectra=spectra, energy=energy, configuration={"roi": roi.to_dict()}
        )
        self.h5_file = os.path.join(self.output_dir, "output_file.h5")
        self.xas_obj.link_to_h5(self.h5_file)

    def tearDown(self):
        shutil.rmtree(self.output_dir)

    def test_h5_link_xas_object(self):
        """Test that the processing can be stored continuously on a .h5 file"""
        self.assertTrue(self.xas_obj.linked_h5_file is not None)
        out = PyMca_normalization()(xas_obj=self.xas_obj)
        exafs_process = PyMca_exafs()
        configuration = {
            "Knots": {"Values": (1, 2, 5), "Number": 3, "Orders": [3, 3, 3]},
            "KMin": 0,
            "KMax": 2.3,
        }
        exafs_process.setConfiguration(configuration=configuration)
        out = exafs_process(xas_obj=out)
        k_weight_process = PyMca_k_weight()
        k_weight_process.setConfiguration({"k_weight": 0})
        out = k_weight_process(xas_obj=out)
        out = PyMca_ft()(xas_obj=out)
        out = PyMca_normalization()(xas_obj=out)
        assert isinstance(out, XASObject)
        assert out.linked_h5_file is self.h5_file
        # then check all process are correctly registered with the valid id...
        processes = self.xas_obj.get_process_flow()
        self.assertEqual(len(processes), 5)
        self.assertEqual(
            h5py_read_dataset(processes[1]["program"]), "pymca_normalization"
        )
        self.assertEqual(h5py_read_dataset(processes[2]["program"]), "pymca_exafs")
        self.assertEqual(
            h5py_read_dataset(processes[5]["program"]), "pymca_normalization"
        )
        self.xas_obj.clean_process_flow()
        processes = self.xas_obj.get_process_flow()
        self.assertEqual(len(processes), 0)

    def test_h5_link_dict(self):
        """Same test as test_h5_link_xas_object but with a dict pass between
        processes"""
        self.assertTrue(self.xas_obj.linked_h5_file is not None)
        out = PyMca_normalization()(xas_obj=self.xas_obj.to_dict())
        exafs_process = PyMca_exafs()
        configuration = {
            "Knots": {"Values": (1, 2, 5), "Number": 3, "Orders": [3, 3, 3]},
            "KMin": 0,
            "KMax": 2.3,
        }
        exafs_process.setConfiguration(configuration=configuration)
        out = exafs_process(xas_obj=out.to_dict())
        k_weight_process = PyMca_k_weight()
        k_weight_process.setConfiguration({"k_weight": 0})
        out = k_weight_process(xas_obj=out.to_dict())
        out = PyMca_ft()(xas_obj=out.to_dict())
        out = PyMca_normalization()(xas_obj=out.to_dict())
        assert isinstance(out, XASObject)
        assert out.linked_h5_file
        assert out.linked_h5_file == self.h5_file
        # then check all process are correctly registered with the valid id...
        processes = self.xas_obj.get_process_flow()
        self.assertEqual(len(processes), 5)
        self.assertEqual(
            h5py_read_dataset(processes[1]["program"]), "pymca_normalization"
        )
        self.assertEqual(h5py_read_dataset(processes[2]["program"]), "pymca_exafs")
        self.assertEqual(
            h5py_read_dataset(processes[5]["program"]), "pymca_normalization"
        )
        self.xas_obj.clean_process_flow()
        processes = self.xas_obj.get_process_flow()
        self.assertEqual(len(processes), 0)


@unittest.skipIf(has_pymca is False, "PyMca5 is not installed")
class TestSaveFlowAuto(unittest.TestCase):
    """Test that the processing can be stored continuously on a temporary
    .h5 file then dump without lost during call to 'dump_xas' of the XASObject
    """

    def setUp(self):
        self.output_dir = tempfile.mkdtemp()
        energy, spectra = spectra_utils.create_dataset(shape=(100, 10, 10))
        assert spectra.shape == (100, 10, 10)
        assert len(energy) == spectra.shape[0]
        self.xas_obj = XASObject(spectra=spectra, energy=energy, dim1=10, dim2=10)

        self.h5_file = os.path.join(self.output_dir, "output_file.h5")

    def tearDown(self):
        shutil.rmtree(self.output_dir)

    def test(self):
        self.assertTrue(self.xas_obj.linked_h5_file is not None)
        out = PyMca_normalization()(xas_obj=self.xas_obj)
        exafs = PyMca_exafs()
        configuration = {
            "Knots": {"Values": (1, 2, 5), "Number": 3, "Orders": [3, 3, 3]},
            "KMin": 0,
            "KMax": 2.3,
        }
        exafs.setConfiguration(configuration)
        out = exafs(xas_obj=out)
        kweight_process = PyMca_k_weight()
        kweight_process.setConfiguration({"k_weight": 0})
        out = kweight_process(xas_obj=out)
        out = PyMca_ft()(xas_obj=out)
        out = PyMca_normalization()(xas_obj=out)

        writer = XASWriter()
        writer.output_file = self.h5_file
        writer(out)

        with h5py.File(self.h5_file, "r") as hdf:
            self.assertTrue("scan1" in hdf.keys())
            self.assertTrue("data" in hdf["scan1"].keys())
            self.assertTrue("absorbed_beam" in hdf["scan1"].keys())
            self.assertTrue("monochromator" in hdf["scan1"].keys())
            self.assertTrue("xas_process_1" in hdf["scan1"].keys())
            self.assertTrue("xas_process_2" in hdf["scan1"].keys())
            self.assertTrue("xas_process_3" in hdf["scan1"].keys())
            self.assertTrue("xas_process_4" in hdf["scan1"].keys())
            self.assertTrue("xas_process_5" in hdf["scan1"].keys())
            targetted_xas_process = hdf["scan1"]["xas_process_2"]
            self.assertTrue("program" in targetted_xas_process)
            self.assertEqual(
                h5py_read_dataset(targetted_xas_process["program"]), "pymca_exafs"
            )
            self.assertTrue("configuration" in targetted_xas_process)

        # check one configuration
        stored_config = h5todict(
            self.h5_file, path="/scan1/xas_process_2/configuration", asarray=False
        )
        for key in ("KMin", "KMax"):
            self.assertTrue(configuration[key] == stored_config[key])


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestStreamSingleSpectrum, TestWorkflowAndH5LinkedFile, TestSaveFlowAuto):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
