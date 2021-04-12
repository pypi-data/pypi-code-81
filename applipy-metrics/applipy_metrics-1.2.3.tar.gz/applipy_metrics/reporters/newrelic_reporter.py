import time

from collections.abc import Mapping
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


class EmptyDict(Mapping):

    def __getitem__(self, key):
        raise KeyError(key)

    def __iter__(self):
        if False:
            yield None

    def __len__(self):
        return 0


_EMPTY_DICT = EmptyDict()


class NewRelicReporter(Reporter):

    _last_report_ts_ms: int
    _client: MetricClient
    _registry: MetricsRegistry
    _logger: Logger
    _last_snapshot: dict

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
        self._last_snapshot = _EMPTY_DICT

    def report_now(self, registry=None, timestamp=None):
        timestamp = (timestamp or time.time()) * 1000

        snapshot = (registry or self._registry).dump_metrics(True)
        metric_batch = []

        for metric, value in snapshot.items():
            prev = self._last_snapshot.get(metric, _EMPTY_DICT)
            if 'avg' in value:
                metric = SummaryMetric(metric.get_key(),
                                       value['count'] - prev.get('count', 0),
                                       value['sum'] - prev.get('sum', 0),
                                       value['min'],
                                       value['max'],
                                       None,
                                       tags=metric.get_tags())
            elif 'value' in value:
                metric = GaugeMetric(metric.get_key(),
                                     value['value'],
                                     tags=metric.get_tags())
            elif 'count' in value:
                metric = CountMetric(metric.get_key(),
                                     value['count'] - prev.get('count', 0),
                                     None,
                                     tags=metric.get_tags())
            else:
                continue

            metric_batch.append(metric)

        if metric_batch:
            common = {
                'timestamp': self._last_report_ts_ms,
                'interval.ms': 0,
                'attributes': self._common_tags,
            }
            response = self._client.send_batch(metric_batch, common)
            try:
                response.raise_for_status()
            except Exception:
                self._logger.exception('Error sending metrics batch')
                return

        self._last_report_ts_ms = timestamp
        self._last_snapshot = snapshot
