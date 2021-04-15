import sys
import inspect

from . import settings


class ExceptionHandler:
    """
    Exception handler is service, that actually raise specific exception based
    on response status code. If exception with given status code in not
    defined, raises ApiRemoteError exception
    """
    exceptions = None

    def __init__(self, exception_modules=settings.EXCEPTION_MODULES):

        self.exceptions = {}
        for module in exception_modules:
            for name, obj in inspect.getmembers(sys.modules[module],
                                                inspect.isclass):
                if issubclass(obj, ApiRemoteError) and \
                        hasattr(obj, 'status_code'):
                    self.exceptions[obj.status_code] = obj

    def handle(self, response):
        if response.status_code in self.exceptions:
            raise self.exceptions[response.status_code](response=response)
        else:
            raise ApiRemoteError(response=response)


class ApiException(Exception):
    """
    ApiException is parent exception so if you catch this exception you
    should catch them all
    """
    pass


class ResourceNotFound(ApiException):
    """
    ResourceNotFound exception is raised when child resource was not found.

    Usage::
    try:
        root = Roor('http://localhost:8000/api')
        foo_bar = root.resource('foo-bar')
    except ResourceNotFound:
        print('resource does not exists')
    else:
        data = foo_bar.get()
    """
    pass


class ApiConnectionError(ApiException):
    """
    Wrap all connection and socket exception
    """
    original_exception = None

    def __init__(self, *args, **kwargs):

        if 'original_exception' in kwargs:
            self.original_exception = kwargs.pop('original_exception')
        super().__init__(*args, **kwargs)


class ApiRemoteError(ApiException):
    """
    ApiRemoteError is parent for all exceptions that can carry and
    handle response object
    """
    response = None

    def __init__(self, *args, **kwargs):
        if 'response' in kwargs:
            self.response = kwargs.pop('response')
        super().__init__(*args, **kwargs)


class ValidationError(ApiRemoteError):
    """
    ValidationError exception handle 400 status code and try to parse
    errors out of response
    """
    status_code = 400
    errors = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            data = self.response.json()
        except (ValueError, TypeError):
            pass
        else:
            self.errors = data


class OKError(ApiRemoteError):
    """
    Represents Response 200 status code (https://httpstatuses.com/200)
    """
    status_code = 200


class CreatedError(ApiRemoteError):
    """
    Represents Response 201 status code (https://httpstatuses.com/201)
    """
    status_code = 201


class AcceptedError(ApiRemoteError):
    """
    Represents Response 202 status code (https://httpstatuses.com/202)
    """
    status_code = 202


class NoContentError(ApiRemoteError):
    """
    Represents Response 204 status code (https://httpstatuses.com/204)
    """
    status_code = 204


class NotModifiedError(ApiRemoteError):
    """
    Represents Response 304 status code (https://httpstatuses.com/304)
    """
    status_code = 304


class UnauthorizedError(ApiRemoteError):
    """
    Represents Response 401 status code (https://httpstatuses.com/401)
    """
    status_code = 401


class ForbiddenError(ApiRemoteError):
    """
    Represents Response 403 status code (https://httpstatuses.com/403)
    """
    status_code = 403


class NotFoundError(ApiRemoteError):
    """
    Represents Response 404 status code (https://httpstatuses.com/404)
    """
    status_code = 404


class MethodNotAllowedError(ApiRemoteError):
    """
    Represents Response 405 status code (https://httpstatuses.com/405)
    """
    status_code = 405


class NotAcceptableError(ApiRemoteError):
    """
    Represents Response 406 status code (https://httpstatuses.com/406)
    """
    status_code = 406


class ConflictError(ApiRemoteError):
    """
    Represents Response 409 status code (https://httpstatuses.com/409)
    """
    status_code = 409


class GoneError(ApiRemoteError):
    """
    Represents Response 410 status code (https://httpstatuses.com/410)
    """
    status_code = 410


class UnsupportedMediaTypeError(ApiRemoteError):
    """
    Represents Response 415 status code (https://httpstatuses.com/415)
    """
    status_code = 415


class KeepCalmError(ApiRemoteError):
    """
    Represents Response 429 status code (https://httpstatuses.com/429)
    """
    status_code = 429


class FatalError(ApiRemoteError):
    """
    Represents Response 500 status code (https://httpstatuses.com/500)
    """
    status_code = 500


class MaintenanceError(ApiRemoteError):
    """
    Represents Response 503 status code (https://httpstatuses.com/503)
    """
    status_code = 503


class BadGatewayError(ApiRemoteError):
    """
    Represents Response 502 status code (https://httpstatuses.com/502)
    """
    status_code = 502


class GatewayTimeoutError(ApiRemoteError):
    """
    Represents Response 504 status code (https://httpstatuses.com/504)
    """
    status_code = 504


class ApiMalformedResponseError(ApiRemoteError):
    """
    ApiMalformedResponseError is raised when body could not be parsed from
    response
    """


exception_handler = ExceptionHandler()
handle = exception_handler.handle
