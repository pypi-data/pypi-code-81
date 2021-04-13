# -*- coding: utf-8 -*-
"""
Interface for Force Volume image channels.

"""

import numpy as np
from ctypes import byref, c_double, c_int, POINTER

from .map_ import MapChannel
from .. import tools
from ..constants import METRIC, RAW, VOLTS
from ..dll import _np_double


class ForceVolumeImageChannel(MapChannel):
    """Force Volume Image Channel interface."""
    def __init__(self, file, i_chan):
        """Create the ForceVolumeImageChannel object.

        This object corresponds to the i_chan channel of the file file.
        """
        super(ForceVolumeImageChannel, self).__init__(file, i_chan)

    def get_image_data(self, unit_type):
        """Return force volume ImageData.

        unit_type: unit type: METRIC, VOLTS, RAW
        """
        tools.check_unit_type(unit_type, (METRIC, VOLTS, RAW))
        spl = self.samples_per_line
        lines = self.number_of_lines

        max_data_size = spl * lines
        actual_data_size = c_int()

        # create array of doubles
        image = np.zeros(self.shape, np.double)

        argtypes = [_np_double, c_int, POINTER(c_int)]

        self.file._dll_get("ForceVolume" + unit_type + "ImageData",
                           image, max_data_size, byref(actual_data_size),
                           argtypes=argtypes)
        return image

    def create_image(self, unit_type):
        """Create a Force Volume Image.

        unit_type: unit type: METRIC, VOLTS, RAW

        Return image_data and ax_properties (dict with title and
        xlabel).
        """
        image_data = self.get_image_data(unit_type)
        type_desc = self.data_type_desc
        ax_properties = {
            "title": "Force Volume {} Image".format(type_desc),
            "xlabel": self.scan_size_label}
        return image_data, ax_properties
