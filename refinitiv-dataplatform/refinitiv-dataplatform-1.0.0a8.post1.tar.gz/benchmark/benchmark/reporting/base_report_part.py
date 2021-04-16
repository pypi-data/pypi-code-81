import abc


class BaseReportPart(abc.ABC):

    @property
    def env(self):
        return self._report_manager.env

    @property
    def config(self):
        return self._config

    def __init__(self, report_manager, config):
        self._config = config
        self._report_manager = report_manager

    @abc.abstractmethod
    def render(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def dump(self, fp, *args, **kwargs):
        pass
