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

import numpy
from PyMca5.PyMcaPhysics.xas.XASClass import XASClass
from PyMca5.PyMcaPhysics.xas.XASClass import e2k, k2e
from est.core.process.process import _input_desc
from est.core.process.process import _output_desc
from est.core.process.process import Process
from est.core.process.process import _NexusDatasetDef
from est.core.types import XASObject, Spectrum

_logger = logging.getLogger(__name__)


def process_spectr_exafs(
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
    _logger.debug("start exafs on spectrum (%s, %s)" % (spectrum.x, spectrum.y))
    if spectrum.energy is None or spectrum.mu is None:
        _logger.error(
            "Energy and or Mu is/are not specified, unable to " "compute exafs"
        )
        return None, None
    pymca_xas = XASClass()
    pymca_xas.setSpectrum(energy=spectrum.energy, mu=spectrum.mu)
    if configuration is not None:
        pymca_xas.setConfiguration(configuration)
    assert "NormalizedBackground" in spectrum

    if (
        "NormalizedBackground" not in spectrum
        or spectrum["NormalizedBackground"] is None
    ):
        _logger.warning("spectrum has not been normalized, will not process exafs")
        return None, None

    e0 = pymca_xas.calculateE0()
    ddict = spectrum.to_dict()
    ddict["Energy"] = pymca_xas._energy
    ddict["Mu"] = pymca_xas._mu
    cleanMu = pymca_xas._mu - ddict["NormalizedBackground"]
    kValues = e2k(pymca_xas._energy - e0)

    ddict.update(pymca_xas.postEdge(kValues, cleanMu))

    dataSet = numpy.zeros((cleanMu.size, 2), numpy.float)
    dataSet[:, 0] = kValues
    dataSet[:, 1] = cleanMu

    # exafs normalization
    exafs = (cleanMu - ddict["PostEdgeB"]) / ddict["PostEdgeB"]
    ddict["EXAFSEnergy"] = k2e(kValues)
    ddict["EXAFSKValues"] = kValues
    ddict["EXAFSSignal"] = cleanMu
    if ddict["KWeight"]:
        exafs *= pow(kValues, ddict["KWeight"])
    ddict["EXAFSNormalized"] = exafs

    if callbacks:
        for callback in callbacks:
            callback()

    res_spectrum = Spectrum.from_dict(ddict=ddict)

    def get_output(original_spec, res_spec):
        if overwrite:
            original_spec.update(res_spec)
            return original_spec
        else:
            return res_spec

    if output is not None:
        assert output_dict is not None
        output[output_dict[spectrum]] = get_output(spectrum, res_spectrum)

    return configuration, get_output(spectrum, res_spectrum)


def pymca_exafs(xas_obj):
    """

    :param xas_obj: object containing the configuration and spectra to process
    :type: Union[XASObject, dict]
    :return: spectra dict
    :rtype: XASObject
    """
    exafs_obj = PyMca_exafs()
    return exafs_obj.process(xas_obj=xas_obj)


_USE_MULTIPROCESSING_POOL = False
# note: we cannot use multiprocessing pool with pypushflow for now.


class PyMca_exafs(Process):
    """Process spectra for exafs and get information about the processing
    advancement"""

    inputs = [
        _input_desc(name="xas_obj", type=XASObject, handler="process", doc=""),
    ]

    outputs = [
        _output_desc(name="xas_obj", type=XASObject, doc=""),
    ]

    def __init__(self):
        Process.__init__(self, name="exafs")

    def set_properties(self, properties):
        if "_pymcaSettings" in properties:
            self.setConfiguration(properties["_pymcaSettings"])

    def process(self, xas_obj):
        _xas_obj = self.getXasObject(xas_obj=xas_obj)
        if self._settings:
            _xas_obj.configuration["EXAFS"] = self._settings

        self._advancement.reset(max_=_xas_obj.n_spectrum)
        self._advancement.startProcess()
        self._pool_process(xas_obj=_xas_obj)
        self._advancement.endProcess()
        self.register_process(
            _xas_obj,
            data_keys=(
                _NexusDatasetDef("EXAFSKValues"),
                _NexusDatasetDef("EXAFSSignal"),
            ),
        )
        return _xas_obj

    def _pool_process(self, xas_obj):
        assert isinstance(xas_obj, XASObject)
        if not _USE_MULTIPROCESSING_POOL:
            for spectrum in xas_obj.spectra.data.flat:
                assert "NormalizedBackground" in spectrum
                process_spectr_exafs(
                    spectrum=spectrum,
                    configuration=xas_obj.configuration,
                    callbacks=self.callbacks,
                    overwrite=True,
                )
                assert "EXAFSKValues" in spectrum
        else:
            from multiprocessing import Manager

            manager = Manager()
            output_dict = {}
            res_list = manager.list()
            for i_spect, spect in enumerate(xas_obj.spectra):
                res_list.append(None)
                output_dict[spect] = i_spect

            with multiprocessing.Pool(5) as p:
                partial_ = functools.partial(
                    process_spectr_exafs,
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
        return "exafs calculation"

    def program_version(self):
        import PyMca5

        return PyMca5.version()

    def program_name(self):
        return "pymca_exafs"

    __call__ = process


if __name__ == "__main__":
    import sys
    import yaml

    xas_object_yaml_file = sys.argv[1]
    _logger.debug("Load xas object from {}".format(xas_object_yaml_file))
    with open(xas_object_yaml_file, "r") as file:
        ddict = yaml.load(file)["input_data"]
        xas_object = XASObject.from_dict(ddict)
    print("******* do exafs ********")
    res_xas_object = pymca_exafs(xas_obj=xas_object)
    res_xas_object._create_saving_pt()

    # dump resulting object
    with open(xas_object_yaml_file, "w") as file:
        yaml.dump({"input_data": res_xas_object.to_dict()}, file)

    # dump resulting object into output_normalization file
    with open("output_exafs.yaml", "w") as file:
        yaml.dump({"input_data": res_xas_object.to_dict()}, file)
