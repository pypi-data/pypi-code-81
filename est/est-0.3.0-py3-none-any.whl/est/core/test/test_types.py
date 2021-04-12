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


import numpy
import os
import unittest
import tempfile
import h5py
import shutil
from est.core.types import Spectrum, XASObject, Dim
from est.core.utils import spectra as spectra_utils
from est.core.io import read as read_xas
from silx.io.url import DataUrl
from est.units import ur
import json
import pint
import silx.io.utils
from est.core.types import Dim

try:
    import PyMca5
except ImportError:
    has_pymca = False
else:
    has_pymca = True
    from PyMca5.PyMcaDataDir import PYMCA_DATA_DIR
    from est.io.utils.spec import read_spectrum


class TestSpectrum(unittest.TestCase):
    """Test the spectrum class"""

    @unittest.skipIf(has_pymca is False, "PyMca5 is not installed")
    def test_from_dat(self):
        """check that we can create a Spectrum from a pymca .dat file"""
        data_file = os.path.join(PYMCA_DATA_DIR, "EXAFS_Cu.dat")
        energy, mu = read_spectrum(
            data_file,
            energy_col_name="Column 1",
            absorption_col_name="Column 2",
        )
        spectrum = Spectrum(energy=energy, mu=mu)
        self.assertTrue(spectrum.energy is not None)
        self.assertTrue(spectrum.mu is not None)

    def test_from_numpy_array(self):
        """check that we can create a Spectrum from numpy arrays"""
        energy = numpy.arange(10, 20)
        mu = numpy.arange(10)
        spectrum = Spectrum(energy=energy, mu=mu)
        numpy.testing.assert_array_equal(spectrum.energy, (energy * ur.eV).m)
        numpy.testing.assert_array_equal(spectrum.mu, mu)
        mu_2 = numpy.arange(30, 40)
        spectrum["Mu"] = mu_2
        numpy.testing.assert_array_equal(spectrum.mu, mu_2)


class TestXASObject(unittest.TestCase):
    """test construction of XAS object from a single spectra"""

    @unittest.skipIf(has_pymca is False, "PyMca5 is not installed")
    def test_create_from_single_spectrum(self):
        """check that we can create a XASObject from a pymca .dat file"""
        data_file = os.path.join(PYMCA_DATA_DIR, "EXAFS_Cu.dat")
        spectrum = {}
        spectrum["Energy"], spectrum["Mu"] = read_spectrum(
            data_file,
            energy_col_name="Column 1",
            absorption_col_name="Column 2",
        )
        self.spectrum = Spectrum(energy=spectrum["Energy"], mu=spectrum["Mu"])
        self.configuration = {
            "FT": {"KWeight": 1},
            "EXAFS": {"EXAFSNormalized": numpy.array([1, 2, 3])},
        }
        obj = XASObject(
            spectra=(self.spectrum,),
            energy=self.spectrum.energy,
            configuration=self.configuration,
            dim1=1,
            dim2=1,
        )
        self.assertEqual(obj.n_spectrum, 1)
        ddict = obj.to_dict()
        obj2 = XASObject.from_dict(ddict)
        self.assertEqual(obj2, obj)
        # insure the XASObject is serializable
        # import json
        # json.dumps(obj2.to_dict())

    def test_create_from_several_spectrums(self):
        """check that we can create a XASObject from numpy arrays"""
        self.energy, self.spectra = spectra_utils.create_dataset(shape=(256, 20, 10))
        self.output_dir = tempfile.mkdtemp()
        spectra_path = "/data/NXdata/data"
        channel_path = "/data/NXdata/Channel"
        filename = os.path.join(self.output_dir, "myfile.h5")
        with h5py.File(filename, "a") as f:
            f[spectra_path] = self.spectra
            f[channel_path] = self.energy

        url_spectra = DataUrl(file_path=filename, data_path=spectra_path, scheme="silx")
        self.xas_obj = read_xas(
            spectra_url=url_spectra,
            channel_url=DataUrl(
                file_path=filename, data_path=channel_path, scheme="silx"
            ),
            dimensions=(Dim.DIM_2, Dim.DIM_1, Dim.DIM_0),
        )
        self.assertEqual(self.xas_obj.spectra.shape[0], 20)
        self.assertEqual(self.xas_obj.spectra.shape[1], 10)
        self.assertEqual(self.xas_obj.n_spectrum, 20 * 10)
        ddict = self.xas_obj.to_dict(with_process_details=False)
        original_spectra = silx.io.utils.get_data(
            DataUrl(file_path=filename, data_path=spectra_path, scheme="silx")
        )
        obj2 = XASObject.from_dict(ddict)
        self.assertEqual(self.xas_obj.n_spectrum, obj2.n_spectrum)
        obj2_mu_spectra = obj2.spectra.map_to(data_info="mu")

        numpy.testing.assert_array_equal(original_spectra, obj2_mu_spectra)
        self.assertEqual(obj2, self.xas_obj)


class TestXASObjectSerialization(unittest.TestCase):
    def setUp(self) -> None:
        self.energy, self.spectra = spectra_utils.create_dataset(shape=(256, 20, 10))
        self.output_dir = tempfile.mkdtemp()
        self.spectra_path = "/data/NXdata/data"
        self.channel_path = "/data/NXdata/Channel"
        self.filename = os.path.join(self.output_dir, "myfile.h5")
        with h5py.File(self.filename, "a") as f:
            f[self.spectra_path] = self.spectra
            f[self.channel_path] = self.energy

        self.dimensions = (Dim.DIM_2, Dim.DIM_1, Dim.DIM_0)

        self.url_spectra = DataUrl(
            file_path=self.filename, data_path=self.spectra_path, scheme="silx"
        )
        self.url_energy = DataUrl(
            file_path=self.filename, data_path=self.channel_path, scheme="silx"
        )
        self.process_flow_file = os.path.join(self.output_dir, "process_flow.h5")

    def tearDown(self) -> None:
        shutil.rmtree(self.output_dir)

    def test_serialization_url_auto(self):
        """Make sure the `to_dict` and `from_dict` functions are working
        if no url are provided"""
        xas_obj = XASObject(
            spectra=self.spectra,
            energy=self.energy,
            dim1=20,
            dim2=10,
            keep_process_flow=False,
        )
        # if no h5 file defined, should fail to copy it to a dictionary
        with self.assertRaises(ValueError):
            xas_obj.to_dict()

        xas_obj.link_to_h5(self.process_flow_file)
        dict_xas_obj = xas_obj.to_dict()

        # make sure it is serializable
        json.dumps(dict_xas_obj)
        # make sure we find a comparable xas object from it
        xas_obj_2 = XASObject.from_dict(dict_xas_obj)

        numpy.testing.assert_array_equal(xas_obj.energy, xas_obj_2.energy)
        self.assertEqual(xas_obj, xas_obj_2)

        # simple test without the process_details
        dict_xas_obj = xas_obj.to_dict(with_process_details=False)
        # make sure it is serializable
        json.dumps(dict_xas_obj)

    def test_serialization_url_provided(self):
        """Make sure the `to_dict` and `from_dict` functions are working
        if url are provided"""
        xas_obj = XASObject(
            spectra=self.spectra,
            energy=self.energy,
            dim1=20,
            dim2=10,
            keep_process_flow=False,
            energy_url=self.url_energy,
            spectra_url=self.spectra_path,
        )
        self.assertTrue(isinstance(xas_obj.energy, numpy.ndarray))
        # if no h5 file defined, should fail to copy it to a dictionary
        with self.assertRaises(ValueError):
            xas_obj.to_dict()

        xas_obj.link_to_h5(self.process_flow_file)
        dict_xas_obj = xas_obj.to_dict()

        # make sure it is serializable
        json.dumps(dict_xas_obj)
        # make sure we find a comparable xas object from it
        xas_obj_2 = XASObject.from_dict(dict_xas_obj)
        self.assertTrue(isinstance(xas_obj_2.energy, numpy.ndarray))

        numpy.testing.assert_array_equal(xas_obj.energy, xas_obj_2.energy)
        self.assertEqual(xas_obj, xas_obj_2)

        # simple test without the process_details
        dict_xas_obj = xas_obj.to_dict(with_process_details=False)
        # make sure it is serializable
        json.dumps(dict_xas_obj)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestSpectrum, TestXASObject, TestXASObjectSerialization):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
