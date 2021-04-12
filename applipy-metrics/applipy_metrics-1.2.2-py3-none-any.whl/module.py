from logging import Logger
from pydoc import locate
from typing import List

from applipy_metrics.registry import MetricsRegistry
from applipy_metrics.reporters import Reporter

try:
    from applipy import (
        AppHandle,
        Config,
        Module,
        LoggingModule,
    )
except ImportError:
    AppHandle = object
    Config = object
    Module = object
    LoggingModule = None


class MetricsReportersAppHandle(AppHandle):

    def __init__(self, reporters: List[Reporter], logger: Logger):
        self._reporters = reporters
        self._logger = logger.getChild(f'{self.__module__}.{self.__class__.__name__}')

    async def on_start(self):
        for reporter in self._reporters:
            if reporter.start():
                self._logger.info(f'Started reporter {reporter.__module__}.{reporter.__class__.__name__}')
            else:
                self._logger.error(f'Failed to start reporter {reporter.__module__}.{reporter.__class__.__name__}')

    async def on_shutdown(self):
        for reporter in self._reporters:
            reporter.stop()


class MetricsModule(Module):

    def __init__(self, config: Config):
        self._config = config

    def configure(self, bind, register):
        bind(self._registry_provider)
        register(MetricsReportersAppHandle)

    def _registry_provider(self) -> MetricsRegistry:
        clock = self._config.get('metrics.clock')
        if clock:
            clock = locate(clock)
        summary_sample_provider = self._config.get('metrics.summary.sample_provider')
        if summary_sample_provider:
            summary_sample_provider = locate(summary_sample_provider)
        return MetricsRegistry(clock=clock, summary_sample_provider=summary_sample_provider)

    @classmethod
    def depends_on(cls):
        if LoggingModule:
            return LoggingModule,
        return ()
