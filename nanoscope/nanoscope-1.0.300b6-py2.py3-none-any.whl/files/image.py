# -*- coding: utf-8 -*-
"""
Interface for opening Image files

"""

from .base import File
from ..channels import ImageChannel


class ImageFile(File):
    """Image file interface

    Regroup one or several ImageChannel.
    """
    def __init__(self, filename):
        """Create the ImageFile object."""
        super(ImageFile, self).__init__(filename)

    def _get_channel(self, i_chan):
        """Return ImageChannel i_chan.

        If out of range, raise an IndexError.
        """
        if i_chan not in self._channels.keys():
            if not (0 <= i_chan < self.number_of_channels):
                raise IndexError("i_chan out of range")
            self._channels[i_chan] = ImageChannel(self, i_chan)
        return self._channels[i_chan]
