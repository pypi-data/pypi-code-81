# -*- coding: utf-8 -*-
"""
Interface for Force Volume Curves channels.

"""

from ctypes import byref, c_double, c_int, c_long
import numpy as np
from .curve_maker import CurveMakerChannel
from .. import tools
from ..constants import UNIT_TYPES
from ..dll import _np_double
from ..structures import TraceRetrace
from ..tools import constant_property


class ForceVolumeCurvesChannel(CurveMakerChannel):
    """Force Volume Curves Channel interface."""
    def __init__(self, file, i_chan):
        """Create the ForceVolumeCurvesChannel object.

        This object corresponds to the i_chan channel of the file file.
        """
        super(ForceVolumeCurvesChannel, self).__init__(file, i_chan)

    @constant_property
    def number_of_points_per_curve(self):
        """Number of points per curve."""
        max_data_size = c_long()  # May be c_int
        self.file._dll_get("NumberOfPointsPerCurve", self.i_chan,
                           byref(max_data_size))
        return max_data_size.value

    @constant_property
    def number_of_force_curves(self):
        """Number of force curves in the file."""
        number_of_force_curves = c_int()
        self.file._dll_get("NumberOfForceCurves",
                           byref(number_of_force_curves))
        return number_of_force_curves.value

    def get_force_curve_data(self, i_curve, unit_type):
        """Return force volume force curve data.

        i_curve: index of the curve, 0-based indexing
        unit_type: unit type: METRIC, VOLTS, FORCE, RAW

        Returns a TraceRetrace object
        """
        tools.check_unit_type(unit_type, UNIT_TYPES)

        max_data_size = self.number_of_points_per_curve

        trace_len = c_int()
        retrace_len = c_int()

        # create arrays of doubles
        trace = np.zeros(max_data_size, np.double)
        retrace = np.zeros(max_data_size, np.double)

        argtypes = [c_int, c_int, _np_double, _np_double]

        self.file._dll_get(
            "ForceVolume" + unit_type + "ForceCurveData", self.i_chan, i_curve,
            trace, retrace, byref(trace_len), byref(retrace_len),
            max_data_size, argtypes=argtypes)

        trace_len = trace_len.value
        retrace_len = retrace_len.value

        trace = trace[trace_len-1::-1]  # revert trace
        retrace = retrace[:retrace_len]

        return TraceRetrace(trace, retrace)

    def create_force_time_plot(self, i_curve, unit_type):
        """Create a Force Time Plot.

        unit_type: unit type: METRIC, VOLTS, FORCE or RAW

        Return data (XYCurve) and ax_properties (dict with title,
        xlabel, and ylabel).
        """
        return self._create_force_time_plot(
            unit_type,
            lambda ut: self.get_force_curve_data(i_curve, ut))

    def create_force_z_plot(self, i_curve, unit_type):
        """Create a Force Z Plot.

        unit_type: unit type: METRIC, VOLTS, FORCE or RAW

        Return data (TraceRetrace with two XYCurve) and ax_properties
        (dict with title, xlabel, and ylabel).
        """
        return self._create_force_z_plot(
            unit_type,
            lambda ut: self.get_force_curve_data(i_curve, ut))
