# coding: utf-8

"""Stb-tester APIs for logging metrics to Prometheus.

Prometheus is an open-source monitoring & alerting tool.

These APIs offer a similar interface as the official `Prometheus Python
client`_ but the implementation is different: Your test scripts don't need to
start their own HTTP server for Prometheus to query.

.. _Prometheus Python client: https://github.com/prometheus/client_python

Copyright © 2018-2021 Stb-tester.com Ltd.

This file contains API stubs for local installation, to allow IDE linting &
autocompletion. The real implementation of these APIs is not open-source and it
requires the Stb-tester Node hardware.
"""

__all__ = [
    "Counter",
    "Histogram",
]

# pylint: disable=unused-argument


def _raise_premium(api_name):
    raise NotImplementedError(
        "`stbt.prometheus.%s` is a premium API only available to "
        "customers of Stb-tester.com Ltd. It requires *Stb-tester Node* "
        "hardware to run. "
        "See https://stb-tester.com for details on products and pricing. "
        "If you are receiving this error on the *Stb-tester Node* hardware "
        "contact support@stb-tester.com for help" % api_name)


class Counter(object):
    """Log a cumulative metric that increases over time, to the Prometheus
    database on your Stb-tester Portal.

    Prometheus is an open-source monitoring & alerting tool. A Prometheus
    Counter tracks counts of events or running totals. See `Metric Types`_ and
    `instrumentation best practices`_ in the Prometheus documentation.

    Example use cases for Counters:

    - Number of times the "buffering" indicator or "loading" spinner has
      appeared.
    - Number of frames seen with visual glitches or blockiness.
    - Number of VoD assets that failed to play.

    :param str name: A unique identifier for the metric. See `Metric names`_
       in the Prometheus documentation.

    :param str description: A longer description of the metric.

    Added in v32.

    .. _Metric Types: https://prometheus.io/docs/concepts/metric_types/
    .. _instrumentation best practices: https://prometheus.io/docs/practices/instrumentation/#counter-vs-gauge-summary-vs-histogram
    .. _Metric names: https://prometheus.io/docs/practices/naming/
    """
    def __init__(self, name, description):
        pass

    def inc(self, value=1, labels=None):
        """Increment the Counter by the given amount.

        :param int value: The amount to increase.

        :param Mapping[str,str] labels: Optional dict of ``label_name:
           label_value`` entries. See `Labels`_ in the Prometheus documentation.

           .. warning::

              Every unique combination of key-value label pairs represents a
              new time series, which can dramatically increase the amount of
              memory required to store the data on the Stb-tester Node, on the
              Stb-tester Portal, and on your Prometheus server. Do not use
              labels to store dimensions with high cardinality (many different
              label values), such as programme names or other unbounded sets of
              values.

        .. _Labels: https://prometheus.io/docs/practices/naming/#labels
        """
        _raise_premium("Counter")
        return None


class Gauge(object):
    """Log a numerical value that can go up and down, to the Prometheus
    database on your Stb-tester Portal.

    Prometheus is an open-source monitoring & alerting tool. A Prometheus
    Gauge tracks values like temperatures or current memory usage.

    :param str name: A unique identifier for the metric. See `Metric names`_
       in the Prometheus documentation.

    :param str description: A longer description of the metric.

    Added in v32.
    """
    def __init__(self, name, description):
        pass

    def set(self, value, labels=None):
        """Set the Gauge to the given value.

        :param float value: The measurement to record.
        :param Mapping[str,str] labels: See `stbt.prometheus.Counter`.
        """
        _raise_premium("Gauge")
        return None


class Histogram(object):
    """Log measurements, in buckets, to the Prometheus database on your
    Stb-tester Portal.

    Prometheus is an open-source monitoring & alerting tool. A Prometheus
    Histogram counts measurements (such as sizes or durations) into
    configurable buckets.

    Prometheus Histograms are commonly used for performance measurements:

    - Channel zapping time.
    - App launch time.
    - Time for VoD content to start playing.

    Prometheus Histograms allow reporting & alerting on particular quantiles.
    For example you could configure an alert if the 90th percentile of the
    above measurements exceeds a certain threshold (that is, the slowest 10% of
    requests are slower than the threshold).

    :param str name: A unique identifier for the metric. See `Metric names`_
       in the Prometheus documentation.

    :param str description: A longer description of the metric.

    :param Sequence[float] buckets: A list of numbers in increasing order,
       where each number is the upper bound of the corresponding bucket in the
       Histogram. With Prometheus you must specify the buckets up-front because
       the raw measurements aren't stored, only the counts of how many
       measurements fall into each bucket.

    Added in v32.
    """
    def __init__(self, name, description, buckets):
        pass

    def log(self, value, labels=None):
        """Store the given value into the Histogram.

        :param float value: The measurement to record.
        :param Mapping[str,str] labels: See `stbt.prometheus.Counter`.
        """
        _raise_premium("Histogram")
        return None
