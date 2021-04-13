# -*- coding: utf-8 -*-
"""
Interface for Script channels.

"""

from ctypes import c_double, c_int
import numpy as np
from .base import Channel
from .. import tools
from ..constants import METRIC, RAW, VOLTS
from ..dll import _np_double
from ..structures import XYCurve


class ScriptChannel(Channel):
    """Interface for Script channels."""
    def __init__(self, file, i_chan):
        """Create the ScriptChannel object."""
        super(ScriptChannel, self).__init__(file, i_chan)

    def get_script_segment_data(self, i_seg, unit_type):
        """Return the data of the script segments as a XYCurve.

        i_seg: index of the segment (0-based)
            if None, get all segments
        unit_type: unit type: METRIC, VOLTS, RAW
        """
        n_segs = self.file.segments_count
        segs_info = self.file.segments_info

        if i_seg is None:
            i_seg = -1
            n_pts = sum([si.size for si in segs_info])
        elif 0 <= i_seg < n_segs:
            n_pts = segs_info[i_seg].size
        else:
            raise IndexError("Segment index i_seg is out of bounds.")

        # create arrays of doubles
        double_x = np.zeros(n_pts, np.double)
        double_y = np.zeros(n_pts, np.double)

        argtypes = [c_int, c_int, c_int, _np_double, _np_double]

        tools.check_unit_type(unit_type, (RAW, METRIC, VOLTS))
        self.file._dll_get("Script" + unit_type + "SegmentData", self.i_chan,
                           i_seg, n_pts, double_x, double_y, argtypes=argtypes)
        return XYCurve(double_x, double_y)
