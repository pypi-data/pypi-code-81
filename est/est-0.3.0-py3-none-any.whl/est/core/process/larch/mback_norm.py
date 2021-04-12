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
"""wrapper to the larch mback process"""

from est.core.types import Spectrum, XASObject
from est.core.process.process import Process
from est.core.process.process import _NexusDatasetDef
from est.core.process.process import _input_desc
from est.core.process.process import _output_desc
from larch.xafs.mback import mback_norm
from larch.xafs.pre_edge import preedge
import multiprocessing
import functools
import logging

_logger = logging.getLogger(__name__)

_DEBUG = True
if _DEBUG:
    from larch.symboltable import Group


def process_spectr_mback_norm(
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
    _logger.debug("start mback_norm on spectrum (%s, %s)" % (spectrum.x, spectrum.y))
    assert isinstance(spectrum, Spectrum)
    if not hasattr(spectrum, "norm"):
        _logger.error(
            "spectrum doesn't have norm. Maybe you meed to compute "
            "pre_edge first? Unable to compute mback_norm."
        )
        return None, None
    if not hasattr(spectrum, "pre_edge"):
        _logger.error(
            "spectrum doesn't have norm. Maybe you meed to compute "
            "pre_edge first? Unable to compute mback_norm."
        )
        return None, None

    _conf = configuration
    if "mback_norm" in _conf:
        _conf = _conf["mback_norm"]
    opts = {}

    if _DEBUG is True:
        assert isinstance(spectrum, Group)
    if overwrite:
        _spectrum = spectrum
    else:
        _spectrum = Spectrum().load_frm_dict(spectrum.to_dict())
    # TODO: computing each time preedge should be avoidable
    pre_edge_details = preedge(_spectrum.energy, _spectrum.mu)
    for opt_name in (
        "z",
        "edge",
        "e0",
        "pre1",
        "pre2",
        "norm1",
        "norm2",
        "nnorm",
        "nvict",
    ):
        if opt_name in _conf:
            opts[opt_name] = _conf[opt_name]
        elif pre_edge_details is not None and opt_name in pre_edge_details:
            opts[opt_name] = pre_edge_details[opt_name]

    mback_norm(_spectrum, group=_spectrum, **opts)
    if callbacks:
        for callback in callbacks:
            callback()
    return configuration, _spectrum


def larch_mback_norm(xas_obj):
    """

    :param xas_obj: object containing the configuration and spectra to process
    :type: Union[XASObject, dict]
    :return: spectra dict
    :rtype: XASObject
    """
    mback_obj = Larch_mback_norm()
    return mback_obj.process(xas_obj=xas_obj)


_USE_MULTIPROCESSING_POOL = False
# note: we cannot use multiprocessing pool with pypushflow for now.


class Larch_mback_norm(Process):

    inputs = [
        _input_desc(name="xas_obj", type=XASObject, handler="process", doc=""),
    ]

    outputs = [
        _output_desc(name="xas_obj", type=XASObject, doc=""),
    ]

    def __init__(self):
        Process.__init__(self, name="mback_norm")

    def set_properties(self, properties):
        if "_larchSettings" in properties:
            self._settings = properties["_larchSettings"]

    def process(self, xas_obj):
        _xas_obj = self.getXasObject(xas_obj=xas_obj)
        if self._settings:
            _xas_obj.configuration["mback_norm"] = self._settings

        self._advancement.reset(max_=_xas_obj.n_spectrum)
        self._advancement.startProcess()
        self._pool_process(xas_obj=_xas_obj)
        self._advancement.endProcess()
        data_keys = [
            _NexusDatasetDef("mback_mu"),
            _NexusDatasetDef("norm_mback"),
        ]
        if _xas_obj.n_spectrum > 0 and hasattr(_xas_obj.spectra[0], "edge_step"):
            data_keys += ["norm"]
        self.register_process(_xas_obj, data_keys=data_keys)
        return _xas_obj

    def _pool_process(self, xas_obj):
        assert isinstance(xas_obj, XASObject)
        if not _USE_MULTIPROCESSING_POOL:
            for spectrum in xas_obj.spectra:
                process_spectr_mback_norm(
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

            with multiprocessing.Pool(5) as p:
                partial_ = functools.partial(
                    process_spectr_mback_norm,
                    configuration=xas_obj.configuration,
                    callback=self._advancement.increaseAdvancement,
                    overwrite=False,
                    output=res_list,
                    output_dict=output_dict,
                )
                p.map(partial_, xas_obj.spectra)

            # then update local spectrum
            for spectrum, res in zip(xas_obj.spectra, res_list):
                spectrum.update(res)

    def definition(self):
        return "mback norm calculation"

    def program_version(self):
        import larch.version

        return larch.version.version_data()["larch"]

    def program_name(self):
        return "larch_mback_norm"

    __call__ = process
