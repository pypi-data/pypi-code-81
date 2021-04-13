# -*- coding: utf-8 -*-
"""
Base structures.

"""

from collections import namedtuple

XYCurve = namedtuple("XYData", ("x", "y"))

TraceRetrace = namedtuple("TraceRetrace", ("trace", "retrace"))
# trace & retrace may be of type XYCurve or simple arrays (Y data only)


class ModulationInfo:
    """Modulation info (used by hold_curve.py)

    type_desc (str): modulation type
    amplitude (double): modulation amplitude (in amplitude_units)
    frequency (double): modulation frequency (in frequency_units)
    amplitude_units (str): amplitude units
    frequency_units (str): frequency units
    """

    def __init__(self, type_desc, amplitude, frequency, amplitude_units,
                 frequency_units):
        self.type_desc = type_desc
        self.amplitude = amplitude
        self.frequency = frequency
        self.amplitude_units = amplitude_units
        self.frequency_units = frequency_units


class ScriptSegmentInfo:
    """ All info about the segments in a script. script.py processes all 
    the objects of type Segments_____ to return one ScriptSegmentInfo object.
    """

    def __init__(self, size, description, type_, duration, period,
                 amplitude, frequency, phase_offset, duration_units,
                 period_units, amplitude_units, frequency_units,
                 phase_offset_units, tip_bias, tip_bias_units, ttl_output,
                 ramp_type, ramp_start, ramp_size, ramp_start_units,
                 ramp_size_units):
        self.size = size
        self.description = description
        self.type = type_
        self.is_modulation = (7 <= type_ <= 10)
        self.duration = duration
        self.period = period
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase_offset = phase_offset
        self.duration_units = duration_units
        self.period_units = period_units
        self.amplitude_units = amplitude_units
        self.frequency_units = frequency_units
        self.phase_offset_units = phase_offset_units
        self.tip_bias = tip_bias
        self.tip_bias_units = tip_bias_units
        self.ttl_output = ttl_output
        self.ramp_type = ramp_type
        self.ramp_start = ramp_start
        self.ramp_size = ramp_size
        self.ramp_start_units = ramp_start_units
        self.ramp_size_units = ramp_size_units


class SegmentsBasicInfo:
    """ Information relevant to every type of segment 
    """

    def __init__(self, sizes, descriptions, types, durations, periods,
                 duration_units, period_units, ttl_outputs):
        self.sizes = sizes
        self.descriptions = descriptions
        self.types = types
        self.durations = durations
        self.periods = periods
        self.duration_units = duration_units
        self.period_units = period_units
        self.ttl_outputs = ttl_outputs


class SegmentsModulationInfo:
    """Modulation info coming from segments
    """

    def __init__(self, amplitudes, frequencies,  amplitude_units,
                 frequency_units, phase_offsets, phase_offset_units):
        self.amplitudes = amplitudes
        self.frequencies = frequencies
        self.amplitude_units = amplitude_units
        self.frequency_units = frequency_units
        self.phase_offsets = phase_offsets
        self.phase_offset_units = phase_offset_units


class SegmentsBiasInfo:
    """ Bias info of segments. (For now, just tip bias)
    """

    def __init__(self, tip_biases, tip_bias_units):
        self.tip_biases = tip_biases
        self.tip_bias_units = tip_bias_units


class SegmentsRampInfo:
    """ Ramp info of segments. 
    """

    def __init__(self, ramp_types, ramp_starts, ramp_sizes, ramp_start_units,
                 ramp_size_units):
        self.ramp_types = ramp_types
        self.ramp_starts = ramp_starts
        self.ramp_sizes = ramp_sizes
        self.ramp_start_units = ramp_start_units
        self.ramp_size_units = ramp_size_units


class SurfaceControlInfo:
    """Modulation and ramp info coming from surface controls.
    This info is used to overwrite modulation and ramp info
    for any segments that have a TTL output of 2
    """

    def __init__(self, amplitude, frequency, amp_units, freq_units,
                 sweep_type, ramp_type, ramp_start, ramp_size,
                 ramp_start_units, ramp_size_units):
        self.amplitude = amplitude
        self.frequency = frequency
        self.amp_units = amp_units
        self.freq_units = freq_units
        self.ramp_type = ramp_type
        self.sweep_type = sweep_type
        self.ramp_start = ramp_start
        self.ramp_size = ramp_size
        self.ramp_start_units = ramp_start_units
        self.ramp_size_units = ramp_size_units
