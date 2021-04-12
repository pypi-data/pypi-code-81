from logging import Logger, Handler
from typing import Optional

from applipy import Module, Config, LoggingModule
from applipy_metrics import MetricsModule, MetricsRegistry
from applipy_metrics.reporters import Reporter
from applipy_metrics.reporters.newrelic_reporter import NewRelicReporter

from newrelic_telemetry_sdk import (
    LogClient,
    MetricClient,
)

from .loghandler import NewRelicLogHandler


class NewRelicModule(Module):

    def __init__(self, config: Config) -> None:
        self._config = config['newrelic']

    def configure(self, bind, register) -> None:
        license = self._config['license']

        if self._config.get('logs.enabled', True):
            bind(LogClient, LogClient(license,
                                      host=self._config.get('logs.host'),
                                      port=self._config.get('logs.port', 443)))
            bind(Handler, NewRelicLogHandler)

        if self._config.get('metrics.enabled', True):
            bind(MetricClient, MetricClient(license,
                                            host=self._config.get('metrics.host'),
                                            port=self._config.get('metrics.port', 443)))
            bind(Reporter, self._metrics_reporter_provider)

    def _metrics_reporter_provider(self,
                                   global_config: Config,
                                   client: MetricClient,
                                   registry: MetricsRegistry,
                                   logger: Optional[Logger]) -> NewRelicReporter:
        reporting_interval = self._config.get('metrics.reporting_interval', 60)
        common_tags = dict(self._config.get('metrics.common_tags', {}))
        common_tags['app_name'] = global_config['app.name']
        return NewRelicReporter(client, registry, reporting_interval, common_tags, logger)

    @classmethod
    def depends_on(cls):
        return MetricsModule, LoggingModule
