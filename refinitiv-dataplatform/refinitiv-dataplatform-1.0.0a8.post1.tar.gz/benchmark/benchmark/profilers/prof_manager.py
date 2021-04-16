from lazy import lazy

from .measured_value_type import MeasuredValueType
from .mprof_prof import MProfProfiler
from .profiler_type import ProfilerType
from .pytest_prof import PytestProfiler
from .timeit_prof import TimeitProfiler
from .time_prof import TimeProfiler


class ProfilersManager(object):
    @lazy
    def timeit_prof(self):
        return TimeitProfiler(self.config_manager.timeit_config)

    @lazy
    def pytest_prof(self):
        return PytestProfiler(self.config_manager.pytest_config)

    @lazy
    def mprof_prof(self):
        return MProfProfiler(self.config_manager.mprof_config)

    @lazy
    def time_prof(self):
        return TimeProfiler(self.config_manager.time_config)

    @lazy
    def profilers_by_type(self):
        _profilers_by_type = {
            ProfilerType.timeit: self.timeit_prof,
            ProfilerType.pytest: self.pytest_prof,
            ProfilerType.mprof: self.mprof_prof,
            ProfilerType.time: self.time_prof,
        }
        return _profilers_by_type

    @lazy
    def profilers_by_measured_value(self):
        _profilers_by_measured_value = {
            MeasuredValueType.time: (
                self.timeit_prof,
                self.pytest_prof,
            ),
            MeasuredValueType.memory: (
                self.mprof_prof,
            )
        }
        return _profilers_by_measured_value

    @property
    def config_manager(self):
        return self._config_manager

    def __init__(self, config_manager) -> None:
        self._config_manager = config_manager

    def get_profilers_by_measured_value(self, measured_value):
        if isinstance(measured_value, MeasuredValueType):
            return self.profilers_by_measured_value[measured_value]
        elif isinstance(measured_value, str):
            return self.profilers_by_measured_value[MeasuredValueType[measured_value]]
        else:
            return None

    def get_profiler_by_type(self, prof_type):
        if isinstance(prof_type, str):
            return self.profilers_by_type[ProfilerType[prof_type]]
        elif isinstance(prof_type, ProfilerType):
            return self.profilers_by_type[prof_type]
        else:
            return None
