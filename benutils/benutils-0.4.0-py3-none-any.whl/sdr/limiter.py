# -*- coding: utf-8 -*-

"""package benutils
author    Benoit Dubois
copyright FEMTO ENGINEERING, 2020
license   GPL v3.0+
brief     LImiter
"""

import numpy as np
import signalslot as ss


DATA_CHECK_ARRAY_LENGTH = 10
MONITORING_MODE, REJECT_MODE = 0, 1

class Limiter():
    """Class Limiter
    """

    in_updated = ss.Signal(['value'])
    out_updated = ss.Signal(['value'])

    def __init__(self, min_, max_):
        """The constructor.
        :param mode: Behavior with outliers, monitoring or reject (int)
        :param length: length of the data buffer (int)
        :returns: None
        """
        self._idx = 0
        self._mode = MONITORING_MODE
        self._ini_value = ini_value
        self._m = length
        self._data = np.full([length], ini_value, np.float64)  # FIFO

    def reset(self, **kwargs):
        """Reset.
        :returns: None
        """
        self._data = np.full([self._m], self._ini_value, np.float64)
        self._idx = 0

    def set_ini(self, value):
        self._ini_value = value

    def get_ini(self):
        return self._ini_value
