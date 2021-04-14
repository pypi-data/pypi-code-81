from time import time

from flask import Response, request
from jsonschema import ValidationError, validate
from werkzeug.exceptions import BadRequest

from ..CommandHandler.CommandHandler import CommandHandler
from ..CommandHandler.Outcome.Failure import Failure
from ..CommandHandler.Outcome.Success import Success
from ..Service.Logger import Logger
from .InvalidRequestSchemaFailure import InvalidRequestSchemaFailure
from .JSend import JSend
from .ParsingJsonFailed import ParsingJsonFailed


class RequestHandler:
    schema = {}
    __view_function_counter = 0

    def __init__(
        self,
        application_protocol: JSend,
        logger: Logger,
    ):
        self.__application_protocol = application_protocol
        self.__logger: Logger = logger

    def get_view_function(self, command_handler: CommandHandler):
        def view_function(*args, **kwargs):
            return self.__dispatch_request(command_handler)

        view_function.methods = command_handler.get_methods()
        view_function.provide_automatic_options = None
        view_function.__name__ = (
            str(RequestHandler.__view_function_counter)
            + "_"
            + command_handler.get_name()
        )

        RequestHandler.__view_function_counter += 1

        return view_function

    def __dispatch_request(self, command_handler: CommandHandler) -> (Response, int):
        command = command_handler.get_name()
        self.__logger.info("processing command", command=command)

        schema = command_handler.get_schema()
        request_data = None

        if request.method == "POST" and schema is not None:
            try:
                request_data = request.get_json(force=True)
            except BadRequest:
                return self.__fail(ParsingJsonFailed())

            valid, details = self.__validate_request_schema(request_data, schema)

            if not valid:
                return self.__fail(InvalidRequestSchemaFailure(details))

        start_time = time()
        outcome = command_handler.process(request_data)
        handling_duration = round(time() - start_time, 3)

        if isinstance(outcome, dict):
            # for convenience
            outcome = Success(outcome)

        if isinstance(outcome, Failure):
            self.__logger.info(
                "command handling failed",
                command_failure_id=outcome.get_id(),
                command_handling_duration_s=handling_duration,
            )

            response = self.__fail(outcome)
        elif isinstance(outcome, Success):
            self.__logger.info(
                "command handling succeeded",
                command_handling_duration_s=handling_duration,
            )

            response = self.__success(outcome.get_data())
        else:
            raise NotImplementedError()

        return response

    def __success(self, data: dict = None) -> (Response, int):
        return self.__application_protocol.build_success_response(data), 200

    def __fail(self, failure: Failure) -> (Response, int):
        return (
            self.__application_protocol.build_fail_response(failure),
            failure.http_status_code,
        )

    @staticmethod
    def __validate_request_schema(request_data, schema: dict) -> (bool, dict):
        try:
            validate(instance=request_data, schema=schema)
        except ValidationError as validation_error:
            return False, {
                "validationError": validation_error.message,
                "path": list(validation_error.absolute_path),
            }

        return True, {}
