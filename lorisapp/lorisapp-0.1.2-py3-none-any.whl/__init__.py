"""
"""

__author__ = """gucky92"""
__email__ = 'gucky@gucky.eu'
__version__ = '0.1.2'

import os

from loris.settings import Config
from loris.errors import LorisError

os.environ['DJ_SUPPORT_ADAPTED_TYPES'] = "TRUE"

loris_config_file = os.environ.get('LORIS_CONFIG_FILE', None)

config = Config.load(loris_config_file)
conn = config.conn


from loris.database.users import (
    grantuser, grantprivileges, dropuser, change_password
)


class DataBase:

    def __init__(self, config):
        self.config = config

    def __getattr__(self, name):

        if (
            ('config' in vars(self))
            and (name in self.config['schemata'])
        ):
            return self.config['schemata'][name]
        else:
            raise AttributeError(f"No database schema of name `{name}`.")


db = DataBase(config)


__all__ = [
    'config',
    'conn',
    'Config',
    'LorisError',
    'df',
    'grantuser',
    'grantprivileges',
    'dropuser',
    'change_password',
    'db'
]
