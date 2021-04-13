# -*- coding: utf-8 -*-
"""
Interface for accessing Image channels

"""


from ctypes import byref, c_double, c_int, POINTER
import numpy as np
from .map_ import MapChannel
from .. import tools
from ..constants import METRIC, RAW, VOLTS
from ..dll import _np_double
from ..tools import constant_property


class ImageChannel(MapChannel):
    """ImageChannel interface."""
    def __init__(self, file, i_chan):
        """Create the ImageChannel object.

        This object corresponds to the i_chan channel of the file file.
        """
        super(ImageChannel, self).__init__(file, i_chan)

    @constant_property
    def aspect_ratio(self):
        """Aspect ratio"""
        aspect_ratio = c_double()
        self.file._dll_get("ImageAspectRatio", self.i_chan,
                           byref(aspect_ratio))
        return aspect_ratio.value

    def get_image_data(self, unit_type):
        """Return image ImageData.

        unit_type: unit type: METRIC, VOLTS, RAW
        """
        tools.check_unit_type(unit_type, (RAW, METRIC, VOLTS))
        spl = self.samples_per_line
        lines = self.number_of_lines

        max_data_size = spl * lines
        actual_data_size = c_int()

        # create arrays of doubles
        data = np.zeros(self.shape, np.double)

        argtypes = [c_int, _np_double, c_int, POINTER(c_int)]
        self.file._dll_get(
            "Image" + unit_type + "Data", self.i_chan, data,
            max_data_size, byref(actual_data_size), argtypes=argtypes)
        return data

    def create_image(self, unit_type):
        """Create the image.

        unit_type: unit type: METRIC, VOLTS, RAW

        Return image_data and ax_properties (dict with title and
        xlabel).
        """
        image_data = self.get_image_data(unit_type)
        type_desc = self.data_type_desc
        line_dir = self.line_direction
        scan_line = self.scan_line
        scan_size_label = self.scan_size_label
        ax_properties = {
            "title": type_desc,
            "xlabel": u"{} \n{} \n{}".format(scan_size_label,
                                             line_dir, scan_line)
                        }
        return image_data, ax_properties
