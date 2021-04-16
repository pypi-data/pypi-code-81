import pathlib


class BasicConfig(object):

    @property
    def config_benchmark(self):
        return self._manager.config_benchmark

    @property
    def config_file(self):
        return self._manager.config_file

    @property
    def config_console(self):
        return self._manager.config_console

    def __init__(self, manager):
        self._manager = manager

    def _get_option(self, section, option="", fromc='file'):
        if fromc == 'file':
            return self.config_file.get(section, option, fallback=None)
        elif fromc == 'console':
            return self.config_console.get(section)

    def get_web_host(self):
        return self._get_option('web', 'host')

    def get_web_port(self):
        return self._get_option('web', 'port')

    def get_web_log_level(self):
        return self._get_option('web', 'log')

    def get_web_app_name(self):
        return self._get_option('web', 'name')

    def storage_name(self):
        return self._get_option('storage', 'name')

    def storage_location(self):
        return self._get_option('storage', 'location')

    def benchmarks_path(self):
        return pathlib.Path("./benchmark").resolve() / self._get_option('profilers', 'benchmarks')

    def get_available_profilers(self):
        value = self._get_option('profilers', 'available')
        profs = [v for v in value.split("\n") if v]
        return profs

    def get_available_measures(self):
        value = self._get_option('profilers', 'available.measures')
        measures = [v for v in value.split("\n") if v]
        return measures

    def parse_config_console(self, argv):
        return None
