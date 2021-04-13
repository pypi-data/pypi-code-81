# -*- coding: utf-8 -*-
"""
Interface for opening nano drive files.

"""

from .image import ImageFile


class NanoDriveFile(ImageFile):
    """Interface to NanoDrive files"""
    def __init__(self, filename):
        """Creates the NanoDriveFile object."""
        super(NanoDriveFile, self).__init__(filename)
