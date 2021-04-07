# -*- coding: utf-8 -*-
"""pytojcamp package to write JCAMP files from Python"""
from ._version import get_versions
from .from_dict import from_dict
from .from_xy import from_xy

__version__ = get_versions()["version"]
del get_versions
