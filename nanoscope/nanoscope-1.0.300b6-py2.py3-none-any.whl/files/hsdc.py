# -*- coding: utf-8 -*-
"""
Interface for opening HSDC files.

"""

from .base import File
from ..channels import HSDCChannel


class HSDCFile(File):
    """HSDC file interface

    Regroup one or several HSDCChannel.
    """
    def __init__(self, filename):
        """Create the HSDCFile object."""
        super(HSDCFile, self).__init__(filename)

    def _get_channel(self, i_chan):
        """Return HSDCChannel i_chan.

        If out of range, raise an IndexError.
        """
        if i_chan not in self._channels.keys():
            if not (0 <= i_chan < self.number_of_channels):
                raise IndexError("i_chan out of range")
            self._channels[i_chan] = HSDCChannel(self, i_chan)
        return self._channels[i_chan]
