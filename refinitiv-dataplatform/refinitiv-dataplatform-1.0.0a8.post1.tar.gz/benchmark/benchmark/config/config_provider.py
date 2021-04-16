import os
from configparser import ConfigParser, ExtendedInterpolation


class ConfigFileProvider(object):
    def __init__(self, configfile_name) -> None:
        self._configfile_name = configfile_name
        self._fileconfig = None

    def get_config(self):
        if self._fileconfig is None:

            if not os.path.isfile(self._configfile_name):
                print("config.ini not exists and will be created.")
                with open(self._configfile_name, 'w') as f:
                    c = ConfigParser(interpolation=ExtendedInterpolation())
                    c.write(f)

            c = ConfigParser(interpolation=ExtendedInterpolation())
            c.read_file(open(self._configfile_name))
            self._fileconfig = c
        return self._fileconfig
