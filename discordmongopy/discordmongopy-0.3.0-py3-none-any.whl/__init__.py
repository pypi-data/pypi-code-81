__title__ = 'discordmongopy'
__author__ = 'BongoPlayzYT'
__license__ = 'MIT'
__copyright__ = 'Copyright 2021 BongoPlayzYT'
__version__ = '0.3.0'

__path__ = __import__('pkgutil').extend_path(__path__, __name__)

from collections import namedtuple
import logging

from .mongo import Mongo
from .exceptions import NoIDPassed

VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')

version_info = VersionInfo(major=0, minor=3, micro=0, releaselevel='final', serial=0)

logging.getLogger(__name__).addHandler(logging.NullHandler())
