# -*- coding: utf-8 -*-
"""
Interface for accessing a Channel in a HSDC file.

"""

from ctypes import byref, c_double, c_int, c_long, POINTER
import numpy as np
from .base import Channel
from .. import tools
from ..constants import METRIC, RAW, VOLTS
from ..dll import _np_double
from ..structures import XYCurve
from ..tools import constant_property


class HSDCChannel(Channel):
    """HSDC channel interface."""
    def __init__(self, file, i_chan):
        """Creates the HSDCChannel object.

        This object corresponds to the i_chan channel of the ChannelFile
        file.
        """
        super(HSDCChannel, self).__init__(file, i_chan)

    @constant_property
    def HSDC_rate(self):
        """HSDC rate."""
        HSDC_rate = c_double()
        self.file._dll_get("HsdcRate", self.i_chan, byref(HSDC_rate))
        if not HSDC_rate.value:
            raise RuntimeError("HSDC rate appears to be nul.")
        return HSDC_rate.value

    @constant_property
    def number_of_points_per_curve(self):
        """Number of points per curve."""
        max_data_size = c_long()  # May be c_int
        self.file._dll_get("NumberOfPointsPerCurve", self.i_chan,
                           byref(max_data_size))
        return max_data_size.value

    def get_HSDC_data(self, unit_type):
        """Return HSDC data.

        unit_type: unit type: METRIC, VOLTS, or RAW

        Return a numpy array with the data.
        """
        tools.check_unit_type(unit_type, (RAW, METRIC, VOLTS))
        max_data_size = self.number_of_points_per_curve
        actual_data_size = c_int()

        # create arrays of doubles
        data = np.zeros(max_data_size, np.double)

        argtypes = [c_int, _np_double, c_int, POINTER(c_int)]

        self.file._dll_get(
            "HSDC" + unit_type + "ForceCurveData", self.i_chan, data,
            max_data_size, byref(actual_data_size), argtypes=argtypes)
        return data

    def create_HSDC_time_plot(self, unit_type):
        """Create a HSDC Time Plot.

        unit_type: unit type: METRIC, VOLTS, or RAW

        Return data (XYCurve) and ax_properties (dict with title,
        xlabel, and ylabel).
        """
        dt = 1/self.HSDC_rate
        y_data = self.get_HSDC_data(unit_type)
        npts = len(y_data)
        x_data = np.linspace(0, dt*npts, npts)

        type_desc = self.data_type_desc
        scale_units = self.get_scale_unit(unit_type)
        ax_properties = {
            "title": "HSDC: {}".format(type_desc),
            "xlabel": "Time (ms)",
            "ylabel": u"{} ({})".format(type_desc, scale_units)
        }
        return XYCurve(x_data, y_data), ax_properties
