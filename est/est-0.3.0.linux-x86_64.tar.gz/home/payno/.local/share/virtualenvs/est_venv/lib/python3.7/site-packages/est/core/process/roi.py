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

from est.core.types import XASObject
from est.core.types import Spectrum
from est.core.types import Spectra
from est.core.process.process import _input_desc
from est.core.process.process import _output_desc
from .process import Process
import logging
import numpy
import pint
from typing import Union

_logger = logging.getLogger(__name__)


def xas_roi(xas_obj):
    """
    apply roi on the XASObject.spectra

    :param xas_obj: object containing the configuration and spectra to process
    :type: Union[:class:`.XASObject`, dict]
    :return: spectra dict
    :rtype: :class:`.XASObject`
    """
    xas_roi_process = ROIProcess()
    return xas_roi_process.process(xas_obj=xas_obj)


class _ROI(object):
    def __init__(self, origin, size):
        self.origin = origin
        self.size = size

    @property
    def origin(self) -> tuple:
        return self.__origin

    @origin.setter
    def origin(self, origin: Union[list, tuple]):
        self.__origin = int(origin[0]), int(origin[1])

    @property
    def size(self) -> tuple:
        return self.__size

    @size.setter
    def size(self, size: Union[list, tuple]):
        self.__size = int(size[0]), int(size[1])

    def to_dict(self) -> dict:
        return {"origin": self.origin, "size": self.size}

    @staticmethod
    def from_dict(ddict: dict):
        return _ROI(origin=ddict["origin"], size=ddict["size"])

    @staticmethod
    def from_silx_def(silx_roi):
        origin = silx_roi.getOrigin()
        size = silx_roi.getSize()
        return _ROI(origin=origin, size=size)


class ROIProcess(Process):

    inputs = [
        _input_desc(name="xas_obj", type=XASObject, handler="process", doc=""),
    ]

    outputs = [
        _output_desc(name="xas_obj", type=XASObject, doc=""),
    ]

    def __init__(self):
        Process.__init__(self, name="roi")
        self._roi = None

    def set_properties(self, properties: dict):
        if "roi" in properties:
            self._roi = _ROI.from_dict(properties["roi"])

    def setRoi(self, origin: Union[list, tuple], size: Union[list, tuple]):
        self._roi = _ROI(origin=origin, size=size)

    def _apply_roi(self, xas_obj, roi):
        _logger.warning("applying roi")
        assert isinstance(xas_obj, XASObject)
        assert isinstance(roi, _ROI)
        assert type(roi.origin[0]) is int
        assert type(roi.origin[1]) is int
        assert type(roi.size[0]) is int
        assert type(roi.size[1]) is int
        ymin, ymax = roi.origin[1], roi.origin[1] + roi.size[1]
        xmin, xmax = roi.origin[0], roi.origin[0] + roi.size[0]
        # clip roi
        ymin = max(ymin, 0)
        ymax = min(ymax, xas_obj.spectra.shape[0])
        xmin = max(xmin, 0)
        xmax = min(xmax, xas_obj.spectra.shape[1])
        assert type(ymin) is int
        assert type(ymax) is int
        assert type(xmin) is int
        assert type(xmax) is int
        assert ymax - ymin == roi.size[1]
        assert xmax - xmin == roi.size[0]

        # TODO: create a spectra object which deal automatically with
        # the following. Should be part of spectra object
        volumes = {}
        for key in xas_obj.spectra_keys():
            if isinstance(
                xas_obj.spectra.data.flat[0][key], (numpy.ndarray, pint.Quantity)
            ):
                # there is no processing for the _larch_grp_members case
                if key == "_larch_grp_members":
                    continue
                volume = xas_obj.spectra.map_to(data_info=key)
                volume_res = volume[:, ymin:ymax, xmin:xmax]
                volume_res = volume_res.reshape(volume_res.shape[0], -1)
                volumes[key] = volume_res

        # then rewrite spectrum list
        assert "Mu" in volumes
        assert "Energy" in volumes
        _mus = volumes["Mu"]
        _energies = volumes["Energy"]
        new_spectra = []
        assert _mus.shape == _energies.shape
        n_new_spectrum = roi.size[0] * roi.size[1]
        assert n_new_spectrum == _mus.shape[1]
        # create the new spectrum
        for i_new_spectrum in range(n_new_spectrum):
            new_spectra.append(
                Spectrum(
                    mu=_mus[:, i_new_spectrum], energy=_energies[:, i_new_spectrum]
                )
            )

        # update them from extra keys
        del volumes["Mu"]
        del volumes["Energy"]
        for key in volumes:
            for slice, new_spectrum in zip(volumes[key], new_spectra):
                new_spectrum[key] = slice

        # set the spectra
        xas_obj.spectra = Spectra(energy=_energies[:, 0], spectra=new_spectra)

        # update the dimensions
        xas_obj.spectra.reshape((roi.size[1], roi.size[0]))
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
            return self._apply_roi(xas_obj=_xas_obj, roi=self._roi)
        elif "roi" in _xas_obj.configuration:
            roi_dict = _xas_obj.configuration["roi"]
            origin, size = roi_dict["origin"], roi_dict["size"]
            return self._apply_roi(xas_obj=_xas_obj, roi=_ROI(origin, size))
        else:
            return _xas_obj

    __call__ = process
