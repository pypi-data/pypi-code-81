"""
TODO doc
"""

from pkg_resources import get_distribution

from ejerico_sdk.config import ConfigManager
from ejerico_sdk.logging import LoggingManager
from ejerico_sdk.stat import StatManager
from ejerico_sdk.annotations import singleton

__all__ = ["Bootstrap"]
__version__ = get_distribution("ejerico_sdk").version

@singleton
class Bootstrap(object):

    def __init__(self):
        self._config = None

    def boot(self, arguments):
        self.config = ConfigManager.instance()
        self.config.configURL = arguments.config_url
        self.config.configUSERNAME = arguments.config_username
        self.config.configPASSWORD = arguments.config_password
        self.config.configTOKEN = arguments.config_token
        self.config.configPATH = arguments.config_path
        self.config.boot()

        self.logging = LoggingManager.instance()
        self.logging.boot()

        self.stat= StatManager.instance()
        self.stat.boot()



