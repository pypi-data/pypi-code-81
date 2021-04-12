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

import functools
import logging
import multiprocessing

from PyMca5.PyMcaPhysics.xas.XASClass import XASClass, e2k
from est.core.process.process import _input_desc
from est.core.process.process import _output_desc
from est.core.process.process import Process
from est.core.process.pymca.exafs import process_spectr_exafs
from est.core.types import XASObject, Spectrum

_logger = logging.getLogger(__name__)


def process_spectr_k(
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
    :param callback: callback to execute.
    :param output: list to store the result, needed for pool processing
    :type: multiprocessing.manager.list
    :param output_dict: key is input spectrum, value is index in the output
                        list.
    :type: dict
    :return: processed spectrum
    :rtype: tuple (configuration, spectrum)
    """
    _logger.debug(
        "start k weight definition on spectrum (%s, %s)" % (spectrum.x, spectrum.y)
    )
    assert spectrum is not None

    pymca_xas = XASClass()
    if spectrum.energy is None or spectrum.mu is None:
        raise ValueError(
            "Energy and or Mu is/are not specified, unable to " "compute exafs"
        )
    pymca_xas.setSpectrum(energy=spectrum.energy, mu=spectrum.mu)
    if configuration is not None:
        if "KWeight" in configuration and configuration["KWeight"] is not None:
            configuration["FT"]["KWeight"] = configuration["KWeight"]
            configuration["EXAFS"]["KWeight"] = configuration["KWeight"]
        pymca_xas.setConfiguration(configuration)

    if overwrite:
        spectrum_ = spectrum
    else:
        spectrum_ = Spectrum.from_dict(spectrum.to_dict())

    # we need to update EXAFSNormalized since we are overwriting it
    cf, exafs_res = process_spectr_exafs(
        spectrum=spectrum_, configuration=configuration
    )
    if exafs_res is None:
        err = "Failed to process exafs."
        if spectrum.x is not None or spectrum.y is not None:
            err = (
                err
                + "Spectrum (x, y) coords: "
                + ",".join((str(spectrum.x), str(spectrum.y)))
            )
        raise ValueError(err)

    # update EXAFSNormalized
    e0 = pymca_xas.calculateE0()

    kValues = e2k(spectrum_.energy - e0)
    exafs = exafs_res["EXAFSNormalized"]
    if "KWeight" in configuration and configuration["KWeight"] is not None:
        exafs *= pow(kValues, configuration["KWeight"])
    spectrum_["EXAFSNormalized"] = exafs
    configuration_ = pymca_xas.getConfiguration()

    if callbacks:
        for callback in callbacks:
            callback()

    if output is not None:
        assert output_dict is not None
        output[output_dict[spectrum]] = spectrum_
    return configuration_, spectrum_


def pymca_k_weight(xas_obj):
    """
    Set weight for exafs values

    :param xas_obj: object containing the configuration and spectra to process
    :type: Union[:class:`.XASObject`, dict]
    :return: spectra dict
    :rtype: :class:`.XASObject`
    """
    k_weight_obj = PyMca_k_weight()
    return k_weight_obj.process(xas_obj=xas_obj)


_USE_MULTIPROCESSING_POOL = False
# note: we cannot use multiprocessing pool with pypushflow for now.


class PyMca_k_weight(Process):

    inputs = [
        _input_desc(name="xas_obj", type=XASObject, handler="process", doc=""),
    ]

    outputs = [
        _output_desc(name="xas_obj", type=XASObject, doc=""),
    ]

    def __init__(self):
        Process.__init__(self, name="k weight")

    def set_properties(self, properties):
        if "_kWeightSetting" in properties:
            _properties = properties.copy()
            _properties["k_weight"] = _properties["_kWeightSetting"]
            del _properties["_kWeightSetting"]
            self.setConfiguration(_properties)

    def _k_weight(self):
        if "k_weight" in self._settings:
            return self._settings["k_weight"]
        return None

    def process(self, xas_obj):
        """

        :param xas_obj: object containing the configuration and spectra to process
        :type: Union[:class:`.XASObject`, dict]
        :return: spectra dict
        :rtype: :class:`.XASObject`
        """
        assert xas_obj is not None
        _xas_obj = self.getXasObject(xas_obj=xas_obj)
        if self._k_weight() is not None:
            _xas_obj.configuration["SET_KWEIGHT"] = self._k_weight()

        if "SET_KWEIGHT" not in _xas_obj.configuration:
            _logger.warning(
                "Missing configuration to know which value we should set "
                "to k weight, will be set to 0 by default"
            )
            _xas_obj.configuration["SET_KWEIGHT"] = 0

        for key in ("FT", "EXAFS", "Normalization"):
            if key not in _xas_obj.configuration:
                _xas_obj.configuration[key] = {}

        _xas_obj.configuration["KWeight"] = _xas_obj.configuration["SET_KWEIGHT"]
        _xas_obj.configuration["FT"]["KWeight"] = _xas_obj.configuration["SET_KWEIGHT"]
        _xas_obj.configuration["EXAFS"]["KWeight"] = _xas_obj.configuration[
            "SET_KWEIGHT"
        ]
        _xas_obj.configuration["Normalization"]["KWeight"] = _xas_obj.configuration[
            "SET_KWEIGHT"
        ]

        self._advancement.reset(max_=_xas_obj.n_spectrum)
        self._advancement.startProcess()
        self._pool_process(xas_obj=_xas_obj)
        self._advancement.endProcess()
        self.register_process(xas_obj=_xas_obj, data_keys=tuple())
        return _xas_obj

    def _pool_process(self, xas_obj):
        """process normalization from a pool"""
        assert isinstance(xas_obj, XASObject)
        if not _USE_MULTIPROCESSING_POOL:
            assert "KWeight" in xas_obj.configuration
            for spectrum in xas_obj.spectra.data.flat:
                process_spectr_k(
                    spectrum=spectrum,
                    configuration=xas_obj.configuration,
                    callbacks=self.callbacks,
                    overwrite=True,
                )
                assert "KWeight" in xas_obj.configuration
        else:
            with multiprocessing.Pool(5) as p:
                partial_ = functools.partial(
                    process_spectr_k,
                    configuration=xas_obj.configuration,
                    callbacks=self.callbacks,
                    overwrite=True,
                )
                p.map(partial_, xas_obj.spectra)

    def definition(self):
        return "Define k weight for xas treatment"

    def program_version(self):
        import PyMca5

        return PyMca5.version()

    def program_name(self):
        return "pymca_k_weight"

    __call__ = process


if __name__ == "__main__":
    import sys
    import yaml

    xas_object_yaml_file = sys.argv[1]
    _logger.debug("Load xas object from {}".format(xas_object_yaml_file))
    with open(xas_object_yaml_file, "r") as file:
        ddict = yaml.load(file)["input_data"]
        xas_object = XASObject.from_dict(ddict)
    print("******* do k-weight ********")
    res_xas_object = pymca_k_weight(xas_obj=xas_object)
    res_xas_object._create_saving_pt()

    # dump resulting object
    with open(xas_object_yaml_file, "w") as file:
        yaml.dump({"input_data": res_xas_object.to_dict()}, file)

    # dump resulting object into output_normalization file
    with open("output_k_weight.yaml", "w") as file:
        yaml.dump({"input_data": res_xas_object.to_dict()}, file)
