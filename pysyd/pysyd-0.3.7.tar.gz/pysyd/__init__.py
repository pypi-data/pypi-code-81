import os

from .functions import *
from .pipeline import *
from .models import *
from .target import *
from .plots import *
from .utils import *

__all__ = ['cli', 'functions', 'pipeline', 'models', 'target', 'plots', 'utils']

__version__ = '0.3.7'

_ROOT = os.path.abspath(os.path.dirname(__file__))
def get_path(path):
    return os.path.join(_ROOT, 'info', path)

TODODIR = get_path('todo.txt')
INFODIR = get_path('star_info.csv')