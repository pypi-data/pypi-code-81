# local imports
from .base import JSONRPCBase

class JSONRPCException(Exception, JSONRPCBase):
    message = 'Unknown'

    def __init__(self, v):
       context_v = '{} error'.format(self.message)
       if v != None:
           context_v += ': ' + v

       super(JSONRPCException, self).__init__(context_v)


class JSONRPCCustomException(JSONRPCException):
    code = -32000
    message = 'Server'


class JSONRPCParseError(JSONRPCException):
    code = -32700
    message = 'Parse'


class JSONRPCInvalidRequestError(JSONRPCException):
    code = -32600
    message = 'Invalid request'


class JSONRPCMethodNotFoundError(JSONRPCException):
    code = -32601
    message = 'Method not found'


class JSONRPCInvalidParametersError(JSONRPCException):
    code = -32602
    message = 'Invalid parameters'


class JSONRPCInternalError(JSONRPCException):
    code = -32603
    message = 'Internal'


class JSONRPCUnhandledErrorException(KeyError):
    pass


class JSONRPCErrors:
    reserved_max = -31999
    reserved_min = -32768
    local_max = -32000
    local_min = -32099

    translations = {
        -32700: JSONRPCParseError,
        -32600: JSONRPCInvalidRequestError,
        -32601: JSONRPCMethodNotFoundError,
        -32602: JSONRPCInvalidParametersError,
        -32603: JSONRPCInternalError,
            }

    @classmethod
    def add(self, code, exception_object):
        if code < self.local_min or code > self.local_max:
            raise ValueError('code must be in range <{},{}>'.format(self.local_min, self.local_max))
        exc = self.translations.get(code)
        if exc != None:
            raise ValueError('code already registered with {}'.format(exc))

        if not issubclass(exception_object, JSONRPCCustomException):
            raise ValueError('exception object must be a subclass of jsonrpc_base.error.JSONRPCCustomException')

        self.translations[code] = exception_object


    @classmethod
    def get(self, code, v=None):
        e = self.translations.get(code)
        if e == None:
            raise JSONRPCUnhandledErrorException(code)
        return e(v)


class InvalidJSONRPCError(ValueError):
    pass
