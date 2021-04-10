import time

from logging import (
    Logger,
    getLogger,
)
from typing import (
    Dict,
    Optional,
)

from applipy_metrics import MetricsRegistry
from .reporter import Reporter

from newrelic_telemetry_sdk import (
    MetricClient,
    CountMetric,
    GaugeMetric,
    SummaryMetric,
)


class NewRelicReporter(Reporter):

    _last_report_ts_ms: int
    _client: MetricClient
    _registry: MetricsRegistry
    _logger: Logger

    def __init__(
        self,
        client: MetricClient,
        registry: MetricsRegistry,
        reporting_interval: int,
        common_tags: Dict[str, str],
        logger: Optional[Logger],
    ):
        super().__init__(registry, reporting_interval)
        self._last_report_ts_ms = time.time() * 1000
        self._common_tags = common_tags
        self._client = client
        self._registry = registry
        if not logger:
            logger = getLogger()
        self._logger = logger.getChild(f'{self.__module__}.{self.__class__.__name__}')

    def report_now(self, registry=None, timestamp=None):
        timestamp = (timestamp or time.time()) * 1000
        interval_ms = timestamp - self._last_report_ts_ms

        snapshot = (registry or self._registry).dump_metrics(True)
        metric_batch = []

        for metric, value in snapshot.items():
            if 'avg' in value:
                metric = SummaryMetric(metric.get_key(), value['count'], value['sum'], value['min'], value['max'],
                                       interval_ms, tags=metric.get_tags(), end_time_ms=timestamp)
            elif 'value' in value:
                metric = GaugeMetric(metric.get_key(), value['value'], tags=metric.get_tags(), end_time_ms=timestamp)
            elif 'count' in value:
                metric = CountMetric(metric.get_key(), value['count'], interval_ms, tags=metric.get_tags(),
                                     end_time_ms=timestamp)
            else:
                continue

            metric_batch.append(metric)

        if metric_batch:
            response = self._client.send_batch(metric_batch, self._common_tags)
            try:
                response.raise_for_status()
            except Exception:
                self._logger.exception('Error sending metrics batch')
                return

        self._last_report_ts_ms = timestamp
