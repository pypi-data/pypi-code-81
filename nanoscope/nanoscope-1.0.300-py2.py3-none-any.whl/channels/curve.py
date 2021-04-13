# -*- coding: utf-8 -*-
"""
Interface for Nanoscope curve channels.

"""

from ctypes import byref, c_double, c_long, c_int
import numpy as np
from .curve_maker import CurveMakerChannel
from .. import tools
from ..constants import UNIT_TYPES
from ..dll import _np_double
from ..structures import TraceRetrace
from ..tools import constant_property


class CurveChannel(CurveMakerChannel):
    """Curve channel interface"""
    def __init__(self, file, i_chan):
        """Create the CurveChannel object.

        This object corresponds to the i_chan channel of the file file.
        """
        super(CurveChannel, self).__init__(file, i_chan)

    @constant_property
    def number_of_trace_points(self):
        """Number of points in trace curve."""
        num_trace = c_long()
        self.file._dll_get("NumberOfTracePoints", self.i_chan,
                           byref(num_trace))
        return num_trace.value

    @constant_property
    def number_of_retrace_points(self):
        """Number of points in retrace."""
        num_retrace = c_long()
        self.file._dll_get("ForceSamplesPerLine", self.i_chan,
                           byref(num_retrace))
        return num_retrace.value

    def get_force_curve_data(self, unit_type):
        """Return the data of the force curve.

        unit_type: unit type: METRIC, VOLTS, FORCE or RAW
        """
        tools.check_unit_type(unit_type, UNIT_TYPES)

        # get number of (re)trace points
        num_trace = self.number_of_trace_points
        num_retrace = self.number_of_retrace_points

        # create arrays of doubles
        trace = np.zeros(num_trace, np.double)
        retrace = np.zeros(num_retrace, np.double)

        argtypes = [c_int, _np_double, _np_double]
        self.file._dll_get("ForceCurve" + unit_type + "Data",
                           self.i_chan, trace, retrace,
                           argtypes=argtypes)

        trace = trace[::-1]  # reverting trace

        return TraceRetrace(trace, retrace)

    def create_force_time_plot(self, unit_type):
        """Create a Force Time Plot.

        unit_type: unit type: METRIC, VOLTS, FORCE or RAW

        Return data (XYCurve) and ax_properties (dict with title,
        xlabel, and ylabel).
        """
        return self._create_force_time_plot(unit_type,
                                            self.get_force_curve_data)

    def create_force_z_plot(self, unit_type):
        """Create a Force Z Plot.

        unit_type: unit type: METRIC, VOLTS, FORCE or RAW

        Return data (TraceRetrace with two XYCurve) and ax_properties
        (dict with title, xlabel, and ylabel).
        """
        return self._create_force_z_plot(unit_type,
                                         self.get_force_curve_data)
