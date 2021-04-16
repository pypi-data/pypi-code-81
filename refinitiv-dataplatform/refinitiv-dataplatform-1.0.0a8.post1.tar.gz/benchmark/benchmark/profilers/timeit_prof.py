import json
import statistics
import time
from abc import ABCMeta
from subprocess import Popen, PIPE

from benchmark.profilers.profiler_type import ProfilerType
from .base import BaseProfiler
from .measured_value_type import MeasuredValueType
from .tools import get_current_time


class TimeitProfiler(BaseProfiler, metaclass=ABCMeta):
    @property
    def measured_value(self):
        return MeasuredValueType.time.value

    @property
    def name(self):
        return ProfilerType.timeit.value

    def __init__(self, c) -> None:
        super().__init__(c)

    def print_benchmarks(self):
        print("get_available_benchmarks()")

    def run(self, *args):
        filepath, name = args

        """
            Example:
            [
                {
                    'start_benchmark_sec': 1578566900.2307787,
                    'end_benchmark_sec': 1578566904.4724925,
                    'benchmark_name': 'time_esg_get_universe',
                    'data': [
                        0.007185599999999681, 0.002207000000000292,
                        0.012281699999999951, 0.002200000000000202,
                        0.002217899999999773, 0.002182699999999649,
                        0.0022417000000007903, 0.002190799999999271,
                        0.002157099999999801, 0.002178500000000305
                    ]
                }
            ]
        :param filename:
        :return: list
        """

        print(f"run_timeit file: {filepath}")

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

        data = json.loads(out)

        result['data'] = data

        result['num_runs'] = len(data)
        result['median_sec'] = statistics.median(data)
        result['mean_sec'] = statistics.mean(data)
        result['stdev_sec'] = statistics.stdev(data)

        return result
