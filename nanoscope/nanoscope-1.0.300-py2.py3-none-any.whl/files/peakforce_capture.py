
# -*- coding: utf-8 -*-
"""
Interface for opening peakforce capture files.

"""


from ctypes import byref, c_double
from .force_volume import ForceVolumeFile
from ..channels import (PeakforceCaptureImageChannel,
                        PeakforceCaptureCurvesChannel,
                        MapChannel)
from ..tools import constant_property


class PeakforceCaptureFile(ForceVolumeFile):
    """Peakforce capture file interface

    Regroup a PeakforceCaptureImageChannel and a
    PeakforceCaptureCurvesChannel.
    """
    def __init__(self, filename):
        """Create the PeakforceCaptureFile object."""
        super(PeakforceCaptureFile, self).__init__(filename)

    def _get_channel(self, i_chan):
        """Return Channel i_chan.

        Channel type depends on the idex:
            Channel 1 is the height map;
            Channel 2 contains the force curves.
        If out of range, raise an IndexError.
        """
        if i_chan not in self._channels.keys():
            if not (0 <= i_chan < self.number_of_channels):
                raise IndexError("i_chan out of range")
            if i_chan == 0:
                self._channels[i_chan] = PeakforceCaptureImageChannel(
                    self, i_chan)
            elif i_chan == 1:
                self._channels[i_chan] = PeakforceCaptureCurvesChannel(
                    self, i_chan)
            else:
                self._channels[i_chan] = MapChannel(self, i_chan)
        return self._channels[i_chan]

    @constant_property
    def peakforce_tapping_freq(self):
        """PeakForce tapping frequency (in Hz)."""
        pft_freq = c_double()
        self._dll_get("PeakForceTappingFreq", byref(pft_freq))
        return pft_freq.value
