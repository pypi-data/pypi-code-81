"""Top-level package for PyProcSync."""

__author__ = """Marcell Pünkösd"""
__email__ = 'punkosdmarcell@rocketmail.com'
__version__ = '0.1.0'

from .pyprocsync import ProcSync  # noqa: F401
from .exceptions import ProcSyncError, TooLateError, TimeOutError  # noqa: F401
