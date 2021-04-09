# local imports
from .base import JSONRPCBase


class JSONRPCException(Exception, JSONRPCBase):
    message = 'Unknown'

    def __init__(self, v, request_id=None):
       context_v = '{} error'.format(self.message)
       if v != None:
           context_v += ': ' + v

       self.request_id = request_id

       super(JSONRPCException, self).__init__(context_v)

    # Thanks to https://stackoverflow.com/questions/35282222/in-python-how-do-i-cast-a-class-object-to-a-dict
    def __iter__(self):
        if self.request_id == None:
            raise AttributeError('request id cannot be undefined when serializing error')
        yield 'jsonrpc', JSONRPCBase.version_string
        yield 'id', self.request_id
        yield 'error', {
                'code': self.code,
                'message': str(self),
                }


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
