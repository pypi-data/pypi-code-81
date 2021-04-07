try:
    from .page import page
    from .search import search

except ModuleNotFoundError:
    pass

__version__ = "0.0.3"
