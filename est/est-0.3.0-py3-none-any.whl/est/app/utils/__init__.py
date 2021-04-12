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
__date__ = "10/12/2020"


from silx.io.url import DataUrl
from est.units import ur
from est.core.types import Dim
from est.thirdparty.silx.hdf5file import get_data
from est.core.types import Spectrum, XASObject
from est.core.io import read_xas
from est.io.utils.information import InputInformation
import logging

try:
    from est.io.utils.spec import read_spectrum

    has_read_spectrum = True
except ImportError:
    has_read_spectrum = False
_logger = logging.getLogger(__name__)


def convert_spectra_dims(dims):
    """
    Convert a tuple of dims that can be strings... to a tuple of
    est.core.types.Dim
    """
    if dims is None:
        return None
    res = []
    for dim in dims:
        if isinstance(dim, str):
            if dim.lower() == Dim.DIM_0.value.lower():
                dim = Dim.DIM_0
            elif dim.lower() == Dim.DIM_1.value.lower():
                dim = Dim.DIM_1
            elif dim.lower() == Dim.DIM_2.value.lower():
                dim = Dim.DIM_2

        dim = Dim.from_value(dim)
        if dim in res:
            raise ValueError(
                "dimension {} has been provided several time."
                "Each dimension should be set once.".format(dim.value())
            )
        else:
            res.append(dim)
    return tuple(dims)


def get_unit(current_unit):
    if current_unit == "eV":
        return ur.eV
    elif current_unit == "keV":
        return ur.keV
    elif current_unit == "J":
        return ur.J
    elif current_unit == "kJ":
        return ur.kJ
    elif isinstance(current_unit, ur.Quantity):
        return current_unit
    else:
        raise ValueError("{} is not a valid unit for quantity".format(current_unit))


def get_url(my_str):
    if my_str in (None, ""):
        return None
    else:
        assert isinstance(my_str, str)
        if "@" in my_str:
            try:
                entry, file_path = my_str.split("@")
            except Exception:
                pass
            else:
                return DataUrl(file_path=file_path, data_path=entry, scheme="silx")
        else:
            try:
                url = DataUrl(path=my_str)
            except Exception:
                pass
            else:
                return url
        raise ValueError("unrecognized url {}".format(my_str))


def get_xas_obj(input_information: InputInformation):
    """load xas object from command line input
    :param spec_input: tuple of Union[str, None, dict]
    """
    print("#### call get_xas_obj")
    if input_information.is_spec_input():
        if has_read_spectrum:
            energy, mu = read_spectrum(
                spec_file=input_information.spec_file,
                energy_col_name=input_information.input_energy_col_name,
                absorption_col_name=input_information.input_abs_col_name,
                monitor_col_name=input_information.input_monitor_col_name,
                energy_unit=input_information.energy_unit,
                scan_header_S=input_information.scan_title,
            )
            spectrum = Spectrum(energy=energy, mu=mu)
            xas_obj = XASObject(energy=energy, spectra=(spectrum,), dim1=1, dim2=1)
        else:
            raise ValueError("Unable to read spectrum")
    else:
        sp, en, conf = read_xas(information=input_information)
        xas_obj = XASObject(spectra=sp, energy=en, configuration=conf)
    attr_names = "I0", "I1", "I2", "mu_ref"
    attr_values = (
        getattr(input_information, "I0", None),
        getattr(input_information, "I1", None),
        getattr(input_information, "I2", None),
        getattr(input_information, "mu_ref", None),
    )
    for attr_name, attr_value in zip(attr_names, attr_values):
        if attr_value is not None:
            if isinstance(attr_value, DataUrl):
                data = get_data(attr_value)
            else:
                data = attr_value
            if data.shape[0] > xas_obj.energy.shape[0]:
                _logger.warning(
                    "energy has less value than dataset. Clip {}.".format(attr_name)
                )
                data = data[: xas_obj.energy.shape[0]]
            xas_obj.attach_3d_array(attr_name, data)
    return xas_obj
