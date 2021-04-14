from ..CommandHandler.Outcome.Failure import Failure


class ParsingJsonFailed(Failure):
    uuid = "1ac03ba3-1b72-488c-af79-aadda2b9dd4b"
    message = "Parsing request JSON failed."
    http_status_code = 400
