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
__date__ = "14/12/2020"


import numpy
from typing import Union
from typing import Iterable
import logging
from est.units import units
from est.units import ur
from est.units import convert_to as convert_unit_to
import pint

_logger = logging.getLogger(__name__)
try:
    import larch
except ImportError:

    class _Spectrum_Base:
        pass

    _has_larch = False
    _logger.info("larch not found")
else:
    from larch.symboltable import Group as LarchGroup

    class _Spectrum_Base(LarchGroup):
        pass

    from est.core.utils import larchutils

    _has_larch = True
    _logger.info("larch found")


class Spectrum(_Spectrum_Base):
    """
    Core object to be used to store larch and pymca results.

    Larch is using 'Group' to store the results and adds members to this group
    according to the different treatment. Pymca is using a dictionary to store
    the results.

    This class has to adpat to both behaviors and the different naming
    convention as well.

    :param numpy.ndarray (1D) energy: beam energy
    :param numpy.ndarray (1D) mu: beam absorption
    :param int x: x index on the spectra
    :param int y: y index on the spectra
    """

    _MU_KEY = "Mu"

    _ENERGY_KEY = "Energy"

    _NORMALIZED_MU_KEY = "NormalizedMu"

    _NORMALIZED_ENERGY_KEY = "NormalizedEnergy"

    _NORMALIZED_SIGNAL_KEY = "NormalizedSignal"

    _EXAFS_SIGNAL_KEY = "EXAFSSignal"

    _EXAFS_KVALUES_KEY = "EXAFSKValues"

    _FT_KEY = "FT"

    _EDGE_KEY = "Edge"

    _NORMALIZED_BACKGROUND_KEY = "NormalizedBackground"

    _X_POS_KEY = "XPos"

    _Y_POS_KEY = "YPos"

    def __init__(
        self,
        energy: Union[None, numpy.ndarray] = None,
        mu: Union[None, numpy.ndarray] = None,
        x: Union[None, int] = None,
        y: Union[None, int] = None,
    ):
        super().__init__()
        if energy is not None:
            assert isinstance(energy, (numpy.ndarray, pint.Quantity))
            if isinstance(energy, numpy.ndarray):
                energy = energy * ur.eV

        self.__x = x
        self.__y = y

        # properties
        self.energy = energy
        self.mu = mu
        self.__chi = None
        self.__k_values = None
        self.__normalized_mu = None
        self.__normalized_energy = None
        self.__pre_edge = None
        self.__post_edge = None
        # unable to create a property top level since larch is using
        # getattr(group, 'edge', None). Or edge should be initialized to
        # something != None that we don't want
        self.__e0 = None
        self.__noise_savgol = None
        self.__norm_noise_savgol = None
        self.__other_parameters = {}
        self.ft = {}

        self.__key_mapper = {
            self._MU_KEY: self.__class__.mu,
            self._ENERGY_KEY: self.__class__.energy,
            self._NORMALIZED_MU_KEY: self.__class__.normalized_mu,
            self._NORMALIZED_ENERGY_KEY: self.__class__.normalized_energy,
            self._NORMALIZED_SIGNAL_KEY: self.__class__.post_edge,
            self._NORMALIZED_BACKGROUND_KEY: self.__class__.pre_edge,
            self._FT_KEY: self.__class__.ft,
            self._EDGE_KEY: self.__class__.e0,
            self._EXAFS_SIGNAL_KEY: self.__class__.chi,
            self._EXAFS_KVALUES_KEY: self.__class__.k,
        }

    @property
    def energy(self) -> Union[None, numpy.ndarray]:
        """

        :note: cannot be with unit because use directly by xraylarch and pymca
        """
        return self.__energy

    @energy.setter
    @units(energy="eV")
    def energy(self, energy):
        if isinstance(energy, pint.Quantity):
            self.__energy = energy.m_as(ur.eV)
        else:
            self.__energy = energy

    @property
    def mu(self) -> Union[None, numpy.ndarray]:
        return self.__mu

    @mu.setter
    def mu(self, mu: numpy.ndarray):
        assert isinstance(mu, numpy.ndarray) or mu is None
        self.__mu = mu

    @property
    def x(self) -> Union[None, int]:
        return self.__x

    @property
    def y(self) -> Union[None, int]:
        return self.__y

    @property
    def chi(self) -> Union[None, numpy.ndarray]:
        return self.__chi

    @chi.setter
    def chi(self, chi: numpy.ndarray):
        self.__chi = chi

    @property
    def k(self) -> Union[None, numpy.ndarray]:
        return self.__k_values

    @k.setter
    def k(self, k: numpy.ndarray):
        self.__k_values = k

    @property
    def normalized_mu(self) -> Union[None, numpy.ndarray]:
        return self.__normalized_mu

    @normalized_mu.setter
    def normalized_mu(self, mu: numpy.ndarray):
        assert isinstance(mu, numpy.ndarray) or mu is None
        self.__normalized_mu = mu

    @property
    def norm(self) -> Union[None, numpy.ndarray]:
        # this alias is needed for larch
        return self.__normalized_mu

    @norm.setter
    def norm(self, value: numpy.ndarray):
        # this alias is needed for larch
        self.__normalized_mu = value

    @property
    def normalized_energy(self) -> Union[None, numpy.ndarray]:
        return self.__normalized_energy

    @normalized_energy.setter
    def normalized_energy(self, energy: Union[numpy.ndarray, pint.Quantity]):
        assert isinstance(energy, (numpy.ndarray, pint.Quantity)) or energy is None
        self.__normalized_energy = energy

    @property
    def pre_edge(self) -> Union[None, numpy.ndarray]:
        return self.__pre_edge

    @pre_edge.setter
    def pre_edge(self, value: numpy.ndarray):
        self.__pre_edge = value

    @property
    def _edge(self) -> Union[None, numpy.ndarray]:
        return self.edge

    @_edge.setter
    def _edge(self, value: numpy.ndarray):
        self.edge = value

    @property
    def post_edge(self) -> Union[None, numpy.ndarray]:
        return self.__post_edge

    @post_edge.setter
    def post_edge(self, value: numpy.ndarray):
        self.__post_edge = value

    @property
    def e0(self) -> Union[None, numpy.ndarray]:
        return self.__e0

    @e0.setter
    def e0(self, e0: numpy.ndarray):
        self.__e0 = e0

    @property
    def noise_savgol(self):
        return self.__noise_savgol

    @noise_savgol.setter
    def noise_savgol(self, values):
        self.__noise_savgol = values

    @property
    def norm_noise_savgol(self):
        return self.__norm_noise_savgol

    @norm_noise_savgol.setter
    def norm_noise_savgol(self, values):
        self.__norm_noise_savgol = values

    @property
    def ft(self):
        return self.__ft

    @ft.setter
    def ft(self, ft):
        if isinstance(ft, _FT):
            self.__ft = ft
        else:
            self.__ft = _FT(ddict=ft)

    @property
    def shape(self) -> tuple:
        _energy_len = 0
        if self.__energy is not None:
            _energy_len = len(self.__energy)
        _mu_len = 0
        if self.__mu is not None:
            _mu_len = len(self.__mu)

        return (_energy_len, _mu_len)

    def extra_keys(self) -> tuple:
        return tuple(self.__other_parameters.keys())

    def __getitem__(self, key):
        """Need for pymca compatibility"""
        if key in self.__key_mapper:
            return self.__key_mapper[key].fget(self)
        else:
            if _has_larch and key in self._members():
                return self._members()[key]
            else:
                return self.__other_parameters[key]

    def __setitem__(self, key, value):
        """Need for pymca compatibility"""
        assert key
        if key in self.__key_mapper:
            self.__key_mapper[key].fset(self, value)
        else:
            self.__other_parameters[key] = value

    def __contains__(self, item):
        return item in self.__key_mapper or item in self.__other_parameters

    def load_frm_dict(self, ddict: dict):
        assert isinstance(ddict, dict)

        def value_is_none(value):
            if hasattr(value, "decode"):
                value = value.decode("UTF-8")

            if isinstance(value, str):
                return value == "None"
            else:
                return value is None

        larch_ddict = {}
        if "_larch_grp_members" in ddict:
            if _has_larch is False:
                _logger.warning(
                    "larch is not installed but the Spectrum "
                    "requires it, won't be able to load data "
                    "relative to larch"
                )
            for key in ddict["_larch_grp_members"]:
                if hasattr(key, "decode"):
                    key = key.decode("UTF-8")
                larch_ddict[key] = None if value_is_none(ddict[key]) else ddict[key]
                del ddict[key]

        for key, value in ddict.items():
            if hasattr(value, "decode"):
                value = value.decode("UTF-8")
            self[key] = None if value_is_none(value) else value
        for key, value in larch_ddict.items():
            setattr(self, key, None if value_is_none(value) else value)
        return self

    @staticmethod
    def from_dict(ddict: dict):
        x_pos = None
        y_pos = None
        if Spectrum._X_POS_KEY in ddict:
            x_pos = ddict[Spectrum._X_POS_KEY]
        if Spectrum._Y_POS_KEY in ddict:
            y_pos = ddict[Spectrum._Y_POS_KEY]
        spectrum = Spectrum(x=x_pos, y=y_pos)
        return spectrum.load_frm_dict(ddict=ddict)

    def to_dict(self) -> dict:
        energy = convert_unit_to(self.energy, ur.eV)
        if energy is not None:
            energy = energy.m_as(ur.eV)
        res = {
            self._X_POS_KEY: self.x,
            self._Y_POS_KEY: self.y,
            self._MU_KEY: self.mu,
            self._ENERGY_KEY: energy,
            self._FT_KEY: self.ft.to_dict(),
            self._NORMALIZED_MU_KEY: "None"
            if self.normalized_mu is None
            else self.normalized_mu,
            self._NORMALIZED_ENERGY_KEY: "None"
            if self.normalized_energy is None
            else self.normalized_energy,
            self._NORMALIZED_SIGNAL_KEY: "None"
            if self.post_edge is None
            else self.post_edge,
            self._NORMALIZED_BACKGROUND_KEY: "None"
            if self.pre_edge is None
            else self.pre_edge,
            self._EDGE_KEY: "None" if self.e0 is None else self.e0,
            self._EXAFS_SIGNAL_KEY: "None" if self.chi is None else self.chi,
            self._EXAFS_KVALUES_KEY: "None" if self.k is None else self.k,
        }
        if _has_larch:
            res.update(self._getLarchGroupMenbers())
        res.update(self.__other_parameters)
        return res

    def _getLarchGroupMenbers(self):
        """Return larch group specific menbers"""

        assert _has_larch is True
        res = {}
        res["_larch_grp_members"] = list(self._members().keys())
        for key in self._members().keys():
            if isinstance(self[key], LarchGroup):
                res[key] = larchutils.group_to_dict(self[key])
            else:
                res[key] = getattr(self, key)
        return res

    def __str__(self):
        def add_info(str_, attr):
            assert hasattr(self, attr)
            sub_str = "- " + attr + ": " + str(getattr(self, attr)) + "\n"
            return str_ + sub_str

        main_info = ""
        for info in (
            "energy",
            "mu",
            "normalized_mu",
            "normalized_signal",
            "normalized_energy",
        ):
            main_info = add_info(str_=main_info, attr=info)

        def add_third_info(str_, key):
            sub_str = ("- " + key + ": " + str(self[key])) + "\n"
            return str_ + sub_str

        for key in self.__other_parameters:
            main_info = add_third_info(str_=main_info, key=key)
        return main_info

    def update(self, obj):
        """
        Update the contained values from the given obj.

        :param obj:
        :type obj: Union[XASObject, dict]
        """
        if isinstance(obj, Spectrum):
            _obj = obj.to_dict()
        else:
            _obj = obj
        assert isinstance(_obj, dict)
        for key, value in _obj.items():
            if isinstance(value, str) and value == "None":
                self[key] = None
            else:
                self[key] = value

    def get_missing_keys(self, keys: Iterable) -> tuple:
        """Return missing keys on the spectrum"""
        missing = []
        for key in keys:
            if key not in self or self[key] is None:
                missing.append(key)
        return tuple(missing)

    def keys(self) -> list:
        keys = list(self.__other_parameters.keys())
        keys += list(self.__key_mapper.keys())
        return keys

    def copy(self):
        return Spectrum().load_frm_dict(self.to_dict())

    def _force_indexes(self, x, y):
        """This is protected because it might change display and
        the indexes should be defined during Spectra or Spectrum construction
        once for all"""
        self.__x = x
        self.__y = y

    # def formula_results(self, formula):


class _FT(object):

    _RADIUS_KEY = "FTRadius"

    _INTENSITY_KEY = "FTIntensity"

    _IMAGINARY_KEY = "FTImaginary"

    def __init__(self, ddict):
        self.__radius = numpy.nan
        self.__intensity = numpy.nan
        self.__imaginary = numpy.nan
        self.__other_parameters = {}

        self.__key_mapper = {
            self._RADIUS_KEY: self.__class__.radius,
            self._INTENSITY_KEY: self.__class__.intensity,
            self._IMAGINARY_KEY: self.__class__.imaginary,
        }

        if ddict is not None:
            for key, values in ddict.items():
                self[key] = values

    @property
    def radius(self):
        return self.__radius

    @radius.setter
    def radius(self, radius):
        self.__radius = radius

    @property
    def intensity(self):
        return self.__intensity

    @intensity.setter
    def intensity(self, intensity):
        self.__intensity = intensity

    @property
    def imaginary(self):
        return self.__imaginary

    @imaginary.setter
    def imaginary(self, imaginery):
        self.__imaginary = imaginery

    def __getitem__(self, key):
        """Need for pymca compatibility"""
        if key in self.__key_mapper:
            return self.__key_mapper[key].fget(self)
        else:
            return self.__other_parameters[key]

    def __setitem__(self, key, value):
        """Need for pymca compatibility"""
        if key in self.__key_mapper:
            self.__key_mapper[key].fset(self, value)
        else:
            self.__other_parameters[key] = value

    def __contains__(self, item):
        return item in self.__key_mapper or item in self.__other_parameters

    def to_dict(self) -> dict:
        res = {
            self._RADIUS_KEY: self.radius,
            self._INTENSITY_KEY: self.intensity,
            self._IMAGINARY_KEY: self.imaginary,
        }
        res.update(self.__other_parameters)
        return res

    def get_missing_keys(self, keys: Iterable) -> tuple:
        """Return missing keys on the spectrum"""
        missing = []
        for key in keys:
            if key not in self:
                missing.append(key)
        return tuple(missing)
