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
"""module for process base class"""

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "07/08/2019"


from .progress import Progress
from est.core.types import XASObject
from ..utils import extract_properties_from_dict
import logging
from collections import namedtuple
from typing import Iterable

_logger = logging.getLogger(__name__)


_input_desc = namedtuple("_input_desc", ["name", "type", "handler", "doc"])

_output_desc = namedtuple("_output_desc", ["name", "type", "doc"])


class _NexusSpectrumDef:
    """Util function to define a Nexus plot"""

    def __init__(
        self,
        signal,
        axes,
        auxiliary_signals,
        silx_style=None,
        title=None,
        title_latex=None,
    ):
        self.__signal = None
        self.__axes = None
        self.__auxiliary_signals = None
        self.__title = None
        self.__title_latex = None
        self.__silx_style = silx_style

        self.signal = signal
        self.axes = axes
        self.auxiliary_signals = auxiliary_signals
        self.title = title

    @property
    def signal(self):
        return self.__signal

    @signal.setter
    def signal(self, signal):
        if not isinstance(signal, str):
            raise TypeError("signal should be an instance of str")
        else:
            self.__signal = signal

    @property
    def axes(self):
        return self.__axes

    @axes.setter
    def axes(self, axes):
        if not isinstance(axes, tuple):
            raise TypeError("axes should be an instance of tuple")
        else:
            self.__axes = axes

    @property
    def auxiliary_signals(self):
        return self.__auxiliary_signals

    @auxiliary_signals.setter
    def auxiliary_signals(self, auxiliary_signals):
        if not isinstance(auxiliary_signals, (tuple, type(None))):
            raise TypeError("auxiliary_signals should be an instance of tuple")
        else:
            self.__auxiliary_signals = auxiliary_signals

    @property
    def silx_style(self):
        if self.__silx_style is None:
            return {}
        else:
            return self.__silx_style

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        if not isinstance(title, (str, type(None))):
            raise TypeError("`title` should be an instance of str or None")
        else:
            self.__title = title

    @property
    def title_latex(self):
        return self.__title_latex

    @title.setter
    def title_latex(self, title):
        if not isinstance(title, (str, type(None))):
            raise TypeError("`title` should be an instance of str or None")
        else:
            self.__title_latex = title


class _NexusDatasetDef:
    """Util function to define a Nexus plot"""

    def __init__(self, name: str, units=None, units_latex=None):
        self.__name = None
        self.__units = None
        self.__units_latex = None

        assert isinstance(name, str)

        self.name = name
        self.units = units
        self.units_latex = units_latex

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise TypeError("name should be an instance of str")
        else:
            self.__name = name

    @property
    def units(self):
        return self.__units

    @units.setter
    def units(self, units):
        if not isinstance(units, (str, type(None))):
            raise TypeError("units should be an instance of str")
        else:
            self.__units = units

    @property
    def units_latex(self):
        return self.__units_latex

    @units_latex.setter
    def units_latex(self, units):
        if not isinstance(units, (str, type(None))):
            raise TypeError("units should be an instance of str")
        else:
            self.__units_latex = units

    @property
    def attrs(self):
        attrs = {}
        if self.units is not None:
            attrs.update({"units": self.units})
        if self.units_latex is not None:
            attrs.update({"units_latex": self.units_latex})
        return attrs

    def __str__(self):
        return self.name


class Process(object):
    def __init__(self, name):
        assert type(name) is str
        self._name = name
        self._advancement = Progress(name=name)
        self.__stop = False
        """flag to notice when a end of process is required"""
        self._settings = {}
        # configuration
        self._callbacks = []

    @property
    def name(self) -> str:
        return self._name

    def stop(self):
        self.__stop = True

    @property
    def advancement(self):
        return self._advancement

    @advancement.setter
    def advancement(self, advancement):
        assert isinstance(advancement, Progress)
        self._advancement = advancement

    @property
    def callbacks(self):
        return self._callbacks

    @staticmethod
    def getXasObject(xas_obj) -> XASObject:
        if isinstance(xas_obj, dict):
            _xas_obj = XASObject.from_dict(xas_obj)
        else:
            _xas_obj = xas_obj
        assert isinstance(_xas_obj, XASObject)
        if _xas_obj.n_spectrum > 0:
            _xas_obj.spectra.check_validity()
        assert isinstance(_xas_obj, XASObject)
        return _xas_obj

    def program_name(self) -> str:
        """Name of the program used for this processing"""
        raise NotImplementedError("Base class")

    def program_version(self) -> str:
        """version of the program used for this processing"""
        raise NotImplementedError("Base class")

    def definition(self) -> str:
        """definition of the process"""
        raise NotImplementedError("Base class")

    def getConfiguration(self) -> dict:
        """

        :return: configuration of the process
        :rtype: dict
        """
        if len(self._settings) > 0:
            return self._settings
        else:
            return None

    def setConfiguration(self, configuration: dict):
        # filter configuration from orange widgets
        if "__version__" in configuration:
            del configuration["__version__"]
        if "savedWidgetGeometry" in configuration:
            del configuration["savedWidgetGeometry"]
        if "savedWidgetGeometry" in configuration:
            del configuration["savedWidgetGeometry"]
        if "controlAreaVisible" in configuration:
            del configuration["controlAreaVisible"]

        self._settings = configuration

    def register_process(
        self, xas_obj: XASObject, data_keys: Iterable, plots: Iterable = tuple()
    ):
        """
        Store the current process in the linked h5 file if any,
        output data stored will be the one defined by the data_keys

        :param xas_obj: object for which we want to save the treatment
        :type: :class:`.XASObject`
        :param tuple data_keys: keys of the id to save
        :param plots:
        """
        if xas_obj.has_linked_file():
            _data = {}
            for data_info in data_keys:
                # data_info can be a string or an instance of _NexusDatasetDef
                key = str(data_info)
                relative_to = None
                use = "map_to"
                if key in (
                    "flat",
                    "fpp",
                    "f2",
                    "dmude",
                    "norm",
                    "norm_area",
                    "post_edge",
                    "bkg",
                    "energy",
                    "mback_mu",
                    "norm_mback",
                    "Energy",
                    "Mu",
                    "mu",
                    "NormalizedEnergy",
                    "NormalizedMu",
                    "NormalizedSignal",
                    "EXAFSKValues",
                    "EXAFSSignal",
                    "mu_ref",
                    "I0",
                    "I1",
                    "I2",
                ):
                    relative_to = "energy"
                    use = "map_to"
                elif key in (
                    "noise_savgol",
                    "noise_savgol_energy",
                ):
                    relative_to = "noise_savgol_energy"
                    use = "map_to"
                elif key in ("chir_re", "chir_im", "chir_mag", "r"):
                    relative_to = "r"
                    use = "map_to"
                elif key in ("masked_chir_mag", "masked_r"):
                    relative_to = "masked_r"
                    use = "map_to"
                elif key in ("ft.radius", "ft.intensity", "ft.imaginary"):
                    relative_to = "radius"
                    use = "_list_res_ft"
                elif key in ("masked_chi_weighted_k", "masked_k"):
                    relative_to = "masked_k"
                    use = "map_to"
                elif key in (
                    "chi",
                    "k",
                    "chi_weighted_k",
                ):
                    relative_to = "k"
                    use = "map_to"

                if use == "map_to":
                    if key == "norm_area":
                        continue
                    _data[key] = xas_obj.spectra.map_to(
                        data_info=key,
                        relative_to=relative_to,
                    )

                    # if we can display the result as a numpy.array 3d
                    try:
                        _data[key] = xas_obj.spectra.map_to(
                            data_info=key,
                            relative_to=relative_to,
                        )
                    except KeyError:
                        mess = "%s: unable to store %s, parameter not found" % (
                            self.name,
                            key,
                        )
                        _logger.error(mess)

                elif use == "_list_res_ft":
                    # for ft we are force to have a dictionary because it
                    # processing can end with a nan or with a numpy array.
                    # combining both would make us end up with a ndarray of
                    # object type
                    key_ = key.split(".")[-1]
                    res = {}
                    for spectrum in xas_obj.spectra:
                        x, y = spectrum.x, spectrum.y
                        res["_".join((str(x), str(y)))] = getattr(spectrum.ft, key_)
                    _data[key] = res
                else:
                    raise ValueError()
                if isinstance(data_info, _NexusDatasetDef):
                    for aname, avalue in data_info.attrs.items():
                        _data[(key, aname)] = avalue
            xas_obj.register_processing(process=self, results=_data, plots=plots)

    def addCallback(self, callback):
        self._callbacks.append(callback)

    def update_properties(self, properties):
        if properties is None:
            return
        if isinstance(properties, str):
            properties = extract_properties_from_dict(properties)
        self._settings.update(properties)
