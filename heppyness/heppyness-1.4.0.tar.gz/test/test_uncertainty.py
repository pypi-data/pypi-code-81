import pytest
import pdb

# Auxiliary modules
import numpy as np
from copy import deepcopy
import sys

# Module to be tested
sys.path.append('..')
import heppy

# Setup: create a histogram
_areas = np.array([4.3, 9.7, 12.1])
_binedges = np.array([-7., 0., 5., 50.])
_uncorr_variations = {
    'stat_up' : _areas + np.sqrt(_areas), # approx [6.37, 12.81, 15.58]
    'stat_down' : _areas - np.sqrt(_areas) # approx [2.23, 6.59, 8.62]
}
_corr_variations = {
    'foo_up' : _areas + np.ones_like(_areas),
    'foo_down' : _areas - np.ones_like(_areas),
    'bar_up'   : _areas + np.array([-1.0, 2.0, 0.0]),
    'bar_down' : _areas + np.array([-1.0, 1.0, -0.5]),
    'baz__1up'   : _areas + np.array([-1.0, 2.0,  0.0]),
    'baz__1down' : _areas + np.array([-1.0, 1.0, -0.5]),
    'baz__down'  : _areas + np.array([-2.0, 0.0,  3.0]),
    'single' : _areas + np.array([-4., 8.5, 3.0]),
}
_h = heppy.histogram(_binedges, _areas, areas=True, uncorr_variations=_uncorr_variations, corr_variations=_corr_variations)



# Tests

def test_remove_same_sign_shifts():
    '''
    Test removing the smaller of same-sign shifts associated with the same correlated uncertainty source
    '''
    h = heppy.uncertainty.remove_same_sign_shifts(_h)
    cv = h.corr_variations # for convenience
    np.testing.assert_array_almost_equal( cv['foo_up'], _areas + np.ones_like(_areas) )
    np.testing.assert_array_almost_equal( cv['foo_down'], _areas - np.ones_like(_areas) )
