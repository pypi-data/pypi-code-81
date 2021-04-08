# coding=utf-8
__version__ = "6.0.89"

from zuper_commons.logs import ZLogger

logger = ZLogger(__name__)
import os

path = os.path.dirname(os.path.dirname(__file__))

logger.debug(f"duckietown_challenges_cli version {__version__} path {path}")

from .cli import *
from .make_readme_templates import make_readmes_templates_main
from .make_readmes import make_readmes_main
