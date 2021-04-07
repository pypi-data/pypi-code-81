# -*- coding: utf-8 -*-
"""Some test fixtures"""
import numpy as np
import pytest


@pytest.fixture()
def make_dataset():
    """Make a dataset with three targets"""
    return np.arange(0, 10, 1), np.arange(10, 20, 1)


@pytest.fixture()
def make_data_dictionary():
    """Create a data dictionary"""
    return {
        "x": {"data": [1, 2, 3], "type": "INDEPENDENT", "unit": "cm"},
        "y": {"data": [3, 2, 3], "type": "DEPENDENT", "unit": "h"},
        "z": {"data": [3, 2, 3], "type": "DEPENDENT", "unit": "kg"},
    }
