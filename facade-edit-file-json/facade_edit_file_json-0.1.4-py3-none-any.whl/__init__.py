
from pkg_resources import get_distribution, DistributionNotFound
try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:  # package is not installed
    __version__ = None
from .cli import FACADE_EDIT_FILE_JSON

__all__ = [FACADE_EDIT_FILE_JSON]