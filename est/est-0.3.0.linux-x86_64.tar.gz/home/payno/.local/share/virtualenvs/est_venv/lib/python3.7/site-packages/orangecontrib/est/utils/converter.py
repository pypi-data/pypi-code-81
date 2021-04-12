# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016 European Synchrotron Radiation Facility
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
__date__ = "08/08/2019"


import Orange.data
from est.core.types import XASObject
import numpy
import logging

_logger = logging.getLogger(__name__)


class Converter(object):
    """This converter insure a minimal conversion between xas_object and
    Orange.data.Table by only storing energy and absorbed beam (mu)"""

    @staticmethod
    def toXASObject(data_table):
        energy = _retrieve_energy(data_table.domain)
        mu = data_table.X
        mu = numpy.swapaxes(mu, 1, 0)
        mu = mu.reshape(mu.shape[0], mu.shape[1], 1)
        # note: for now we only consider 2D spectra...
        return XASObject(energy=energy, spectra=mu, dim2=1, dim1=mu.shape[-1])

    @staticmethod
    def toDataTable(xas_object):
        _logger.warning(
            "casting xas_object to Orange.data.Table might bring "
            "lost of some information (process flow, "
            "treatment result...). Only keep energy and absorbed "
            "beam information"
        )
        # TODO: prendre normalized_mu and normalized_energy if exists,
        # otherwise take mu and energy...
        spectra = xas_object.spectra.map_to(data_info="mu")
        # invert dimensions and axis to fit spectroscopy add-on
        X = spectra.reshape((spectra.shape[0], -1))
        X = numpy.swapaxes(X, 0, 1)

        domain = Orange.data.Domain(
            attributes=[
                Orange.data.ContinuousVariable.make("%f" % f) for f in xas_object.energy
            ]
        )
        data = Orange.data.Table.from_numpy(domain=domain, X=X)
        return data


def _retrieve_energy(domain):
    """
    Return x of the data. If all attribute names are numbers,
    return their values. If not, return indices.
    """
    energy = numpy.arange(len(domain.attributes), dtype="f")
    try:
        energy = numpy.array([float(a.name) for a in domain.attributes])
    except:
        _logger.error("fail to retrieve energy from attributes")
    return energy
