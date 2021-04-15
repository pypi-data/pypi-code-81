from statistics import StatisticsError

import pytest

from d8s_stats import (
    statistical_overview,
    mode,
    variance,
    stdev,
    mean,
    harmonic_mean,
    geometric_mean,
    StatsOverview,
)


def test_geometric_mean_docs_1():
    assert geometric_mean([1, 2, 3]) == 1.8171205928321397
    assert geometric_mean(['1', 2, 3]) == 1.8171205928321397
    assert geometric_mean([1, 1, 2, 3, 5]) == 1.97435048583482
    assert geometric_mean([-1, 0, 1]) == 0.0


def test_harmonic_mean_docs_1():
    assert harmonic_mean([1, 2, 3]) == 1.6363636363636365
    assert harmonic_mean(['1', 2, 3]) == 1.6363636363636365
    assert harmonic_mean([1, 1, 2, 3, 5]) == 1.6483516483516483
    with pytest.raises(StatisticsError):
        harmonic_mean([-1, 0, 1])


def test_mean_docs_1():
    assert mean([1, 2, 3]) == 2
    assert mean(['1', 2, 3]) == 2
    assert mean([1, 1, 2, 3, 5]) == 2.4
    assert mean([-1, 0, 1]) == 0


def test_mode_docs_1():
    assert mode([1, 2, 2]) == 2
    assert mode(['a', 'a', 0]) == 'a'

    # this does different things based on the python version... in <3.8 it will raise a StatisticsError; in >= 3.8 it will return 1
    # with pytest.raises(StatisticsError):
    #     mode([1, 2])

    assert mode([1, 2], raise_error_if_no_mode=False) == None
    assert mode([1, 2], result_if_no_mode='foo') == 'foo'


def test_statistical_overview_docs_1():
    assert statistical_overview([0, 1, 2, 2]) == StatsOverview(
        min=0, max=2, mean=1.25, mode=2, variance=0.6875, stdev=0.82915619758885
    )
    assert statistical_overview([0, 1, 2, 2], data_is_sample=True) == StatsOverview(
        min=0, max=2, mean=1.25, mode=2, variance=0.9166666666666666, stdev=0.9574271077563381
    )
    assert statistical_overview([0, '1', 2, '2']) == StatsOverview(
        min=0, max=2, mean=1.25, mode=2, variance=0.6875, stdev=0.82915619758885
    )
