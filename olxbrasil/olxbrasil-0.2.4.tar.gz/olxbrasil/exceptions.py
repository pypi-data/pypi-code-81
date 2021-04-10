class OlxRequestError(Exception):
    """Raised when is not possible to do a successful request to OLX"""

    pass


class FilterNotFoundError(Exception):
    """Raised when a filter was passed wrongly"""

    pass
