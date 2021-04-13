from .insert_data import insert_data
from .get_data import get_data

# if somebody does "from somepackage import *", this is what they will
# be able to access:
__all__ = [
    'insert_data',
    'get_data',
]
