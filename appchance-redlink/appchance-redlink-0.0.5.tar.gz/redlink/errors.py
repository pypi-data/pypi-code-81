class RedlinkError(Exception):
    pass


class RedlinkAuthorizationError(RedlinkError):
    """
    Authorization data is invalid
    """


class RedlinkNotFoundError(RedlinkError):
    """
    Request was successfully processed but no results were returned
    """


class RedlinkServerError(RedlinkError):
    """
    Request was not processed due to server error
    """
