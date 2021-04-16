from benchmark.profilers import tools


class BaseProfiler(object):

    @property
    def measured_value(self):
        raise NotImplementedError('Abstract property.')

    @property
    def name(self):
        raise NotImplementedError('Abstract property.')

    @property
    def config(self):
        return self._config

    def __init__(self, c) -> None:
        self._config = c

    def run(self, *args):
        raise NotImplementedError('Abstract method.')

    def run_if_can(self, bench_name, description):
        for benchmark_filepath in self.get_available_benchmarks():
            if benchmark_filepath.name == bench_name:
                return self.run(benchmark_filepath, description)

    def get_available_benchmarks(self):
        return (
            f
            for f
            in tools.get_benchmarks(self.config.benchmarks_path())
            if f.stem.startswith(self.measured_value)
        )

    def run_benchmarks(self):
        return tools.multithreading(self.run, self.get_available_benchmarks(), 5)
