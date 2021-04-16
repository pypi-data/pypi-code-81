from benchmark.config.basic_config import BasicConfig


class PytestConfig(BasicConfig):

    def results_path(self):
        return self._get_option('profilers.pytest', 'path')

    def pytest_histogram_filename_prefix(self):
        return self._get_option('profilers.pytest', 'histogram_filename_prefix')
