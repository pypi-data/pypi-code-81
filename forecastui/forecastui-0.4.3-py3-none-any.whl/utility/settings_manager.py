import os
from configparser import SafeConfigParser, NoSectionError
import pathlib


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SettingsManager(metaclass=Singleton):

    def __init__(self):
        path = pathlib.Path.home() / ".config" / "forecastui"
        path.mkdir(parents=True, exist_ok=True)
        self.file = path / "forecastui.conf"
        self._config = SafeConfigParser()
        if not self.file.exists():
            open(self.file, 'a').close()
            self.default()

    def default(self):
        FORECAST_FOLDER = pathlib.Path.home() / "forecast"
        LOGS_FOLDER = FORECAST_FOLDER / "logs"
        PRESETS_FOLDER = FORECAST_FOLDER / "presets"
        import pkg_resources
        version = pkg_resources.get_distribution("forecastui").version

        self.set("App", "version", str(version))

        self.set("General", "dark", "false")
        self.set("General", "mode", 1)

        self.set("Directories", "forecast", str(FORECAST_FOLDER))
        self.set("Directories", "logs", str(LOGS_FOLDER))
        self.set("Directories", "presets", str(PRESETS_FOLDER))

    def _load_properties(self):
        with open(self.file, "r") as propertiesFile:
            self._config.read_file(propertiesFile)

    def _save_properties(self):
        with open(self.file, "w") as propertiesFile:
            self._config.write(propertiesFile)

    def get(self, section, option):
        self._load_properties()
        return self._config.get(section, option)

    def getAll(self, section=None):
        self._load_properties()
        if section is None:
            return dict(self._config.__dict__["_sections"].copy())
        else:
            return dict(self._config.__dict__["_sections"][section].copy())

    def set(self, section, option, value):
        option = str(option)
        value = str(value)
        try:
            self._config.set(section, option, value)
        except NoSectionError:
            self._config.add_section(section)
            self._config.set(section, option, value)
        self._save_properties()
