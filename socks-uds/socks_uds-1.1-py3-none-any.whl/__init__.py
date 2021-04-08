__version__ =  '1.1'

from .socks import *


def has_httpcore():
    try:
        import httpcore
        return True
    except ImportError:
        return False


if has_httpcore():
    from .httpcore_wrapper import *
