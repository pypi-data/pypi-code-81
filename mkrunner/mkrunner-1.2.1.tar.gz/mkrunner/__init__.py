__version__ = "1.2.1"
__description__ = "One-stop solution for HTTP(S) testing."

# import firstly for monkey patch if needed
from mkrunner.ext.locust import main_locusts
from mkrunner.parser import parse_parameters as Parameters
from mkrunner.runner import mkrunner
from mkrunner.testcase import Config, Step, RunRequest, RunTestCase
from mkrunner.log import logger



__all__ = [
    "logger",
    "__version__",
    "__description__",
    "mkrunner",
    "Config",
    "Step",
    "RunRequest",
    "RunTestCase",
    "Parameters",
]
