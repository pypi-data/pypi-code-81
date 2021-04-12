# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
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
__date__ = "25/01/2021"


from est.core.types import Dim
from est.units import ur


class SpecInputInformation:
    """Input information relative to spec"""

    def __init__(
        self,
        spec_file,
        energy_abs_col_name,
        input_abs_col_name,
        input_monitor_col_name,
        scan_title,
    ):
        self.__spec_file = None
        self.__scan_title = None
        self.__energy_abs_col_name = None
        self.__input_abs_col_name = None
        self.__input_monitor_col_name = None

        self.spec_file = spec_file
        self.scan_title = scan_title
        self.energy_abs_col_name = energy_abs_col_name
        self.input_abs_col_name = input_abs_col_name
        self.input_monitor_col_name = input_monitor_col_name

    @property
    def spec_file(self):
        return self.__spec_file

    @spec_file.setter
    def spec_file(self, spec_file):
        self.__spec_file = spec_file

    @property
    def scan_title(self):
        return self.__scan_title

    @scan_title.setter
    def scan_title(self, title):
        self.__scan_title = title

    @property
    def energy_abs_col_name(self):
        return self.__energy_abs_col_name

    @energy_abs_col_name.setter
    def energy_abs_col_name(self, col_name):
        self.__energy_abs_col_name = col_name

    @property
    def input_abs_col_name(self):
        return self.__input_abs_col_name

    @input_abs_col_name.setter
    def input_abs_col_name(self, col_name):
        self.__input_abs_col_name = col_name

    @property
    def input_monitor_col_name(self):
        return self.__input_monitor_col_name

    @input_monitor_col_name.setter
    def input_monitor_col_name(self, col_name):
        self.__input_monitor_col_name = col_name


class _HDF5InputInformation:
    def __init__(self):
        pass


class InputInformation:
    """
    Utils class to store input information
    """

    def __init__(
        self,
        spectra_url,
        channel_url,
        config_url=None,
        dimensions=(Dim.DIM_2, Dim.DIM_1, Dim.DIM_0),
        energy_unit=ur.eV,
        spec_input=None,
        columns_names=None,
    ):
        # main information
        self.__spectra_url = None
        self.__channel_url = None
        self.__dimensions = None
        self.__config_url = None
        self.__energy_unit = None
        self.__spec_info = None
        self.__columns_names = None

        # "fancy information"
        self.__I0_url = None
        self.__I1_url = None
        self.__I2_url = None
        self.__mu_ref_url = None

        self.spectra_url = spectra_url
        self.channel_url = channel_url
        self.config_url = config_url
        self.dimensions = dimensions
        self.energy_unit = energy_unit
        self.columns_names = columns_names

    def is_spec_input(self) -> bool:
        """return True if the input information (spectra...) comes from a
        spec file
        """
        return self.__spec_info is not None

    def has_url_information(self) -> bool:
        """
        Return True if this contains at least on of the following url:
               input_spectra_url or input_channel_url or input_configuration_url

        """
        return self.spectra_url or self.channel_url or self.configuration_url

    def is_valid(self):
        """Return True if at least a spec file is provided or some url
        information"""
        return self.spec_file is not None or self.has_url_information

    @property
    def spectra_url(self):
        return self.__spectra_url

    @spectra_url.setter
    def spectra_url(self, url):
        # TODO: maybe we want to add a check to create a DataUrl if this is a string...
        self.__spectra_url = url

    @property
    def channel_url(self):
        return self.__channel_url

    @channel_url.setter
    def channel_url(self, url):
        self.__channel_url = url

    @property
    def config_url(self):
        return self.__config_url

    @config_url.setter
    def config_url(self, url):
        self.__config_url = url

    @property
    def dimensions(self):
        return self.__dimensions

    @dimensions.setter
    def dimensions(self, dims):
        self.__dimensions = dims

    @property
    def energy_unit(self):
        return self.__energy_unit

    @energy_unit.setter
    def energy_unit(self, unit):
        self.__energy_unit = unit

    @property
    def columns_names(self):
        return self.__columns_names

    @columns_names.setter
    def columns_names(self, columns_names):
        self.__columns_names = columns_names

    @property
    def I0_url(self):
        return self.__I0_url

    @I0_url.setter
    def I0_url(self, url):
        self.__I0_url = url

    @property
    def I1_url(self):
        return self.__I1_url

    @I1_url.setter
    def I1_url(self, url):
        self.__I1_url = url

    @property
    def I2_url(self):
        return self.__I2_url

    @I2_url.setter
    def I2_url(self, url):
        self.__I2_url = url

    @property
    def mu_ref_url(self):
        return self.__mu_ref_url

    @mu_ref_url.setter
    def mu_ref_url(self, url):
        self.__mu_ref_url = url

    @property
    def spec_info(self):
        return self.__spec_info

    @property
    def scan_title(self):
        if self.is_spec_input():
            return self.spec_info.scan_title
        else:
            return None

    @property
    def scan_title(self):
        if self.is_spec_input():
            return self.spec_info.scan_title
        else:
            return None

    @property
    def spec_file(self):
        if self.is_spec_input():
            return self.spec_info.spec_file
        else:
            return None

    @property
    def input_energy_col_name(self):
        if self.is_spec_input():
            return self.spec_info.input_energy_col_name
        else:
            return None

    @property
    def input_abs_col_name(self):
        if self.is_spec_input():
            return self.spec_info.input_abs_col_name
        else:
            return None

    @property
    def input_monitor_col_name(self):
        if self.is_spec_input():
            return self.spec_info.input_monitor_col_name
        else:
            return None

    def __str__(self):
        return "\n".join(
            (
                "is spec: {}".format(self.is_spec_input()),
                "spectra url is: {}".format(self.spectra_url),
                "channel url is: {}".format(self.channel_url),
                "config url is: {}".format(self.config_url),
                "dimensions are: {}".format(self.dimensions),
                "energy unit is: {}".format(self.energy_unit),
                "columns names: {}".format(self.columns_names),
            )
        )
