# -*- coding: utf-8 -*-
"""
Interface for Peakforce capture image channels.

"""

from .force_volume_image import ForceVolumeImageChannel


class PeakforceCaptureImageChannel(ForceVolumeImageChannel):
    """Peakforce capture image channel interface."""
    def __init__(self, file, i_chan):
        """Create the ForceVolumeImageChannel object.

        This object corresponds to the i_chan channel of the file file.
        """
        super(PeakforceCaptureImageChannel, self).__init__(file, i_chan)

    def create_image(self, unit_type):
        """Create a Force Volume Image.

        unit_type: unit type: METRIC, VOLTS, RAW

        Return image_data and ax_properties (dict with title and
        xlabel).
        """
        image_data = self.get_image_data(unit_type)
        type_desc = self.data_type_desc
        ax_properties = {
            "title": "Peakforce {} Image".format(type_desc),
            "xlabel": self.scan_size_label}
        return image_data, ax_properties
