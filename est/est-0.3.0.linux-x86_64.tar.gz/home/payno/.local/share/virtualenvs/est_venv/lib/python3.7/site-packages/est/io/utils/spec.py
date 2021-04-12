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
__date__ = "06/11/2019"

from silx.io.spech5 import SpecFile
from est.units import ur
import functools
import numpy


@functools.lru_cache(maxsize=2)
def read_spectrum(
    spec_file,
    energy_col_name=None,
    absorption_col_name=None,
    monitor_col_name=None,
    energy_unit=ur.eV,
    scan_header_S=None,
):
    """
    :note: the cache is sued because we call twice the same function for energy
           and absorption


    :param str spec_file: path to the spec file containing the spectra
                          definition
    :param str energy_col_index:
    :param str absorption_col_index:
    :param Union[str,None] monitor_col_name: name of the column to get monitor
    :param Union[str,None] scan_header_S: name of the scan to consider

    :return: (energy, mu)
    :rtype: tuple energy and list of absorption
    """
    spec_file = SpecFile(spec_file)
    energy = None
    mu = None
    for i_data, scan in enumerate(spec_file):
        # if a scan header 'title' is provided
        if scan_header_S is not None and scan_header_S != scan.scan_header_dict["S"]:
            continue

        if (
            energy_col_name not in scan.labels
            and absorption_col_name not in scan.labels
        ):
            continue

        # get energy
        if energy_col_name is not None:
            energy = spec_file.data_column_by_name(
                scan_index=i_data, label=energy_col_name
            )
            if energy is not None:
                energy = (energy * energy_unit).m_as(ur.eV)

        # get absorption
        if absorption_col_name is not None:
            mu = spec_file.data_column_by_name(
                scan_index=i_data, label=absorption_col_name
            )

            if energy is not None:
                assert len(mu) == len(
                    energy
                ), "different number of elements between energy {} and absorption {}".format(
                    len(energy), len(mu)
                )

        # get monitor
        if monitor_col_name is not None:
            monitor = spec_file.data_column_by_name(
                scan_index=i_data, label=monitor_col_name
            )
            mu = mu / monitor

        return energy, numpy.asarray(mu)
    return energy, mu
