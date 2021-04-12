from ..exceptions import ForecastFlowError


class APIFailed(ForecastFlowError):
    """
    Base Exception of firebase_api package.
    """

    ...


class NotFound(APIFailed):
    ...


class PermissionDenied(APIFailed):
    ...
