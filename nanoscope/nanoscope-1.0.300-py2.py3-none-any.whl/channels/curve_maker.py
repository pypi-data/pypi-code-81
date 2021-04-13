# -*- coding: utf-8 -*-
"""
Common fonctions for force curves with or without hold, standalone or
in a bigger file.

"""

from ctypes import byref, c_double, c_char
import numpy as np
from .base import Channel
from .. import tools
from ..constants import FORCE, METRIC, UNIT_TYPES
from ..dll import _string_buffer
from ..structures import XYCurve, TraceRetrace
from ..tools import constant_property


class CurveMakerChannel(Channel):
    """Object able to create force curves and corresponding plots."""
    def __init__(self, file, i_chan):
        super(CurveMakerChannel, self).__init__(file, i_chan)

    @constant_property
    def is_deflection_channel(self):
        """True iff channel is a deflection channel."""
        return self.data_type_desc.lower().find("deflection") >= 0

    def get_forward_ramp_velocity(self, is_metric):
        """Return the forward ramp velocity from the header file.

        is_metric:
            if True, return ramp_size to metric unit
            else, return ramp_size to volts unit
        """
        velocity = c_double()
        self.file._dll_get("ForwardRampVelocity", self.i_chan,
                           byref(velocity), is_metric)
        return velocity.value

    def get_reverse_ramp_velocity(self, is_metric):
        """Return the reverse ramp velocity from the header file.

        is_metric:
            if True, return ramp_size to metric unit
            else, return ramp_size to volts unit
        """
        velocity = c_double()
        self.file._dll_get("ReverseRampVelocity", self.i_chan,
                           byref(velocity), is_metric)
        return velocity.value

    def get_ramp_size(self, is_metric):
        """Ramp size of force curve.

        is_metric:
            if True, return ramp_size to metric unit
            else, return ramp_size to volts unit
        """
        size = c_double()
        self.file._dll_get("RampSize", self.i_chan, byref(size), is_metric)
        return size.value

    def get_ramp_size_unit(self, is_metric):
        """Return the ramp size unit of force curve.

        is_metric:
            if True, return ramp_size to metric unit
            else, return ramp_size to volts unit
        """
        ramp_unit = _string_buffer()
        self.file._dll_get("RampUnits", self.i_chan, ramp_unit, is_metric)
        return ramp_unit.value.decode("latin-1")

    def compute_separation(self, data, unit_type, h_sens_data=None):
        """Compute separation from force curve data.

        unit_type: unit type: METRIC or FORCE
        data: XYCurve or TraceRetrace.
        h_sens_data: height sensor data: array or TraceRetrace, overwrite
            x data if provided (optional).

        Return sep_data (type of data).
        """
        tools.check_unit_type(unit_type, {FORCE, METRIC})

        x_data = None
        z_trace = None
        z_retrace = None

        if unit_type == FORCE:
            d_sep_scale = 1. / self.spring_constant
        else:
            d_sep_scale = 1.

        if isinstance(data, XYCurve):
            if not h_sens_data:
                x_data = data.x
            elif isinstance(h_sens_data, np.array):
                x_data = h_sens_data
            else:
                ValueError("Incompatible Height Sensor Data.")
            delta = data.y.max()
            z_max = x_data.max()
            x = (z_max - x_data) - (delta - data.y)*d_sep_scale
            return XYCurve(x, np.array(data.y))
        elif isinstance(data, TraceRetrace):
            if not h_sens_data:
                z_trace = data.trace.x
                z_retrace = data.retrace.x
            elif isinstance(h_sens_data, TraceRetrace):
                z_trace = h_sens_data.trace
                z_retrace = h_sens_data.retrace
            else:
                ValueError("Incompatible Height Sensor Data.")

            y_trace = data.trace.y
            y_retrace = data.retrace.y

            delta = y_trace[-1]
            z_max = z_trace[-1]
            x_trace = (z_max - z_trace) - (delta - y_trace)*d_sep_scale
            z_max = z_retrace[0]
            x_retrace = (z_max - z_retrace) - (delta - y_retrace)*d_sep_scale
            trace = XYCurve(x_trace, np.array(y_trace))
            retrace = XYCurve(x_retrace, np.array(y_retrace))
            return TraceRetrace(trace, retrace)

    def _create_force_time_plot(self, unit_type, get_fc_data_func,
                                get_hold_data_func=None, i_curve=None):
        """Create a Force Time Plot.

        unit_type: unit type: METRIC, VOLTS, FORCE or RAW
        get_fc_data_func: function called to get the force curve data
        get_hold_data_func:
            function called to get the hold data (if applicable)
            if provided, self must have a parameter force_hold_time
        i_curve: index of the curve, if in a multi-curve channel

        If i_curve is None, both function must have a (unit_type)
        signature. Else, their signature must be (i_curve, unit_type).

        Return data (XYCurve) and ax_properties (dict with title,
        xlabel, and ylabel).
        """
        tools.check_unit_type(unit_type, UNIT_TYPES)

        args = (unit_type,) if i_curve is None else (i_curve, unit_type)
        y_trace, y_retrace = get_fc_data_func(*args)
        trace_len = len(y_trace)
        retrace_len = len(y_retrace)

        is_metric = int(unit_type in (METRIC, FORCE))
        ramp_size = self.get_ramp_size(is_metric)
        ramp_vel_for = self.get_forward_ramp_velocity(is_metric)
        ramp_vel_rev = self.get_reverse_ramp_velocity(is_metric)

        if not (ramp_vel_for and ramp_vel_rev and trace_len and retrace_len):
            raise ValueError("Corrupted file: bad data")
        trace_time_s = ramp_size * 1. / ramp_vel_for
        retrace_time_s = ramp_size * 1. / ramp_vel_rev
        t_incr_t = trace_time_s * 1. / trace_len
        t_incr_r = retrace_time_s * 1. / retrace_len

        if get_hold_data_func:
            y_hold = get_hold_data_func(unit_type)
            hold_len = len(y_hold)
            hold_time_secs = self.force_hold_time
            t_incr_h = hold_time_secs * 1. / hold_len
        else:
            y_hold = []
            hold_len = 0
            hold_time_secs = 0
            t_incr_h = 1  # Will be multiplied by 0

        # merge reversed trace and retrace arrays
        y = np.concatenate((y_trace, y_hold, y_retrace))

        # note: x_trace correspond to the reversed y_trace
        x_trace = np.array(range(trace_len)) * t_incr_t
        x_hold = (trace_time_s +
                  np.array(range(hold_len)) * t_incr_h)
        x_retrace = (trace_time_s + hold_time_secs +
                     np.array(range(retrace_len)) * t_incr_r)
        x = np.concatenate((x_trace, x_hold, x_retrace))

        type_desc = self.data_type_desc
        scale_unit = self.get_scale_unit(unit_type)

        data = XYCurve(x, y)
        ax_properties = {
            "title": type_desc + " vs. Time",
            "xlabel": "Time (s)",
            "ylabel": u"{} ({})".format(type_desc, scale_unit)}

        return data, ax_properties

    def _create_force_z_plot(self, unit_type,
                             get_fc_data_func, i_curve=None):
        """Create a Force Z Plot.

        unit_type: unit type: METRIC, VOLTS, FORCE or RAW
        get_fc_data_func: function called to get the force curve data
        i_curve: index of the curve, if in a multi-curve channel

        If i_curve is None, the function must have a (unit_type)
        signature. Else, its signature must be (i_curve, unit_type).

        Return data (TraceRetrace with two XYCurve) and ax_properties
        (dict with title, xlabel, and ylabel).
        """
        tools.check_unit_type(unit_type, UNIT_TYPES)
        args = (unit_type,) if i_curve is None else (i_curve, unit_type)
        y_trace, y_retrace = get_fc_data_func(*args)
        trace_len = len(y_trace)
        retrace_len = len(y_retrace)

        type_desc = self.data_type_desc
        scale_unit = self.get_scale_unit(unit_type)

        tools.check_unit_type(unit_type, UNIT_TYPES)
        is_metric = int(unit_type in (METRIC, FORCE))
        ramp_size = self.get_ramp_size(is_metric)
        ramp_unit = self.get_ramp_size_unit(is_metric)

        z_incr = ramp_size * 1. / retrace_len
        if trace_len < retrace_len:
            z_init = (retrace_len - trace_len) * z_incr
        else:
            z_init = 0.

        y_trace = y_trace
        y_label = u"{} ({})".format(type_desc, scale_unit)

        x_label = u"Z ({})".format(ramp_unit)
        x_trace = z_init + np.array(range(trace_len))*z_incr
        x_retrace = x_trace[-1] - np.array(range(retrace_len))*z_incr

        trace = XYCurve(x_trace, y_trace)
        retrace = XYCurve(x_retrace, y_retrace)
        data = TraceRetrace(trace, retrace)
        ax_properties = {
            "title": type_desc + " vs. Z",
            "xlabel": x_label,
            "ylabel": y_label}

        return data, ax_properties
