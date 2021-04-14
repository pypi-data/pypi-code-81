import traceback
from logging import LoggerAdapter

from werkzeug.exceptions import InternalServerError

from ..RequestHandler.JSend import JSend


class ErrorHandler:
    def __init__(self, application_protocol: JSend, logger: LoggerAdapter):
        self.__application_protocol: JSend = application_protocol
        self.__logger = logger

    def handle_error(self, exception: InternalServerError):
        trace = traceback.format_exc()
        self.__logger.error(str(exception.original_exception), error={"trace": trace})
        return self.__application_protocol.build_error_response(), 500
