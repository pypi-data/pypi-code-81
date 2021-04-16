import os

from envvarconf import BaseSettings
from envvarconf.converters.string_converter import StringConverter
from envvarconf.inspection import get_settings_variables
from envvarconf.loaders.base import BaseLoader


class Loader(BaseLoader):
    converter = StringConverter()

    def load(self, settings: BaseSettings):
        for varname, vartype in get_settings_variables(settings).items():
            if varname in os.environ:
                assert vartype is not None, f"{varname} is not typed. Probably there is error in settings definition."
                self.set_var(settings, varname, raw_value=os.environ[varname], vartype=vartype)
