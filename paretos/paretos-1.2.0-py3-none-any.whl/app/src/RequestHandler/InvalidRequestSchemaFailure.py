from ..CommandHandler.Outcome.Failure import Failure


class InvalidRequestSchemaFailure(Failure):
    uuid = "69147172-c48d-4f25-a014-3885b789b9d1"
    message = "Request schema validation failed."
    http_status_code = 400
