# -*- coding: utf-8 -*-
"""
Common interface for accessing a channel in Nanoscope files.

"""

from ctypes import byref, c_double, c_char
from .. import tools
from ..constants import UNIT_TYPES
from ..dll import _string_buffer
from ..tools import constant_property


class Channel(object):
    """Common channel interface"""
    def __init__(self, file, i_chan):
        """Create the Channel object.

        This object corresponds to the i_chan channel of the file file.
        """
        super(Channel, self).__init__()
        self.file = file
        self.i_chan = i_chan

    def get_scale_unit(self, unit_type):
        """Scale unit corresponding to the unit_type.

        unit_type: unit type: METRIC, VOLTS, FORCE, RAW
        """
        tools.check_unit_type(unit_type, UNIT_TYPES)
        if not unit_type:
            return "LSB"
        scale_unit = _string_buffer()
        self.file._dll_get(unit_type + "DataScaleUnits", self.i_chan,
                           scale_unit)
        return scale_unit.value.decode("latin-1")

    @constant_property
    def data_type_desc(self):
        """Type description, as a unicode string."""
        type_desc = _string_buffer()
        self.file._dll_get("DataTypeDesc", self.i_chan, type_desc)
        return type_desc.value.decode("latin-1")

    @constant_property
    def spring_constant(self):
        """Spring constant of the cantilever."""
        spring_const = c_double()
        self.file._dll_get("ForceSpringConstant", self.i_chan,
                           byref(spring_const))
        return spring_const.value

    @constant_property
    def z_sens_units(self):
        """Z sensitivity units"""
        units = _string_buffer()
        self.file._dll_get("ZSensitivityUnits", self.i_chan, units)
        return units.value.decode("latin-1")

    @constant_property
    def z_scale_in_sw_units(self):
        """Raw to Metric ratio"""
        scale = c_double()
        self.file._dll_get("ZScaleInSwUnits", self.i_chan, byref(scale))
        return scale.value

    @constant_property
    def z_scale_in_hw_units(self):
        """Raw to Volts ratio"""
        scale = c_double()
        self.file._dll_get("ZScaleInHwUnits", self.i_chan, byref(scale))
        return scale.value

    def get_scaling_factor(self, is_metric):
        """Return Scaling Factor.

        Metric: Raw to Metric ratio
        Otherwise: Raw to Volts ration.
        """
        scale = c_double()
        self.file._dll_get("ScalingFactor", self.i_chan, byref(scale),
                           is_metric)
        return scale.value
