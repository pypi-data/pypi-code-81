import re
import time
from .meters import Counter, Summary, Gauge, CallbackGauge, SimpleGauge, BaseMetric


class MetricsRegistry(object):

    """
    A single interface used to gather metrics on a service. It keeps track of
    all the relevant Counters, Summaries, and Gauges. It does not have
    a reference back to its service. The service would create a
    L{MetricsRegistry} to manage all of its metrics tools.
    """

    def __init__(self, clock=None, summary_sample_provider=None):
        """
        Creates a new L{MetricsRegistry} instance.
        """
        self._counters = {}
        self._summaries = {}
        self._gauges = {}
        self._clock = clock or time
        self._summary_sample_provider = summary_sample_provider or (lambda _: None)

    def add(self, key, metric, tags=None):
        """
        Use this method to manually add custom metric instances to the registry
        which are not created with their constructor's default arguments,
        e.g. Summary with a different size.

        :param key: name of the metric
        :type key: C{str}
        :param metric: instance of Summary, Gauge or Counter
        :param tags: tags attached to the metric (e.g. {'region': 'us-west-1'})
        :type tags: C{dict}

        """
        class_map = (
            (Summary, self._summaries),
            (Gauge, self._gauges),
            (Counter, self._counters),
        )
        for cls, registry in class_map:
            if isinstance(metric, cls):
                metric_key = BaseMetric(key, tags)
                if metric_key in registry:
                    raise LookupError("Metric %r already registered" % key)
                registry[metric_key] = metric
                return
        raise TypeError("Invalid class. Could not register metric %r" % key)

    def counter(self, key, tags=None):
        """
        Gets a counter based on a key, creates a new one if it does not exist.

        :param key: name of the metric
        :type key: C{str}

        :param tags: tags attached to the counter (e.g. {'region': 'us-west-1'})
        :type tags: C{dict}

        :return: L{Counter}
        """
        metric_key = BaseMetric(key, tags)
        if metric_key not in self._counters:
            self._counters[metric_key] = Counter(key=key, tags=tags)
        return self._counters[metric_key]

    def summary(self, key, tags=None):
        """
        Gets a summary based on a key, creates a new one if it does not exist.

        :param key: name of the metric
        :type key: C{str}

        :param tags: tags attached to the summary (e.g. {'region': 'us-west-1'})
        :type tags: C{dict}

        :return: L{Summary}
        """
        metric_key = BaseMetric(key, tags)
        if metric_key not in self._summaries:
            self._summaries[metric_key] = Summary(key=key,
                                                  clock=self._clock,
                                                  tags=tags,
                                                  sample=self._summary_sample_provider(self._clock))
        return self._summaries[metric_key]

    def gauge(self, key, gauge=None, default=float("nan"), tags=None):
        metric_key = BaseMetric(key, tags)
        if metric_key not in self._gauges:
            if gauge is None:
                gauge = SimpleGauge(
                    key=key,
                    value=default,
                    tags=tags
                )  # raise TypeError("gauge required for registering")
            elif not isinstance(gauge, Gauge):
                if not callable(gauge):
                    raise TypeError("gauge getter not callable")
                gauge = CallbackGauge(key=key, callback=gauge, tags=tags)
            self._gauges[metric_key] = gauge
        return self._gauges[metric_key]

    def create_sink(self):
        return None

    def clear(self):
        self._counters.clear()
        self._gauges.clear()
        self._summaries.clear()

    def _get_counter_metrics(self, metric_key):
        if metric_key in self._counters:
            counter = self._counters[metric_key]
            results = {"count": counter.get_count()}
            return results
        return {}

    def _get_gauge_metrics(self, metric_key):
        if metric_key in self._gauges:
            gauge = self._gauges[metric_key]
            result = {"value": gauge.get_value()}
            return result
        return {}

    def _get_summary_metrics(self, metric_key):
        if metric_key in self._summaries:
            summary = self._summaries[metric_key]
            snapshot = summary.get_snapshot()
            res = {
                "avg": snapshot.get_mean(),
                "count": summary.get_count(),
                "max": snapshot.get_max(),
                "min": snapshot.get_min(),
                "sum": summary.get_sum(),
                "std_dev": snapshot.get_stddev(),
                "75_percentile": snapshot.get_75th_percentile(),
                "95_percentile": snapshot.get_95th_percentile(),
                "99_percentile": snapshot.get_99th_percentile(),
                "999_percentile": snapshot.get_999th_percentile(),
            }
            return res
        return {}

    def get_metrics(self, key, tags=None):
        """
        Gets all the metrics for a specified key.

        :param key: name of the metric
        :type key: C{str}

        :param tags: tags attached to the metric (e.g. {'region': 'us-west-1'})
        :type tags: C{dict}

        :return: C{dict}
        """
        return self._get_metrics_by_metric_key(BaseMetric(key, tags))

    def _get_metrics_by_metric_key(self, metric_key):
        metrics = {}
        for getter in (
            self._get_counter_metrics,
            self._get_summary_metrics,
            self._get_gauge_metrics,
        ):
            metrics.update(getter(metric_key))
        return metrics

    def dump_metrics(self, key_is_metric=False):
        """
        Formats all of the metrics and returns them as a dict.

        :param key_is_metric: True if the resulting dict's keys are the metric objects themselves,
        False if the keys are names only (thus effectively ignoring tags)

        :return: C{list} of C{dict} of metrics
        """
        metrics = {}
        for metric_type in (
            self._counters,
            self._summaries,
            self._gauges,
        ):
            for metric_key in metric_type.keys():
                if key_is_metric:
                    key = metric_key
                else:
                    key = metric_key.get_key()

                metrics[key] = self._get_metrics_by_metric_key(metric_key)

        return metrics


# TODO make sure tags are supported properly
class RegexRegistry(MetricsRegistry):

    """
    A single interface used to gather metrics on a service. This class uses a regex to combine
    measures that match a pattern. For example, if you have a REST API, instead of defining
    a summary for each method, you can use a regex to capture all API calls and group them.
    A pattern like '^/api/(?P<model>)/\\d+/(?P<verb>)?$' will group and measure the following:
        /api/users/1 -> users
        /api/users/1/edit -> users/edit
        /api/users/2/edit -> users/edit
    """

    def __init__(self, pattern=None, clock=time):
        super(RegexRegistry, self).__init__(clock)
        if pattern is not None:
            self.pattern = re.compile(pattern)
        else:
            self.pattern = re.compile("^$")

    def _get_key(self, key):
        matches = self.pattern.finditer(key)
        key = "/".join((v for match in matches for v in match.groups() if v))
        return key

    def summary(self, key, tags=None):
        return super(RegexRegistry, self).summary(key=self._get_key(key), tags=tags)

    def counter(self, key, tags=None):
        return super(RegexRegistry, self).counter(key=self._get_key(key), tags=tags)

    def gauge(self, key, gauge=None, default=float("nan"), tags=None):
        return super(RegexRegistry, self).gauge(
            key=self._get_key(key),
            gauge=gauge,
            default=default,
            tags=tags
        )


_global_registry = MetricsRegistry()


def global_registry():
    return _global_registry


def set_global_registry(registry):
    global _global_registry
    _global_registry = registry


def counter(key, tags=None):
    return _global_registry.counter(key, tags)


def summary(key, tags=None):
    return _global_registry.summary(key, tags)


def gauge(key, gauge=None, tags=None):
    return _global_registry.gauge(key=key, gauge=gauge, tags=tags)


def dump_metrics():
    return _global_registry.dump_metrics()


def clear():
    return _global_registry.clear()
