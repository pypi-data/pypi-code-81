import sys
import time
from abc import ABCMeta
from subprocess import Popen, PIPE

from benchmark.profilers.profiler_type import ProfilerType
from .base import BaseProfiler
from .measured_value_type import MeasuredValueType
from .tools import get_current_time


class TimeProfiler(BaseProfiler, metaclass=ABCMeta):
    @property
    def measured_value(self):
        return MeasuredValueType.time.value

    @property
    def name(self):
        return ProfilerType.time.value

    def __init__(self, c) -> None:
        super().__init__(c)

    def print_benchmarks(self):
        print("get_available_benchmarks()")

    def run(self, *args):
        filepath, name = args

        print(f"run_time file: {filepath}")

        result = {
            "start_benchmark_sec": time.time(),
            "date": get_current_time()
            }

        with Popen(["python", filepath.as_posix()], stderr=PIPE, stdout=PIPE) as proc:
            out, err = proc.communicate()

        result['end_benchmark_sec'] = time.time()

        if err:
            print(filepath, err)

        result['benchmark_name'] = filepath.stem

        return result
