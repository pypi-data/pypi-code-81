# -*- coding: utf-8 -*-
"""
Interface for opening Nanoscope hold curves files.

"""

from ctypes import byref, c_double

from .curve import CurveFile
from ..channels import HoldCurveChannel
from ..dll import _string_buffer
from ..tools import constant_property
from ..structures import ModulationInfo


class HoldCurveFile(CurveFile):
    """Curve file interface

    Regroups one or several HoldCurveChannel.
    """
    def __init__(self, filename):
        """Create the CurveFile object."""
        super(CurveFile, self).__init__(filename)

    def _get_channel(self, i_chan):
        """Return CurveChannel i_chan.

        If out of range, raise an IndexError.
        """
        if i_chan not in self._channels.keys():
            if not (0 <= i_chan < self.number_of_channels):
                raise IndexError("i_chan out of range")
            self._channels[i_chan] = HoldCurveChannel(self, i_chan)
        return self._channels[i_chan]

    @constant_property
    def modulation_info(self):
        """Info on the modulation.

        Stored as a ModulationInfo object.
        """
        type_ = _string_buffer()
        amp = c_double()
        freq = c_double()
        amp_units = _string_buffer()
        freq_units = _string_buffer()

        self._dll_get("RampModulationInfo", type_, byref(amp), byref(freq))
        self._dll_get("RampModulationUnits", amp_units, freq_units)

        return ModulationInfo(
            type_.value.decode("latin-1"),
            amp.value, freq.value,
            amp_units.value.decode("latin-1"),
            freq_units.value.decode("latin-1"))

    @constant_property
    def force_sweep_type_desc(self):
        """Force sweep type description."""
        sweep = _string_buffer()
        i_chan = 0  # default
        self._dll_get("ForceSweepChannel", i_chan, sweep)
        return sweep.value.decode("latin-1")

    @constant_property
    def force_sweep_freq_range(self):
        """Force sweep frequency range (start, stop)."""
        start = c_double()
        stop = c_double()
        i_chan = 0
        self._dll_get("ForceSweepFreqRange", i_chan, byref(start), byref(stop))
        return start.value, stop.value
