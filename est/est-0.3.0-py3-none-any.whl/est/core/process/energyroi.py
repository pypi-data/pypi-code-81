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
__date__ = "27/01/2021"

from est.core.types import XASObject
from .process import Process
from est.core.process.process import _input_desc
from est.core.process.process import _output_desc
import logging
from typing import Union

_logger = logging.getLogger(__name__)


def xas_energy_roi(xas_obj):
    """
    apply roi on the XASObject.spectra

    :param xas_obj: object containing the configuration and spectra to process
    :type: Union[:class:`.XASObject`, dict]
    :return: spectra dict
    :rtype: :class:`.XASObject`
    """
    xas_roi_process = EnergyROIProcess()
    return xas_roi_process.process(xas_obj=xas_obj)


class ROI1D:
    def __init__(self, from_, to_):
        self.from_ = from_
        self.to_ = to_


class EnergyROIProcess(Process):

    inputs = [
        _input_desc(name="xas_obj", type=XASObject, handler="process", doc=""),
    ]

    outputs = [
        _output_desc(name="xas_obj", type=XASObject, doc=""),
    ]

    def __init__(self):
        Process.__init__(self, name="energy roi")
        self._roi = ROI1D(0, 9999999999)

    def set_properties(self, properties: dict):
        if "energy_roi" in properties:
            self._settings = properties["energy_roi"]
            self._read_roi(self._settings)

    def update_properties(self, properties):
        super().update_properties(properties=properties)
        self._read_roi(properties=self._settings)

    def _read_roi(self, properties):
        if "minE" in properties:
            self._roi.from_ = properties["minE"]
        if "maxE" in properties:
            self._roi.to_ = properties["maxE"]

    def setRoi(self, from_, to_):
        self._roi = ROI1D(from_=from_, to_=to_)

    def _apply_roi(self, xas_obj, roi):
        mask = (xas_obj.spectra.energy <= roi.to_) & (
            xas_obj.spectra.energy >= roi.from_
        )
        xas_obj.spectra.energy = xas_obj.spectra.energy[mask]
        for spectrum in xas_obj.spectra.data.flat:
            spectrum.energy = spectrum.energy[mask]
            spectrum.mu = spectrum.mu[mask]
            for attached_key in ("I0", "I1", "I2", "mu_ref"):
                if hasattr(spectrum, attached_key):
                    values = getattr(spectrum, attached_key)[mask]
                    setattr(spectrum, attached_key, values)
        #     print(spectrum.__dict__)
        # print(xas_obj.__dict__)
        return xas_obj

    def process(self, xas_obj: Union[dict, XASObject]):
        """

        :param xas_obj: object containing the configuration and spectra to process
        :type: Union[:class:`.XASObject`, dict]
        :return: spectra dict
        :rtype: :class:`.XASObject`
        """
        assert xas_obj is not None
        _xas_obj = self.getXasObject(xas_obj=xas_obj)

        # existing roi is priority. This is the case if called from pushworkflow
        # for example.
        if self._roi is not None:
            xas_obj = self._apply_roi(xas_obj=_xas_obj, roi=self._roi)

        self.register_process(_xas_obj, data_keys=("Mu", "energy"))
        return xas_obj

    def definition(self):
        return "apply a ROI on energy range"

    def program_version(self):
        import est.version

        return est.version.version

    def program_name(self):
        return "energy-roi"

    __call__ = process
