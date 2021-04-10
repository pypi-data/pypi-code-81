from click import ClickException


class FlowfusicException(ClickException):
    def __init__(self, message=None):
        super(FlowfusicException, self).__init__(message)


class AuthenticationException(FlowfusicException):
    def __init__(
        self, message="Authentication failed. Retry by invoking flowfusic login."
    ):
        super(AuthenticationException, self).__init__(message=message)


class AuthorizationException(FlowfusicException):
    def __init__(self, response):
        try:
            message = response.json()["message"]
        except (KeyError, AttributeError):
            message = "You are not authorized to access this resource on Flowfusic."
        super(AuthorizationException, self).__init__(message=message)


class NotFoundException(FlowfusicException):
    def __init__(
        self,
        message="The resource you are looking for was not found."
        "Check if the name or id is correct.",
    ):
        super(NotFoundException, self).__init__(message=message)


class BadRequestException(FlowfusicException):
    def __init__(self, response):
        try:
            message = (
                "One or more request parameters is incorrect\n%s"
                % response.json()["message"]
            )
        except (KeyError, AttributeError):
            message = (
                "One or more request parameters is incorrect, %s" % response.content
            )
        super(BadRequestException, self).__init__(message=message)


class OverLimitException(FlowfusicException):
    def __init__(
        self,
        message="You are over the allowed limits for this operation."
        "Consider upgrading your account.",
    ):
        super(OverLimitException, self).__init__(message=message)


class ServerException(FlowfusicException):
    def __init__(self, message="Internal Flowfusic server error."):
        super(ServerException, self).__init__(message=message)


class BadGatewayException(FlowfusicException):
    def __init__(self, message="Invalid response from Flowfusic server."):
        super(BadGatewayException, self).__init__(message=message)


class GatewayTimeoutException(FlowfusicException):
    def __init__(self, message="Flowfusic server took too long to respond."):
        super(GatewayTimeoutException, self).__init__(message=message)


class WaitTimeoutException(FlowfusicException):
    def __init__(self, message="Timeout waiting for server state update."):
        super(WaitTimeoutException, self).__init__(message=message)


class LockedException(FlowfusicException):
    def __init__(self, message="Resource locked."):
        super(LockedException, self).__init__(message=message)
