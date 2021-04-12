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

from est.core.types import XASObject, Spectrum
from .process import Process
import logging

_logger = logging.getLogger(__name__)


def _xas_set_config(xas_obj):
    """
    Copy process configuration to object

    :param xas_obj: object containing the configuration and spectra to process
    :type: Union[:class:`.XASObject`, dict]
    :return: spectra dict
    :rtype: :class:`.XASObject`
    """
    xas_set_config = _SetConfigProcess()
    return xas_set_config.process(xas_obj=xas_obj)


class _SetConfigProcess(Process):
    def __init__(self):
        Process.__init__(self, name="set_config")

    def process(self, xas_obj):
        """

        :param xas_obj: object containing the configuration and spectra to process
        :type: Union[:class:`.XASObject`, dict]
        :return: spectra dict
        :rtype: :class:`.XASObject`
        """
        assert xas_obj is not None
        _xas_obj = self.getXasObject(xas_obj=xas_obj)
        conf_obj = _xas_obj.configuration
        conf_process = self.getConfiguration()
        for key, value in conf_process.items():
            conf_obj[key] = value
        _xas_obj.configuration = conf_obj
        return _xas_obj
