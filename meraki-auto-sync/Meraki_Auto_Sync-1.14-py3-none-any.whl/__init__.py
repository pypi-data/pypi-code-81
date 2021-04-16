from ._metadata import *
from pkg_resources import get_distribution
from .Main import RUN
release = get_distribution('Meraki_Auto_Sync').version
__version__ = '.'.join(release.split('.')[:3])