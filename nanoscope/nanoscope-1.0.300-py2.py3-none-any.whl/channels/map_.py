# -*- coding: utf-8 -*-
"""
Interface for accessing Map channels.

"""

from ctypes import byref, c_double, c_long, c_char, c_int
from .base import Channel
from ..dll import _string_buffer
from ..tools import constant_property


class MapChannel(Channel):
    """MapChannel interface."""
    def __init__(self, file, i_chan):
        """Create the MapChannel object.

        This object corresponds to the i_chan channel of the file file.
        """
        super(MapChannel, self).__init__(file, i_chan)

    @constant_property
    def planefit_settings(self):
        """Planefit settings of the Image channel.

        Format: (a, b, c, fit_type_str).
        a, b, c: coefficients in z = a*x + b*y + c
        fit_type_str (unicode): type of plane fit
            NeedsFull: full planefitting is needed
            Offset: offset has been removed
            Local: actual plane in data has been removed
            Captured: captured plane has been removed
            NeedsOffset: offset removal is needed
            Nothing: no planefit has been removed
            NeedsNothing: don't do any planefitting
        """
        a = c_double()
        b = c_double()
        c = c_double()
        fit_type = c_int()
        self.file._dll_get("PlanefitSettings", self.i_chan, byref(a),
                           byref(b), byref(c), byref(fit_type))
        fit_type_str = ("NeedsFull", "Offset", "Local", "Captured",
                        "NeedsOffset", "Nothing",
                        "NeedsNothing")[fit_type.value]
        return a.value, b.value, c.value, fit_type_str

    @constant_property
    def samples_per_line(self):
        """Number of samples per line."""
        samples_per_line = c_long()  # May be c_int
        self.file._dll_get("SamplesPerLine", self.i_chan,
                           byref(samples_per_line))
        return samples_per_line.value

    @constant_property
    def number_of_lines(self):
        """Number of lines."""
        number_of_lines = c_long()  # May be c_int()
        self.file._dll_get("NumberOfLines", self.i_chan,
                           byref(number_of_lines))
        return number_of_lines.value

    @constant_property
    def shape(self):
        """Image shape: (number_of_lines, samples_per_line)"""
        return self.number_of_lines, self.samples_per_line

    @constant_property
    def line_direction(self):
        """Line direction."""
        line_dir = _string_buffer()
        self.file._dll_get("LineDirection", self.i_chan, line_dir)
        return line_dir.value.decode("latin-1")

    @constant_property
    def scan_line(self):
        """Scan line description."""
        scan_line = _string_buffer()
        return self.file._dll_get("ScanLine", self.i_chan, scan_line)

    @constant_property
    def scan_size(self):
        """Scan size of the image channel."""
        scan_size = c_double()
        self.file._dll_get("ScanSize", self.i_chan, byref(scan_size))
        return scan_size.value

    @constant_property
    def scan_size_unit(self):
        """Scan size unit of the image channel."""
        unit = _string_buffer()
        self.file._dll_get("ScanSizeUnit", self.i_chan, unit)
        return unit.value.decode("latin-1")

    @constant_property
    def scan_size_label(self):
        """String label of the scan size

        E.g.: "Scan Size: 2.50 (um)"
        """
        scan_size = self.scan_size
        scan_size_unit = self.scan_size_unit

        return u"Scan Size: {:.2f} ({})".format(scan_size, scan_size_unit)
