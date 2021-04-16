import os
from subprocess import Popen, PIPE

from benchmark.profilers.profiler_type import ProfilerType
from .base import BaseProfiler
from .measured_value_type import MeasuredValueType
from .tools import get_benchmarks, multithreading, get_current_time


class PytestProfiler(BaseProfiler):
    @property
    def measured_value(self):
        return MeasuredValueType.time.value

    @property
    def name(self):
        return ProfilerType.pytest.value

    def __init__(self, c) -> None:
        super().__init__(c)

    def run(self, *args):
        filepath, name = args

        print(f"run_pytest file: {filepath}")
        results_path = os.path.join(self.config.results_path(), name)

        with Popen([
            "pytest",
            f"--benchmark-save={name}",
            "--benchmark-save-data",
            f"--benchmark-storage={results_path}",
            str(filepath)
        ], stderr=PIPE, stdout=PIPE) as proc:
            out, err = proc.communicate()

        if err:
            print(err.decode("utf-8"))

        out = out.decode("utf-8")
        print(out)
        return out

    def print_benchmarks(self):
        print("get_available_benchmarks()")

    def plot_pytest_benchmarks(self):
        print(f"plot_pytest_benchmarks")

        histogram_path = os.path.join(self.config.pytest_histogram_filename_prefix(),
                                      f"{self.name}_{get_current_time()}")

        with Popen([
            "pytest-benchmark",
            f"--histogram={histogram_path}",
            "compare",
            f"0 1 2 3 4 5 6",
        ], stderr=PIPE, stdout=PIPE) as proc:
            out, err = proc.communicate()

        if err:
            print(err.decode("utf-8"))

        out = out.decode("utf-8")
        print(out)
        return out

    def run_benchmarks(self):
        files = [(str(f), f.stem) for f in get_benchmarks(self.config.benchmarks_path()) if f.stem.startswith("test")]
        return multithreading(self.run, files, 5)
