from .Failure import Failure


class NotFoundFailure(Failure):
    uuid = "79ef4b0e-ff5e-45e3-8128-d77a14b8fde5"
    message = "Resource not found."
    http_status_code = 404
