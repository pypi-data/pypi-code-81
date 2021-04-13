# -*- coding: utf-8 -*-
"""
Common interface for opening all Nanoscope files.

"""

import ctypes
import numpy as np
from ctypes import byref, c_char_p, c_double, c_int

from .. import dll as _dll
from ..channels import Channel
from ..dll import _string_buffer
from ..tools import constant_property


class File(object):
    """Common file interface.

    You may open and close the file by yourself:
        file_ = File(filename)
        file_.open()
        ...
        file_.close()

    or use a with-statement:
        with File(filename) as file_:
            ...
    """
    def __init__(self, filename):
        """Create the File object."""
        super(File, self).__init__()
        self._filename = filename
        self._opened = False
        self._channels = dict()

    def __enter__(self):
        """Open the file, in a with-statement."""
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        """Close the file, in a with-statement."""
        self.close()

    def __getitem__(self, i_chan):
        """Return Channel i_chan.

        If out of range, raise an IndexError. Supports slicing.
        """
        if isinstance(i_chan, slice):
            r_start = 0 if i_chan.start is None else i_chan.start
            if r_start < 0:
                raise IndexError("Start index cannot be negative.")
            r_stop = (self.number_of_channels if i_chan.stop is None
                      else min(i_chan.stop, self.number_of_channels))
            r_step = 1 if i_chan.step is None else i_chan.step
            return [self._get_channel(i)
                    for i in range(r_start, r_stop, r_step)]
        return self._get_channel(i_chan)

    def __len__(self):
        """Return the number of channels in the file."""
        return self.number_of_channels

    def __iter__(self):
        """Return a generator so that file can be used in loops."""
        return (self[i] for i in range(self.number_of_channels))

    def _dll_get(self, arg_name, *args, **kwargs):
        """Execute the get function linked to the arg_name.

        That function must be part of the dll.
        """
        if not self._opened:
            raise RuntimeError("File must be open.")
        try:
            _dll._get(arg_name, *args, **kwargs)
        except RuntimeError:
            raise RuntimeError("Openend file does not match with {}."
                               "".format(type(self).__name__))

    def _get_channel(self, i_chan):
        """Return Channel i_chan.

        If out of range, raise an IndexError.
        """
        if i_chan not in self._channels.keys():
            if not (0 <= i_chan < self.number_of_channels):
                raise IndexError("i_chan out of range")
            self._channels[i_chan] = Channel(self, i_chan)
        return self._channels[i_chan]

    def open(self):
        """Open the file manually.

        To be called if not using a with-statement.
        The file has then to be closed by the close function.
        Raise an IOError if filename cannot be opened.
        """
        _dll._open(self._filename)
        self._opened = True

    def close(self):
        """Close the file manually."""
        _dll._close()
        self._opened = False

    @constant_property
    def number_of_channels(self):
        """Number of channels in the file"""
        number_of_channels = c_int()
        self._dll_get("NumberOfChannels", byref(number_of_channels))
        return number_of_channels.value

    @constant_property
    def channels_data_types_desc(self):
        """Tuple with the channel descriptions in order"""
        return tuple(self[i].data_type_desc
                     for i in range(self.number_of_channels))

    @constant_property
    def poisson_ratio(self):
        """Poisson ratio from header file (no units)"""
        poisson_ratio = c_double()
        self._dll_get("PoissonRatio", byref(poisson_ratio))
        return poisson_ratio.value

    @constant_property
    def tip_radius(self):
        """Tip radius from header file (in nm)"""
        tip_radius = c_double()
        self._dll_get("TipRadius", byref(tip_radius))
        return tip_radius.value

    @constant_property
    def spring_constant(self):
        """Spring constant of the cantilever"""
        spring_const = c_double()
        i_chan = 0  # default
        self._dll_get("ForceSpringConstant", i_chan, byref(spring_const))
        return spring_const.value

    @constant_property
    def half_angle(self):
        """Tip half angle (in radians)"""
        half_angle = c_double()
        self._dll_get("HalfAngle", byref(half_angle))
        return half_angle.value

    @constant_property
    def defl_sens(self):
        """Deflection sensitivity"""
        defl_sens = c_double()
        self._dll_get("DeflSens", byref(defl_sens))
        return defl_sens.value

    @constant_property
    def defl_sens_units(self):
        """Deflection sensitity units"""
        units = _string_buffer()
        self._dll_get("DeflSensUnits", units)
        return units.value.decode("latin-1")

    @constant_property
    def defl_limits(self):
        """Deflection limit & ~Lockin3LSADC1."""
        limit = c_double()
        limit2 = c_double()
        self._dll_get("DeflLimits", byref(limit), byref(limit2))
        return limit.value, limit2.value

    @constant_property
    def defl_limits_units(self):
        units = _string_buffer()
        units2 = _string_buffer()
        self._dll_get("DeflLimitsUnits", units, units2)
        return units.value.decode("latin-1"), units2.value.decode("latin-1")

    @constant_property
    def z_sens_units(self):
        """Z sensitivity units"""
        units = _string_buffer()
        i_chan = 0  # default
        self._dll_get("ZSensitivityUnits", i_chan, units)
        return units.value.decode("latin-1")

    @constant_property
    def x_y_offsets(self):
        """X Offset and Y Offset"""
        x_offset = c_double()
        y_offset = c_double()
        self._dll_get("XYOffsets", byref(x_offset), byref(y_offset))
        return x_offset.value, y_offset.value

    @constant_property
    def x_y_offsets_units(self):
        """X Offset Units and Y Offset Units"""
        x_offset_units = _string_buffer()
        y_offset_units = _string_buffer()
        self._dll_get("XYOffsetsUnits", byref(x_offset_units), byref(y_offset_units))
        return x_offset_units.value, y_offset_units.value
