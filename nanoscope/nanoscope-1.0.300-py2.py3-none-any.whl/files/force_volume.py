# -*- coding: utf-8 -*-
"""
Interface for opening FV files.

"""

from .base import File
from ..channels import (ForceVolumeImageChannel, ForceVolumeCurvesChannel,
                        MapChannel)


class ForceVolumeFile(File):
    """Force Volume file interface

    Regroup a ForceVolumeImageChannel and one or several
    ForceVolumeCurvesChannel.
    """
    def __init__(self, filename):
        """Create the ForceVolumeFile object."""
        super(ForceVolumeFile, self).__init__(filename)

    def _get_channel(self, i_chan):
        """Return Channel i_chan.

        Channel type depends on the idex:
            Channel 0 is the height map;
            Channel 1 contains the force curves;
            Channel 2+ is unclear (curves for FVHold).
        If out of range, raise an IndexError.
        """
        if i_chan not in self._channels.keys():
            if not (0 <= i_chan < self.number_of_channels):
                raise IndexError("i_chan out of range")
            if i_chan == 0:
                self._channels[i_chan] = ForceVolumeImageChannel(
                    self, i_chan)
            elif i_chan == 1:
                self._channels[i_chan] = ForceVolumeCurvesChannel(
                    self, i_chan)
            else:
                self._channels[i_chan] = ForceVolumeCurvesChannel(self, i_chan)
        return self._channels[i_chan]

    def find_channel(self, desc):
        """Find channel by description."""
        desc = desc.lower()
        for chan in self[1:]:  # skip image
            if chan.data_type_desc.lower().find(desc) >= 0:
                return chan
        raise IndexError('No {} channel found.'.format(desc))

    @property
    def image_channel(self):
        """Image channel, equivalent to file[0]."""
        return self[0]

    @property
    def force_curves_channel(self):
        """Force Curve channel, equivalent to file[1]."""
        return self[1]

    @property
    def deflection_channel(self):
        """Deflection channel, if exists."""
        return self.find_channel("deflection")

    @property
    def height_sensor_channel(self):
        """Height Sensor channel, if exists."""
        return self.find_channel("height sensor")
