from pydoc import locate

from applipy_metrics.registry import MetricsRegistry

try:
    from applipy import (
        Config,
        Module,
    )
except ImportError:
    Config = object
    Module = object


class MetricsModule(Module):

    def __init__(self, config: Config):
        self._config = config

    def configure(self, bind, register):
        bind(self._registry_provider)

    def _registry_provider(self) -> MetricsRegistry:
        clock = self._config.get('metrics.clock')
        if clock:
            clock = locate(clock)
        summary_sample_provider = self._config.get('metrics.summary.sample_provider')
        if summary_sample_provider:
            summary_sample_provider = locate(summary_sample_provider)
        return MetricsRegistry(clock=clock, summary_sample_provider=summary_sample_provider)
