import scipy_quadopt as sqp
import pytest
import numpy as np


def test1():
    with pytest.raises(Exception):
        sqp.get_weights()


def test2():
    with pytest.raises(Exception):
        sqp.get_weights([1])


def test3():
    with pytest.raises(Exception):
        sqp.get_weights([1], [1], lam=-1)
    with pytest.raises(Exception):
        sqp.get_weights([1], [1], bnd_up=-1)
    with pytest.raises(Exception):
        sqp.get_weights([1], [1], bnd_up=2)


def test4():
    good = [.51, .52]
    simi = [[1, 2], [3, 4]]
    weights, results = sqp.get_weights(good, simi, lam=0.5)
    assert len(weights) == 2


def test5():
    # goodness scores
    good = np.array([.51, .53, .55, .57])
    # similarity matrices
    simi_1 = np.array([
        [1, .9, .8, .7],
        [.9, 1, .6, .5],
        [.8, .6, 1, .4],
        [.7, .5, .4, 1],
    ])
    simi_2 = np.array([
        [1, .7, .8, .3],
        [.7, 1, .4, .2],
        [.8, .4, 1, .6],
        [.3, .2, .6, 1],
    ])
    # preference parameters
    lam = 0.4
    beta_1 = 0.25
    beta_2 = 0.75
    # compute
    simi = sqp.aggregate_matrices(simi_1, beta_1, simi_2, beta_2)
    weights, _ = sqp.get_weights(good, simi, lam)
    # check
    assert simi.shape == (4, 4)
    assert weights.shape == (4,)
