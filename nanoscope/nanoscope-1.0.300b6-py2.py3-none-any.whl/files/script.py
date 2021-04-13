# -*- coding: utf-8 -*-
"""
Interface for Nanoscope Script files.

"""

from ctypes import (byref, c_double, c_int, c_int32, pointer, POINTER)
import numpy as np
from ..channels import ScriptChannel
from .base import File
from ..dll import _np_int32, _np_double, _string_buffer
from ..tools import constant_property
from ..tools import script_tools as st
from ..structures import ScriptSegmentInfo, SegmentsModulationInfo, \
    SurfaceControlInfo, SegmentsBiasInfo, SegmentsRampInfo, SegmentsBasicInfo


class ScriptFile(File):
    """Interface to Nanoscope Script files

    Regroup one or several ScriptChannel.
    """

    def __init__(self, filename):
        """Create the ScriptFile object."""
        super(ScriptFile, self).__init__(filename)

    def _get_channel(self, i_chan):
        """Return ScriptChannel i_chan.

        If out of range, raise an IndexError.
        """
        if i_chan not in self._channels.keys():
            if not (0 <= i_chan < self.number_of_channels):
                raise IndexError("i_chan out of range")
            self._channels[i_chan] = ScriptChannel(self, i_chan)
        return self._channels[i_chan]

    @constant_property
    def segments_count(self):
        """Number of segments in the script file."""
        num_segs = c_int()
        self._dll_get("ScriptSegmentCount", byref(num_segs))
        return num_segs.value

    @constant_property
    def segments_basic_info(self):
        """Basic info of the script segments.

        List of ScriptSegment, one element per segment.
        """
        # initialize everything
        n_segs = self.segments_count
        buff_type = POINTER(_string_buffer) * n_segs

        descrs = buff_type()
        types = np.zeros(n_segs, np.int32)

        sizes = np.zeros(n_segs, np.int32)

        durations = np.zeros(n_segs, np.double)
        duration_units = buff_type()

        periods = np.zeros(n_segs, np.double)
        period_units = buff_type()

        ttl_outputs = np.zeros(n_segs, np.int32)

        for i in range(n_segs):
            descrs[i] = pointer(_string_buffer())
            duration_units[i] = pointer(_string_buffer())
            period_units[i] = pointer(_string_buffer())

        # set argument types for DLL calls
        argtypes_info = [c_int, POINTER(buff_type), _np_int32,
                         _np_int32, _np_double, _np_double, _np_int32]
        argtypes_time_units = [c_int, POINTER(buff_type), POINTER(buff_type)]

        # DLL calls
        self._dll_get("ScriptSegmentInfo", n_segs, pointer(descrs), types,
                      sizes, durations, periods, ttl_outputs,
                      argtypes=argtypes_info)
        self._dll_get("ScriptSegmentTimeUnits", n_segs,
                      pointer(duration_units), pointer(period_units),
                      argtypes=argtypes_time_units)

        # decode necessary values so members of SegmentsBasicInfo are regular
        # Python types, not ctypes types
        descrs = st.decode_2d_char_array(descrs)
        duration_units = st.decode_2d_char_array(duration_units)
        period_units = st.decode_2d_char_array(period_units)

        return SegmentsBasicInfo(
            sizes,
            descrs,
            types,
            durations,
            periods,
            duration_units,
            period_units,
            ttl_outputs
        )

    @constant_property
    def surface_control_info(self):
        """Returns modulation and ramp values from surface controls. 
        Note: these are single values, not arrays.
        """

        # initialize everything
        amplitude = c_double()
        frequency = c_double()
        amp_units = _string_buffer()
        freq_units = _string_buffer()
        sweep_type = _string_buffer()
        ramp_type = _string_buffer()
        ramp_start = c_double()
        ramp_stop = c_double()
        ramp_start_units = 'Hz'  # ForceSweepFreqRange DLL function returns Hz
        ramp_size_units = 'Hz'
        i_chan = 0  # default

        # DLL calls
        self._dll_get("RampModulationInfo", ramp_type, byref(amplitude),
                      byref(frequency))
        self._dll_get("RampModulationUnits", amp_units, freq_units)

        self._dll_get("ForceSweepChannel", i_chan, sweep_type)
        self._dll_get("ForceSweepFreqRange", i_chan, byref(ramp_start),
                      byref(ramp_stop))

        # use .value to decode so that all members of SurfaceControlInfo are
        # regular Python types rather than ctypes types

        # store info in terms of ramp size to be consistent with surface
        # control info
        ramp_size = ramp_stop.value - ramp_start.value

        return SurfaceControlInfo(
            amplitude.value,
            frequency.value,
            amp_units.value,
            freq_units.value,
            sweep_type.value,
            ramp_type.value,
            ramp_start.value,
            ramp_size,
            ramp_start_units,
            ramp_size_units,
        )

    @constant_property
    def segments_bias_info(self):
        """Returns bias info from segments (for now, just tip bias).
        """

        # initialize everything
        n_segs = self.segments_count
        buff_type = POINTER(_string_buffer) * n_segs

        tip_bias = np.zeros(n_segs, np.double)
        tip_bias_units = buff_type()

        # set argument types for DLL calls
        argtypes_bias_info = [c_int, _np_double]
        argtypes_bias_units = [c_int, POINTER(buff_type)]

        for i in range(n_segs):
            tip_bias_units[i] = pointer(_string_buffer())

        # DLL calls
        self._dll_get("ScriptBiasSegmentInfo",  n_segs, tip_bias,
                      argtypes=argtypes_bias_info)
        self._dll_get("ScriptBiasSegmentUnits", n_segs, tip_bias_units,
                      argtypes=argtypes_bias_units)

        # decode necessary values so all members of BiasInfo are regular
        # Python types, not ctypes types
        tip_bias_units = st.decode_2d_char_array(tip_bias_units)

        return SegmentsBiasInfo(
            tip_bias,
            tip_bias_units
        )

    @constant_property
    def segments_ramp_info(self):
        """Returns ramp info from segments.
        """

        # initialize everything
        n_segs = self.segments_count
        buff_type = POINTER(_string_buffer) * n_segs

        ramp_type = buff_type()
        ramp_start = np.zeros(n_segs, np.double)
        ramp_size = np.zeros(n_segs, np.double)
        ramp_start_units = buff_type()
        ramp_size_units = buff_type()

        for i in range(n_segs):
            ramp_type[i] = pointer(_string_buffer())
            ramp_start_units[i] = pointer(_string_buffer())
            ramp_size_units[i] = pointer(_string_buffer())

        # set argument types for DLL calls
        argtypes_ramp_info = [c_int, POINTER(
            buff_type), _np_double, _np_double]
        argtypes_ramp_units = [c_int, POINTER(buff_type), POINTER(buff_type)]

        # DLL calls
        self._dll_get("ScriptRampSegmentInfo", n_segs, pointer(ramp_type),
                      ramp_size, ramp_start, argtypes=argtypes_ramp_info)
        self._dll_get("ScriptRampSegmentUnits", n_segs,
                      pointer(ramp_size_units), pointer(ramp_start_units),
                      argtypes=argtypes_ramp_units)

        # decode necessary values so all members of RampInfo are regular
        # Python types, not ctypes types
        ramp_type = st.decode_2d_char_array(ramp_type)
        ramp_start_units = st.decode_2d_char_array(ramp_start_units)
        ramp_size_units = st.decode_2d_char_array(ramp_size_units)

        return SegmentsRampInfo(
            ramp_type,
            ramp_start,
            ramp_size,
            ramp_start_units,
            ramp_size_units,
        )

    @constant_property
    def segments_modulation_info(self):
        # initialize everything
        n_segs = self.segments_count
        buff_type = POINTER(_string_buffer) * n_segs

        amplitudes = np.zeros(n_segs, np.double)
        amp_units = buff_type()

        frequencies = np.zeros(n_segs, np.double)
        freq_units = buff_type()

        phase_offs = np.zeros(n_segs, np.double)
        phase_off_units = buff_type()

        for i in range(n_segs):
            amp_units[i] = pointer(_string_buffer())
            freq_units[i] = pointer(_string_buffer())
            phase_off_units[i] = pointer(_string_buffer())

        # set argument types for DLL calls
        argtypes_mod_info = [c_int, _np_double, _np_double, _np_double]
        argtypes_mod_units = [c_int, POINTER(buff_type), POINTER(buff_type),
                              POINTER(buff_type)]

        # DLL calls
        self._dll_get("ScriptModulationSegmentInfo", n_segs, amplitudes,
                      frequencies, phase_offs, argtypes=argtypes_mod_info)
        self._dll_get("ScriptModulationSegmentUnits", n_segs, amp_units,
                      freq_units, phase_off_units, argtypes=argtypes_mod_units)

        # decode necessary values so all members of ModulationInfo are regular
        # Python types, not ctypes types
        amp_units = st.decode_2d_char_array(amp_units)
        freq_units = st.decode_2d_char_array(freq_units)
        phase_off_units = st.decode_2d_char_array(phase_off_units)

        return SegmentsModulationInfo(
            amplitudes,
            frequencies,
            amp_units,
            freq_units,
            phase_offs,
            phase_off_units
        )

    @constant_property
    def segments_info(self):
        """ Collects all the types of info (basic, modulation, ramp, bias, 
        surface control) into ScriptSegmentInfo objects containing all the info
        about each segment. Handles the overwriting of modulation/ramp values
        by surface controls for segments that have a TTL output of 2.
        """
        # load all script into
        n_segs = self.segments_count
        basic_info = self.segments_basic_info
        mod_info = self.segments_modulation_info
        ramp_info = self.segments_ramp_info
        bias_info = self.segments_bias_info
        surface_info = self.surface_control_info

        # initialize lists for the properties that may be modified in this
        # function
        amplitudes = mod_info.amplitudes
        amplitude_units = mod_info.amplitude_units
        frequencies = mod_info.frequencies  # fixed frequencies
        frequency_units = mod_info.frequency_units
        ramp_types = ramp_info.ramp_types
        ramp_starts = ramp_info.ramp_starts
        ramp_sizes = ramp_info.ramp_sizes
        ramp_start_units = ramp_info.ramp_start_units
        ramp_size_units = ramp_info.ramp_size_units

        # strip out frequency units for any non-modulating segments
        for i in range(n_segs):
            if basic_info.types[i] > 10 or basic_info.types[i] < 7:
                frequency_units[i] = ""

        # Overwrite ramp and modulation info with info from surface controls
        # if TTL output is 2, indicating the setting "Out2+Mod" (modulation
        # set at surface controls)
        is_frequency_sweep = b"freq" in surface_info.sweep_type.lower()
        for i in range(n_segs):

            if basic_info.ttl_outputs[i] != 2:
                continue

            # set segment amplitude to workspace amplitude
            amplitudes[i] = surface_info.amplitude
            amplitude_units[i] = surface_info.amp_units

            if is_frequency_sweep:  # surface modulation is frequency sweep
                ramp_types[i] = "Sweep"
                ramp_starts[i] = surface_info.ramp_start
                ramp_sizes[i] = surface_info.ramp_size

                ramp_start_units[i] = surface_info.ramp_start_units
                ramp_size_units[i] = surface_info.ramp_size_units

            else:  # surface modulation is fixed frequency
                ramp_types[i] = ""
                frequencies[i] = surface_info.frequency
                frequency_units[i] = surface_info.freq_units

        return [
            ScriptSegmentInfo(
                basic_info.sizes[i],
                basic_info.descriptions[i],
                basic_info.types[i],
                basic_info.durations[i],
                basic_info.periods[i],
                amplitudes[i],
                frequencies[i],
                mod_info.phase_offsets[i],
                basic_info.duration_units[i],
                basic_info.period_units[i],
                amplitude_units[i],
                frequency_units[i],
                mod_info.phase_offset_units[i],
                bias_info.tip_biases[i],
                bias_info.tip_bias_units[i],
                basic_info.ttl_outputs[i],
                ramp_types[i],
                ramp_starts[i],
                ramp_sizes[i],
                ramp_start_units[i],
                ramp_size_units[i],
            )
            for i in range(n_segs)]
