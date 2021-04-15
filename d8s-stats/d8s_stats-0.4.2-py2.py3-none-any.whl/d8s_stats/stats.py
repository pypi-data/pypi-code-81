import collections
import statistics
from typing import Any

from d8s_math import prod, string_to_number

StatsOverview = collections.namedtuple('StatsOverview', ['min', 'max', 'mean', 'mode', 'variance', 'stdev'])


def statistical_overview(
    data, *, data_is_sample: bool = False, result_if_no_mode: Any = None, raise_error_if_no_mode: bool = True
):
    """Return an overview of the data's statistical properties."""
    data = tuple(map(string_to_number, data))

    # calculate the mean once so that it can be passed into some of the functions later to expedite their execution
    data_mean = mean(data)

    data_variance = variance(data, data_mean=data_mean, data_is_sample=data_is_sample)
    data_stdev = stdev(data, data_mean=data_mean, data_is_sample=data_is_sample)

    overview = StatsOverview(
        min=min(data),
        max=max(data),
        mean=data_mean,
        mode=mode(data, result_if_no_mode=result_if_no_mode, raise_error_if_no_mode=raise_error_if_no_mode),
        variance=data_variance,
        stdev=data_stdev,
    )
    return overview


def mode(data, *, result_if_no_mode: Any = None, raise_error_if_no_mode: bool = True):
    """Return the item in the data which occurs the greatest number of times."""
    try:
        result = statistics.mode(data)
    except statistics.StatisticsError as e:
        if not raise_error_if_no_mode or (result_if_no_mode != None):
            result = result_if_no_mode
        else:
            raise e
    return result


# TODO: research the differences between the functions for samples and the functions for whole populations (e.g. variance_of_sample vs variance)
def variance(data, *, data_mean=None, data_is_sample: bool = False):
    """Return the variance of the data (assuming the data represents an entire population)."""
    data = tuple(map(string_to_number, data))

    if data_is_sample:
        result = statistics.variance(data, xbar=data_mean)
    else:
        result = statistics.pvariance(data, mu=data_mean)
    return result


def stdev(data, *, data_mean=None, data_is_sample: bool = False):
    """Return the standard deviation of the data (assuming the data represents an entire population)."""
    data = tuple(map(string_to_number, data))

    if data_is_sample:
        result = statistics.stdev(data, xbar=data_mean)
    else:
        result = statistics.pstdev(data, mu=data_mean)
    return result


# TODO: research the different means and what they mean ;)
def mean(iterable):
    """Return the average of the list."""
    iterable = map(string_to_number, iterable)

    # TODO: this could also be called "average"
    return statistics.mean(iterable)


def harmonic_mean(iterable):
    """Return the harmonic mean of the list."""
    iterable = map(string_to_number, iterable)

    return statistics.harmonic_mean(iterable)


def geometric_mean(iterable):
    """Return the geometric mean of the list."""
    iterable = tuple(map(string_to_number, iterable))

    return pow(prod(iterable), (1 / len(iterable)))
