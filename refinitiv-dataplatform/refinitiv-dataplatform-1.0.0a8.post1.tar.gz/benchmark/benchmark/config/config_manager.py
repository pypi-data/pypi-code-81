from lazy import lazy

from .basic_config import BasicConfig
from .mprof_config import MProfConfig
from .pytest_config import PytestConfig
from .report_config import ReportConfig
from .chart_config import LineChartConfig, ColumnChartConfig, HistogramConfig
from .config_provider import ConfigFileProvider


class ConfigManager(object):

    def __init__(self, configfile_name) -> None:
        self._configfile_name = configfile_name

    @lazy
    def config_file(self):
        _configfile_provider = ConfigFileProvider(self._configfile_name)
        return _configfile_provider.get_config()

    @lazy
    def config_benchmark(self):
        return ""

    @lazy
    def config_console(self):
        return {}

    @lazy
    def basic_config(self):
        return BasicConfig(self)

    @lazy
    def mprof_config(self):
        return MProfConfig(self)

    @lazy
    def pytest_config(self):
        return PytestConfig(self)

    @lazy
    def timeit_config(self):
        return self.basic_config

    @lazy
    def time_config(self):
        return self.basic_config

    @lazy
    def report_config(self):
        return ReportConfig(self)

    @lazy
    def line_chart_config(self):
        return LineChartConfig(self)

    @lazy
    def column_chart_config(self):
        return ColumnChartConfig(self)

    @lazy
    def histogram_config(self):
        return HistogramConfig(self)

    @lazy
    def configs(self):
        return [
            self.basic_config,
            self.mprof_config,
            self.pytest_config,
            self.report_config,
            self.line_chart_config,
            ]

    def parse_config_console(self, s):
        for c in self.configs:
            c.parse_config_console(s)

    def parse_config_benchmark(self, s):
        if s:
            self.config_benchmark += f" {s}"
