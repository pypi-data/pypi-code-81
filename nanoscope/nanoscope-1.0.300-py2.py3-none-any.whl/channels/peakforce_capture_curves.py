# -*- coding: utf-8 -*-
"""
Interface for Peakforce capture curves channels.

"""

from ctypes import c_double, c_int
import numpy as np
from .force_volume_curves import ForceVolumeCurvesChannel
from .. import tools
from ..constants import FORCE, METRIC, UNIT_TYPES
from ..dll import _np_double
from ..structures import XYCurve, TraceRetrace


class PeakforceCaptureCurvesChannel(ForceVolumeCurvesChannel):
    """Peakforce capture curves channel interface."""
    def __init__(self, file, i_chan):
        """Create the PeakforceCaptureCurvesChannel object.

        This object corresponds to the i_chan channel of the file file.
        """
        super(PeakforceCaptureCurvesChannel, self).__init__(file, i_chan)

    def get_forward_ramp_velocity(self, is_metric):
        """Not defined in peakforce."""
        raise AttributeError("'PeakforceCaptureCurvesChannel' has no "
                             "attribute 'get_forward_ramp_velocity'")
        # cancel attribute from 'CurveMaker'

    def get_reverse_ramp_velocity(self, is_metric):
        """Not defined in peakforce."""
        raise AttributeError("'PeakforceCaptureCurvesChannel' has no "
                             "attribute 'get_reverse_ramp_velocity'")
        # cancel attribute from 'CurveMaker'

    def get_force_curve_z_data(self, trace_len, retrace_len):
        """Return peakforce height data.

        trace_len, retrace_len:
            Number of samples in the trace and retrace.

        Return a TraceRetrace object.
        """
        # create arrays of doubles
        trace = np.zeros(trace_len, np.double)
        retrace = np.zeros(retrace_len, np.double)

        argtypes = [_np_double, _np_double, c_int, c_int]

        self.file._dll_get("PeakForceCaptureZData", trace,
                           retrace, trace_len, retrace_len, argtypes=argtypes)
        trace = trace[::-1]

        return TraceRetrace(trace, retrace)

    def create_force_time_plot(self, i_curve, unit_type):
        """Create a Force Time Plot.

        unit_type: unit type: METRIC, VOLTS, FORCE or RAW

        Return data (XYCurve) and ax_properties (dict with title,
        xlabel, and ylabel).
        """
        tools.check_unit_type(unit_type, UNIT_TYPES)

        y_trace, y_retrace = self.get_force_curve_data(i_curve, unit_type)
        trace_len = len(y_trace)
        retrace_len = len(y_retrace)

        freq = self.file.peakforce_tapping_freq
        if not freq:
            raise ValueError("Corrupted file: bad data")
        t_interval = 1e6 / freq  # in µs
        t_incr = t_interval / (trace_len + retrace_len)
        y = np.concatenate((y_trace, y_retrace))
        x = np.array(range(trace_len + retrace_len)) * t_incr

        type_desc = self.data_type_desc
        scale_unit = self.get_scale_unit(unit_type)

        data = XYCurve(x, y)
        ax_properties = {
            "title": type_desc + " vs. Time",
            "xlabel": "Time (s)",
            "ylabel": u"{} ({})".format(type_desc, scale_unit)}

        return data, ax_properties

    def create_force_z_plot(self, i_curve, unit_type):
        """Create a Force Z Plot.

        unit_type: unit type: METRIC

        Return data (TraceRetrace with two XYCurve) and ax_properties
        (dict with title, xlabel, and ylabel).
        """
        tools.check_unit_type(unit_type, UNIT_TYPES)

        y_trace, y_retrace = self.get_force_curve_data(i_curve, unit_type)
        trace_len = len(y_trace)
        retrace_len = len(y_retrace)
        x_trace, x_retrace = self.get_force_curve_z_data(trace_len,
                                                         retrace_len)
        type_desc = self.data_type_desc
        x_scale_unit = self.get_scale_unit(METRIC)
        y_label = u"{} ({})".format(type_desc, x_scale_unit)

        x_label = u"Z ({})".format(x_scale_unit)

        trace = XYCurve(x_trace, y_trace)
        retrace = XYCurve(x_retrace, y_retrace)
        data = TraceRetrace(trace, retrace)
        ax_properties = {
            "title": "Force vs. Z",
            "xlabel": x_label,
            "ylabel": y_label}
        return data, ax_properties
