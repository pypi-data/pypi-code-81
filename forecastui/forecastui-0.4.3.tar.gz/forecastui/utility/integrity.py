from flask import current_app
import pathlib
from .settings_manager import SettingsManager

class Doctor:

    def __init__(self):
        self.__paths = {}

    def init(self):
        manager = SettingsManager()
        dirs = manager.getAll("Directories")
        for key, value in dirs.items():
            self.__paths[key] = pathlib.Path(value)

    def is_first_start(self):
        path = pathlib.Path.home() / ".config" / "forecastui" / "forecastui.conf"
        return not self.exists(path)
    
    def just_updated(self):
        import pkg_resources
        installed_version = pkg_resources.get_distribution("forecastui").version

        if self.is_first_start():
            return (False, installed_version, installed_version)

        manager = SettingsManager()
        conf_version = manager.get("App", "version")
        if conf_version != installed_version:
            return (True, conf_version, installed_version)
        else:
            return (False, conf_version, installed_version)


    def create_folders(self):
        for path in self.__paths.values():
            path.mkdir(parents=True, exist_ok=True)

    def exists(self, path):
        assert isinstance(path, pathlib.Path)
        return path.exists()
