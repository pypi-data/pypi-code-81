# -*- coding: utf-8 -*-
"""
Interface for Nanoscope hold curve channels

"""

from ctypes import byref, c_double, c_int
import numpy as np
from .curve import CurveChannel
from .. import tools
from ..constants import METRIC, RAW, VOLTS
from ..dll import _np_double, _string_buffer
from ..structures import XYCurve
from ..tools import constant_property


class HoldCurveChannel(CurveChannel):
    """Hold Curve channel interface."""
    def __init__(self, file, i_chan):
        """Create the HoldCurveChannel object."""
        super(HoldCurveChannel, self).__init__(file, i_chan)

    @constant_property
    def number_of_hold_points(self):
        """Number of points in hold."""
        num_hold = c_int()
        self.file._dll_get("NumberOfHoldPoints", self.i_chan,
                           byref(num_hold))
        return num_hold.value

    @constant_property
    def force_hold_time(self):
        """Hold time (in secs)."""
        hold_time_secs = c_double()
        self.file._dll_get("ForceHoldTime", self.i_chan, byref(hold_time_secs))
        return hold_time_secs.value

    @constant_property
    def force_sweep_type(self):
        """Force sweep type description."""
        sweep = _string_buffer()
        self.file._dll_get("ForceSweepChannel", self.i_chan, sweep)
        return sweep.value.decode("latin-1")

    @constant_property
    def force_sweep_freq_range(self):
        """Force sweep frequency range (start, stop)."""
        start = c_double()
        stop = c_double()
        self.file._dll_get("ForceSweepFreqRange", self.i_chan, byref(start),
                           byref(stop))
        return start.value, stop.value

    def get_force_hold_data(self, unit_type):
        """Return force hold curve data.

        unit_type: unit type: METRIC, VOLTS, or RAW
        """
        tools.check_unit_type(unit_type, (RAW, METRIC, VOLTS))
        n_hold_pts = self.number_of_hold_points

        # create array of doubles
        hold = np.zeros(n_hold_pts, np.double)

        argtypes = [c_int, _np_double]

        self.file._dll_get("Force" + unit_type + "HoldData", self.i_chan,
                           hold, argtypes=argtypes)
        return hold

    def create_force_hold_time_plot(self, unit_type):
        """Create a Force Hold Time Plot.

        unit_type: unit type: METRIC, VOLTS, or RAW

        Return data (XYCurve) and ax_properties (dict with title,
        xlabel, and ylabel).
        """
        tools.check_unit_type(unit_type, (RAW, METRIC, VOLTS))

        y = self.get_force_hold_data(unit_type)
        hold_len = len(y)

        type_desc = self.data_type_desc
        scale_unit = self.get_scale_unit(unit_type)

        hold_time_secs = self.force_hold_time
        # get hold data (metric units) for i_chan
        x = np.linspace(0, hold_time_secs, hold_len)

        data = XYCurve(x, y)
        ax_properties = {
            "title": "Force Hold Data {} vs. Time".format(type_desc),
            "xlabel": "Time (s)",
            "ylabel": u"{} ({})".format(type_desc, scale_unit)
        }

        return data, ax_properties

    def create_force_time_plot(self, unit_type):
        """Create a Force Time Plot.

        unit_type: unit type: METRIC, VOLTS, FORCE or RAW

        Return data (TraceRetrace with two XYCurve) and ax_properties
        (dict with title, xlabel, and ylabel).
        """
        return self._create_force_time_plot(unit_type,
                                            self.get_force_curve_data,
                                            self.get_force_hold_data)
