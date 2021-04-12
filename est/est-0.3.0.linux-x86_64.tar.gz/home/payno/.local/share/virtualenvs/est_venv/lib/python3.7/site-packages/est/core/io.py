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
"""simple helper function to link io module and XASObject"""

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "07/16/2019"


from est.io import read_xas, write_xas, get_xasproc
from est.core.types import XASObject
from silx.io.url import DataUrl
from est.core.types import Dim
from est.units import ur, convert_to
from typing import Union
from est.io.utils.information import InputInformation
import h5py
import logging

_logger = logging.getLogger(__name__)

DEFAULT_SPECTRA_PATH = "/data/NXdata/data"

DEFAULT_CHANNEL_PATH = "/data/NXdata/Channel"

DEFAULT_CONF_PATH = "/configuration"


def read(
    spectra_url,
    channel_url,
    dimensions=(Dim.DIM_2, Dim.DIM_1, Dim.DIM_0),
    config_url=None,
    energy_unit=ur.eV,
):
    """

    :param DataUrl spectra_url: data url to the spectra
    :param DataUrl channel_url: data url to the channel / energy
    :param DataUrl config_url: data url to the process configuration
    :param dimensions: way the data has been stored.
                       Usually is (X, Y, channels) of (Channels, Y, X).
                       If None, by default is considered to be (Z, Y, X)
    :type: tuple
    :return:
    :rtype: XASObject
    """
    dimensions_ = dimensions
    if dimensions_ is None:
        dimensions_ = (Dim.DIM_2, Dim.DIM_1, Dim.DIM_0)
    reader = XASReader()
    return reader.read_frm_url(
        InputInformation(
            spectra_url=spectra_url,
            channel_url=channel_url,
            config_url=config_url,
            dimensions=dimensions_,
            energy_unit=energy_unit,
        )
    )


def read_frm_file(
    file_path,
    energy_unit=ur.eV,
    dimensions: tuple = (Dim.DIM_2, Dim.DIM_1, Dim.DIM_0),
    columns_names: Union[None, dict] = None,
):
    """

    :param str file_path: path to the file containing the spectra. Must ba a
                          .dat file that pymca can handle or a .h5py with
                          default path
    :param tuple dimensions: dimensions of the input data. For ASCII file can
                             be (X, Y) or (Y, X)
    :param Union[None,tuple] columns: name of the column to take for .dat...
                                      files.
    :return XasObject created from the input
    :rtype: XASObject
    """
    if file_path in (None, ""):
        return
    reader = XASReader()
    return reader.read_from_file(
        file_path=file_path,
        energy_unit=energy_unit,
        dimensions=dimensions,
        columns_names=columns_names,
    )


class XASReader(object):
    """Simple reader of a xas file"""

    @staticmethod
    def read_frm_url(input_information):
        sp, en, conf = read_xas(information=input_information)
        return XASObject(spectra=sp, energy=en, configuration=conf)

    @staticmethod
    def read_from_file(
        file_path,
        energy_unit=ur.eV,
        dimensions=(Dim.DIM_2, Dim.DIM_1, Dim.DIM_0),
        columns_names=None,
    ):
        """

        :param str file_path:
        :return: `.XASObject`
        """
        # TODO: we should be able to avoid calling the creation of an InputInformation
        if file_path.endswith((".dat", ".csv")):
            return XASReader.read_frm_url(
                InputInformation(
                    spectra_url=DataUrl(file_path=file_path, scheme="PyMca"),
                    channel_url=DataUrl(file_path=file_path, scheme="PyMca"),
                    energy_unit=energy_unit,
                    dimensions=dimensions,
                    columns_names=columns_names,
                )
            )
        elif file_path.endswith(".xmu"):
            return XASReader.read_frm_url(
                InputInformation(
                    spectra_url=DataUrl(file_path=file_path, scheme="larch"),
                    channel_url=DataUrl(file_path=file_path, scheme="larch"),
                    energy_unit=energy_unit,
                    dimensions=dimensions,
                    columns_names=columns_names,
                )
            )
        elif h5py.is_hdf5(file_path):
            return XASReader.read_frm_url(
                InputInformation(
                    spectra_url=DataUrl(
                        file_path=file_path,
                        scheme="silx",
                        data_path=DEFAULT_SPECTRA_PATH,
                    ),
                    channel_url=DataUrl(
                        file_path=file_path,
                        scheme="silx",
                        data_path=DEFAULT_CHANNEL_PATH,
                    ),
                    config_url=DataUrl(
                        file_path=file_path, scheme="silx", data_path="configuration"
                    ),
                    energy_unit=energy_unit,
                    dimensions=dimensions,
                )
            )
        else:
            raise ValueError(
                "file type {} not managed, unable to load".format(file_path)
            )

    __call__ = read_from_file


class XASWriter(object):
    """
    class to write the output file. In this case we need a class in order to
    setup the output file before
    """

    def __init__(self):
        self._output_file = None

    @property
    def output_file(self):
        return self._output_file

    @output_file.setter
    def output_file(self, file_):
        self._output_file = file_

    def set_properties(self, properties):
        if "_output_file_setting" in properties:
            self._output_file = properties["_output_file_setting"]

    def dump_xas(self, xas_obj, write_process=True):
        """
        write the XASObject into a hdf5 file.

        :param xas_obj: object to be stored
        :type: Union[:class:`.XASObject`,dict]
        :param bool write_process: if True then store the process flow in the
            same file.
        """
        if isinstance(xas_obj, dict):
            _xas_obj = XASObject.from_dict(xas_obj)
        else:
            _xas_obj = xas_obj

        if not self._output_file:
            _logger.warning(
                "no output file defined, please give path to the" "output file"
            )
            self._output_file = input()

        _logger.info("dump xas obj to {}".format(self._output_file))

        # write raw data
        write_xas(
            h5_file=self._output_file,
            energy=_xas_obj.energy,
            mu=_xas_obj.absorbed_beam(),
            entry=_xas_obj.entry,
        )

        if write_process is True:
            if len(get_xasproc(self._output_file, entry=_xas_obj.entry)) > 0:
                _logger.warning(
                    "removing previous process registred. They are no " "more accurate"
                )
                _xas_obj.clean_process_flow()

            # write process flow
            _xas_obj.copy_process_flow_to(self._output_file)

    __call__ = dump_xas
