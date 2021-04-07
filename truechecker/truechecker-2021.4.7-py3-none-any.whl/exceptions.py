class TrueCheckerException(Exception):
    pass


class BadRequest(TrueCheckerException):
    pass


class Unauthorized(BadRequest):
    pass


class BadState(BadRequest):
    pass


class ValidationError(BadRequest):
    pass


class NotFound(BadRequest):
    pass
