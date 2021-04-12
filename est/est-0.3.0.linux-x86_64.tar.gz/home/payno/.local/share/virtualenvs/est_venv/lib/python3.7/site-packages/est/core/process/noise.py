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
__date__ = "18/01/2021"

from est.core.types import XASObject
from est.core.types import Spectrum
from est.core.process.process import _input_desc
from est.core.process.process import _output_desc
from .process import Process
from .process import _NexusSpectrumDef
from .process import _NexusDatasetDef
import scipy.signal
import logging
import numpy
import pkg_resources
import multiprocessing
import functools
from typing import Union

_logger = logging.getLogger(__name__)


_USE_MULTIPROCESSING_POOL = False
# note: we cannot use multiprocessing pool with pypushflow for now.


def process_noise_savgol(
    spectrum,
    configuration,
    overwrite=True,
    callbacks=None,
    output=None,
    output_dict=None,
):
    """

    :param spectrum: spectrum to process
    :type: :class:`.Spectrum`
    :param configuration: configuration of the pymca normalization
    :type: dict
    :param overwrite: False if we want to return a new Spectrum instance
    :type: bool
    :param callbacks: callback to execute.
    :param output: list to store the result, needed for pool processing
    :type: multiprocessing.manager.list
    :param output_dict: key is input spectrum, value is index in the output
                        list.
    :type: dict
    :return: processed spectrum
    :rtype: tuple (configuration, spectrum)
    """
    _logger.debug(
        "start noise with Savitsky-Golay on spectrum (%s, %s)"
        % (spectrum.x, spectrum.y)
    )
    if "noise" in configuration:
        configuration = configuration["noise"]
    if not "window_size" in configuration:
        raise ValueError("`window_size` should be specify. Missing in configuration")
    else:
        window_size = configuration["window_size"]
    if not "polynomial_order" in configuration:
        raise ValueError(
            "`polynomial_order` should be specify. Missing in configuration"
        )
    else:
        polynomial_order = configuration["polynomial_order"]
    if not "e_min" in configuration:
        e_min = None
    else:
        e_min = configuration["e_min"]
    if not "e_max" in configuration:
        e_max = None
    else:
        e_max = configuration["e_max"]

    if e_min in (None, -1):
        e_min = spectrum.energy.min() - 1
    if e_max in (None, -1):
        e_max = spectrum.energy.max() + 1

    mask = (spectrum.energy > e_min) & (spectrum.energy < (e_max))
    noise_savgol_energy = spectrum.energy[mask]
    raw_mu = spectrum.mu[mask]
    smooth_spectrum = scipy.signal.savgol_filter(raw_mu, window_size, polynomial_order)
    noise = numpy.absolute(raw_mu - smooth_spectrum)
    spectrum.noise_savgol = noise
    if hasattr(spectrum, "edge_step"):
        spectrum.norm_noise_savgol = numpy.mean(noise) / spectrum.edge_step
    else:
        spectrum.norm_noise_savgol = None
        _logger.warning(
            "Unable to compute Normalized edge."
            "Normalization (pre-edge) should be run first"
        )
    spectrum.noise_savgol_energy = noise_savgol_energy

    if callbacks:
        for callback in callbacks:
            callback()

    if overwrite:
        spectrum_ = spectrum
    else:
        spectrum_ = Spectrum()
        spectrum_.update(spectrum)

    if output is not None:
        assert output_dict is not None
        output[output_dict[spectrum]] = spectrum_
    return configuration, spectrum_


def xas_noise(xas_obj):
    """
    apply roi on the XASObject.spectra

    :param xas_obj: object containing the configuration and spectra to process
    :type: Union[:class:`.XASObject`, dict]
    :return: spectra dict
    :rtype: :class:`.XASObject`
    """
    xas_noise_process = NoiseProcess()
    return xas_noise_process.process(xas_obj=xas_obj)


class NoiseProcess(Process):

    inputs = [
        _input_desc(name="xas_obj", type=XASObject, handler="process", doc=""),
    ]

    outputs = [
        _output_desc(name="xas_obj", type=XASObject, doc=""),
    ]

    def __init__(self):
        Process.__init__(self, name="noise")
        self._window_size = 5
        self._polynomial_order = 2

    def set_properties(self, properties: dict):
        if "noise" in properties:
            properties = properties["noise"]
        self._settings = properties
        if "window_size" in properties:
            self._window_size = properties["window_size"]
        if "polynomial_order" in properties:
            self._polynomial_order = properties["polynomial_order"]

    def process(self, xas_obj: Union[dict, XASObject]):
        """

        :param xas_obj: object containing the configuration and spectra to process
        :type: Union[:class:`.XASObject`, dict]
        :return: spectra dict
        :rtype: :class:`.XASObject`
        """
        assert xas_obj is not None
        _xas_obj = self.getXasObject(xas_obj=xas_obj)

        if self._settings:
            _xas_obj.configuration["noise"] = self._settings

        self._advancement.reset(max_=_xas_obj.n_spectrum)
        self._advancement.startProcess()
        self._pool_process(xas_obj=_xas_obj)
        self._advancement.endProcess()
        self.register_process(
            _xas_obj,
            data_keys=(
                _NexusDatasetDef("norm_noise_savgol"),
                _NexusDatasetDef("noise_savgol", units="raw data noise"),
                _NexusDatasetDef("noise_savgol_energy", units="eV"),
                _NexusDatasetDef("edge_step"),
            ),
            plots=(
                _NexusSpectrumDef(
                    signal="noise_savgol",
                    axes=("noise_savgol_energy",),
                    auxiliary_signals=None,
                    silx_style={"signal_scale_type": "log"},
                    title="noise",
                ),
            ),
        )
        return _xas_obj

    def _pool_process(self, xas_obj):
        assert isinstance(xas_obj, XASObject)
        if not _USE_MULTIPROCESSING_POOL:
            for spectrum in xas_obj.spectra:
                process_noise_savgol(
                    spectrum=spectrum,
                    configuration=xas_obj.configuration,
                    callbacks=self.callbacks,
                    overwrite=True,
                )
        else:
            from multiprocessing import Manager

            manager = Manager()
            output_dict = {}
            res_list = manager.list()
            for i_spect, spect in enumerate(xas_obj.spectra):
                res_list.append(None)
                output_dict[spect] = i_spect

            with multiprocessing.Pool(1) as p:
                partial_ = functools.partial(
                    process_noise_savgol,
                    configuration=xas_obj.configuration,
                    callbacks=self.callbacks,
                    overwrite=False,
                    output=res_list,
                    output_dict=output_dict,
                )
                p.map(partial_, xas_obj.spectra)

            # then update local spectrum
            for spectrum, res in zip(xas_obj.spectra, res_list):
                spectrum.update(res)

    def definition(self):
        return "noise using Savitsky-Golay algorithm"

    def program_version(self):
        return pkg_resources.get_distribution("est").version

    def program_name(self):
        return "noise_savgol"

    __call__ = process
