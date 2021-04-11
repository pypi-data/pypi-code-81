class AuthError(Exception):
    pass


class NotFound(Exception):
    pass


class Forbidden(Exception):
    pass


class Unauthorized(Exception):
    pass


class BadRequest(Exception):
    pass


class UnprocessableEntity(Exception):
    pass


class ServerError(Exception):
    pass


class OtherResponseError(Exception):
    pass


class ObjectError(Exception):
    pass


class CRUDError(Exception):
    pass