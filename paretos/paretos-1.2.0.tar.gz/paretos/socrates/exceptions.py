from paretos.exceptions import ParetosError


class ResponseParsingError(ParetosError):
    pass


class InvalidResponseStructure(ParetosError):
    pass


class RequestFailed(ParetosError):
    pass
