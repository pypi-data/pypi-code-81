import os
import simple_utils
from simple_utils import logging

def test_logging():
    logging.warning('hello', 'world', {'abc'})
