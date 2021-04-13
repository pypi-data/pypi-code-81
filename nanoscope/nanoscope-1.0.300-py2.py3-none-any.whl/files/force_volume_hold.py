# -*- coding: utf-8 -*-
"""
Interface for open FV hold files.

"""

from .force_volume import ForceVolumeFile
from .hold_curve import HoldCurveFile
from ..channels import ForceVolumeImageChannel, ForceVolumeHoldCurvesChannels


class ForceVolumeHoldFile(ForceVolumeFile, HoldCurveFile):
    """Force Volume Hold file interface

    Regroup a ForceVolumeImageChannel and one or several
    ForceVolumeHoldCurvesChannel.
    """
    def __init__(self, filename):
        """Create the ForceVolumeHoldFile object."""
        super(ForceVolumeHoldFile, self).__init__(filename)

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
                self._channels[i_chan] = ForceVolumeImageChannel(
                    self, i_chan)
            else:
                self._channels[i_chan] = ForceVolumeHoldCurvesChannels(
                    self, i_chan)
        return self._channels[i_chan]

    @property
    def force_curves_channel(self):
        """Force Curve channel, equivalent to file[1]."""
        raise AttributeError("ForceVolumeHoldFiles may have several Force "
                             "Channels. See force_curves_channels instead.")

    @property
    def force_curves_channels(self):
        """Force Curve channels, equivalent to file[1:]."""
        return self[1:]
