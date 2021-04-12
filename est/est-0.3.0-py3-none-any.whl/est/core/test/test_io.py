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
from est.core.types import Dim
from est.core.io import XASReader
from silx.io.url import DataUrl
from est.core.types import XASObject
from est.io.utils.information import InputInformation
from est.units import ur
import numpy
import os
import tempfile
import h5py
import shutil


class TestSpectraDimensions(unittest.TestCase):
    """
    Test reading spectra with different dimensions organisation
    (X, Y, Channels), (Channels, Y, X), (Y, Channels, X)
    """

    def setUp(self) -> None:
        self.spectra_path = "/data/NXdata/data"
        self.channel_path = "/data/NXdata/Channel"
        self.output_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.output_dir, "myfile.h5")

    def tearDown(self) -> None:
        shutil.rmtree(self.output_dir)

    def saveSpectra(self, spectra):
        """Save the spectra to the spectra file defined in setup and return the
        associated silx url"""
        with h5py.File(self.filename, "a") as f:
            f[self.spectra_path] = spectra

        return DataUrl(
            file_path=self.filename, data_path=self.spectra_path, scheme="silx"
        )

    def saveChannel(self, channel):
        """Save the energy to the spectra file defined in setup and return the
        associated silx url"""
        with h5py.File(self.filename, "a") as f:
            f[self.channel_path] = channel

        return DataUrl(
            file_path=self.filename, data_path=self.channel_path, scheme="silx"
        )

    def testDimensionsXYEnergy(self):
        """Test that spectra stored as X, Y Energy can be read"""
        x_dim = 4
        y_dim = 2
        energy_dim = 3
        shape = (x_dim, y_dim, energy_dim)
        spectra = numpy.arange(x_dim * y_dim * energy_dim).reshape(shape)
        channel = numpy.linspace(0, 1, energy_dim)
        spectra_url = self.saveSpectra(spectra)
        channel_url = self.saveChannel(channel=channel)

        # if dims are incoherent with energy, should raise an error
        dims = (Dim.DIM_2, Dim.DIM_1, Dim.DIM_0)
        with self.assertRaises(ValueError):
            XASReader().read_frm_url(
                InputInformation(
                    spectra_url=spectra_url,
                    channel_url=channel_url,
                    dimensions=dims,
                )
            )
        dims = (Dim.DIM_0, Dim.DIM_1, Dim.DIM_2)
        xas_obj = XASReader().read_frm_url(
            InputInformation(
                spectra_url=spectra_url,
                channel_url=channel_url,
                dimensions=dims,
            )
        )
        self.assertTrue(isinstance(xas_obj, XASObject))
        self.assertTrue(xas_obj.n_spectrum == x_dim * y_dim)
        numpy.testing.assert_array_equal(
            xas_obj.spectra.data.flat[1].mu, spectra[1, 0, :]
        )
        numpy.testing.assert_array_equal(xas_obj.spectra.data.flat[2].energy, channel)

    def testDimensionsChannelYX(self):
        """Test that spectra stored as Channel, Y, X can be read"""
        x_dim = 10
        y_dim = 5
        energy_dim = 30
        shape = (energy_dim, y_dim, x_dim)
        spectra = numpy.arange(x_dim * y_dim * energy_dim).reshape(shape)
        channel = numpy.linspace(0, 100, energy_dim)
        spectra_url = self.saveSpectra(spectra)
        channel_url = self.saveChannel(channel=channel)

        # if dims are incoherent with energy, should raise an error
        dims = (Dim.DIM_0, Dim.DIM_1, Dim.DIM_2)
        with self.assertRaises(ValueError):
            XASReader().read_frm_url(
                InputInformation(
                    spectra_url=spectra_url,
                    channel_url=channel_url,
                    dimensions=dims,
                )
            )

        dims = (Dim.DIM_2, Dim.DIM_1, Dim.DIM_0)
        xas_obj = XASReader().read_frm_url(
            InputInformation(
                spectra_url=spectra_url, channel_url=channel_url, dimensions=dims
            )
        )
        self.assertTrue(isinstance(xas_obj, XASObject))
        self.assertTrue(xas_obj.n_spectrum == x_dim * y_dim)
        numpy.testing.assert_array_equal(
            xas_obj.spectra.data.flat[1].mu, spectra[:, 0, 1]
        )
        numpy.testing.assert_array_equal(
            xas_obj.spectra.data.flat[2].energy, (channel * ur.eV).m
        )


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestSpectraDimensions,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
