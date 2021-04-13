# -*- coding: utf-8 -*-
"""
Interface for Force Volume Hold Curves channels

"""

from ctypes import byref, c_double, c_int
import numpy as np
from .force_volume_curves import ForceVolumeCurvesChannel
from .hold_curve import HoldCurveChannel
from .. import tools
from ..constants import METRIC, RAW, VOLTS
from ..dll import _np_double
from ..structures import XYCurve
from ..tools import constant_property


class ForceVolumeHoldCurvesChannels(ForceVolumeCurvesChannel,
                                    HoldCurveChannel):
    """docstring for ForceVolumeHoldCurvesChannels"""
    def __init__(self, file, i_chan):
        """Create the ForceVolumeHoldCurvesChannel object.

        This object corresponds to the i_chan channel of the file file.
        """
        super(ForceVolumeHoldCurvesChannels, self).__init__(file, i_chan)

    @constant_property
    def number_of_hold_points_per_curve(self):
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

    def get_force_hold_data(self, i_curve, unit_type):
        """Return force hold curve data.

        i_curve: index of the curve, 0-based indexing
        unit_type: unit type: METRIC, VOLTS, or RAW
        """
        tools.check_unit_type(unit_type, (RAW, METRIC, VOLTS))
        n_hold_pts = self.number_of_hold_points_per_curve

        # create array of doubles
        hold = np.zeros(n_hold_pts, np.double)

        argtypes = [c_int, c_int, _np_double]

        self.file._dll_get("ForceVolume" + unit_type + "HoldData", self.i_chan,
                           i_curve, hold, argtypes=argtypes)
        return hold

    def create_force_hold_time_plot(self, i_curve, unit_type):
        """Create a Force Hold Time Plot.

        i_curve: index of the curve, 0-based indexing
        unit_type: unit type: METRIC, VOLTS, or RAW

        Return data (XYCurve) and ax_properties (dict with title,
        xlabel, and ylabel).
        """
        tools.check_unit_type(unit_type, (RAW, METRIC, VOLTS))

        y = self.get_force_hold_data(i_curve, unit_type)
        hold_len = len(y)

        type_desc = self.data_type_desc
        scale_unit = self.get_scale_unit(unit_type)

        hold_time_secs = self.force_hold_time
        # get hold data (metric units) for i_chan
        x = np.linspace(0, hold_time_secs, hold_len)

        data = XYCurve(x, y)
        ax_properties = {
            "title": "FV Hold Data {} vs. Time".format(type_desc),
            "xlabel": "Time (s)",
            "ylabel": u"{} ({})".format(type_desc, scale_unit)
        }

        return data, ax_properties

    def create_force_time_plot(self, i_curve, unit_type):
        """Create a Force Time Plot.

        unit_type: unit type: METRIC, VOLTS, FORCE or RAW

        Return data (TraceRetrace with two XYCurve) and ax_properties
        (dict with title, xlabel, and ylabel).
        """
        return self._create_force_time_plot(
            unit_type,
            lambda ut: self.get_force_curve_data(i_curve, ut),
            lambda ut: self.get_force_hold_data(i_curve, ut))
