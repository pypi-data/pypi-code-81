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
from est.core.process.process import _NexusSpectrumDef, _NexusDatasetDef
from est.core.process.process import _input_desc
from est.core.process.process import _output_desc
from est.core.utils.symbol import MU_CHAR
from larch.xafs.pre_edge import pre_edge
import multiprocessing
import functools
import logging

_logger = logging.getLogger(__name__)

_DEBUG = True
if _DEBUG:
    from larch.symboltable import Group


def process_spectr_pre_edge(
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
    :param callbacks: callbacks to execute.
    :param output: list to store the result, needed for pool processing
    :type: multiprocessing.manager.list
    :param output_dict: key is: input spectrum, value is index in the output
                        list.
    :type: dict
    :return: processed spectrum
    :rtype: tuple (configuration, spectrum)
    """
    _logger.debug("start pre_edge on spectrum (%s, %s)" % (spectrum.x, spectrum.y))
    assert isinstance(spectrum, Spectrum)
    if spectrum.energy is None or spectrum.mu is None:
        _logger.error(
            "Energy and or Mu is/are not specified, unable to " "compute pre edge"
        )
        return None, None
    _conf = configuration
    if "pre_edge" in _conf:
        _conf = _conf["pre_edge"]
    opts = {}
    for opt_name in (
        "z",
        "edge",
        "e0",
        "pre1",
        "pre2",
        "norm1",
        "nnorm",
        "nvict",
        "step",
        "make_flat",
        "norm2",
        "order",
        "leexiang",
        "tables",
        "fit_erfc",
        "make_flat",
    ):
        if opt_name in _conf:
            opts[opt_name] = _conf[opt_name]

    if _DEBUG is True:
        assert isinstance(spectrum, Group)
    if overwrite:
        _spectrum = spectrum
    else:
        _spectrum = Spectrum().load_frm_dict(spectrum=spectrum)

    pre_edge(_spectrum, group=_spectrum, **opts)
    if callbacks:
        for callback in callbacks:
            callback()

    return configuration, _spectrum


def larch_pre_edge(xas_obj):
    """

    :param xas_obj: object containing the configuration and spectra to process
    :type: Union[XASObject, dict]
    :return: spectra dict
    :rtype: XASObject
    """
    mback_obj = Larch_pre_edge()
    return mback_obj.process(xas_obj=xas_obj)


_USE_MULTIPROCESSING_POOL = False
# note: we cannot use multiprocessing pool with pypushflow for now.


class Larch_pre_edge(Process):

    inputs = [
        _input_desc(name="xas_obj", type=XASObject, handler="process", doc=""),
    ]

    outputs = [
        _output_desc(name="xas_obj", type=XASObject, doc=""),
    ]

    def __init__(self):
        Process.__init__(self, name="pre_edge")

    def set_properties(self, properties):
        if "_larchSettings" in properties:
            self._settings = properties["_larchSettings"]

    def process(self, xas_obj):
        _xas_obj = self.getXasObject(xas_obj=xas_obj)
        if self._settings:
            _xas_obj.configuration["pre_edge"] = self._settings

        self._advancement.reset(max_=_xas_obj.n_spectrum)
        self._advancement.startProcess()
        self._pool_process(xas_obj=_xas_obj)
        self._advancement.endProcess()
        self.register_process(
            _xas_obj,
            data_keys=(
                _NexusDatasetDef(
                    "flat", units="{}(E)".format(MU_CHAR), units_latex="\mu(E)"
                ),
                _NexusDatasetDef("dmude"),
                _NexusDatasetDef("edge_step_poly"),
                _NexusDatasetDef("norm"),
                _NexusDatasetDef("norm_area"),
                _NexusDatasetDef("post_edge"),
                _NexusDatasetDef("pre_edge_details"),
                _NexusDatasetDef("e0", "eV"),
                _NexusDatasetDef(
                    "Mu", units="{}(E)".format(MU_CHAR), units_latex="\mu(E)"
                ),
                _NexusDatasetDef("energy", "eV"),
                _NexusDatasetDef(
                    "mu_ref", units="{}(E)".format(MU_CHAR), units_latex="\mu(E)"
                ),
                _NexusDatasetDef("I0"),
                _NexusDatasetDef("I1"),
                _NexusDatasetDef("I2"),
            ),
            plots=(
                _NexusSpectrumDef(
                    signal="Mu",
                    axes=("energy",),
                    auxiliary_signals=None,
                    silx_style={"signal_scale_type": "linear"},
                    title="Mu",
                    title_latex="\mu",
                ),
                _NexusSpectrumDef(
                    signal="Mu",
                    axes=("energy",),
                    auxiliary_signals=("I0", "I1", "I2"),
                    silx_style={
                        "y_axis": ("I0", "I1", "I2"),
                        "signal_scale_type": "linear",
                    },
                ),
                _NexusSpectrumDef(
                    signal="Mu",
                    axes=("energy",),
                    auxiliary_signals=("mu_ref",),
                    silx_style={"signal_scale_type": "linear"},
                    title="Mu vs Mu ref",
                    title_latex="\mu \quad vs \quad \mu_{ref}",
                ),
                _NexusSpectrumDef(
                    signal="flat",
                    axes=("energy",),
                    auxiliary_signals=None,
                    silx_style={"signal_scale_type": "linear"},
                    title="Mu flat",
                    title_latex="\mu_{flat}",
                ),
            ),
        )
        return _xas_obj

    def _pool_process(self, xas_obj):
        assert isinstance(xas_obj, XASObject)
        if not _USE_MULTIPROCESSING_POOL:
            for spectrum in xas_obj.spectra:
                process_spectr_pre_edge(
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
                    process_spectr_pre_edge,
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
        return "pre_edge calculation"

    def program_version(self):
        import larch.version

        return larch.version.version_data()["larch"]

    def program_name(self):
        return "larch_pre_edge"

    __call__ = process
