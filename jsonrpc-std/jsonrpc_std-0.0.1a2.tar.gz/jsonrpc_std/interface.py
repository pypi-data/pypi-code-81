# standard imports
import uuid

# local imports
from .base import JSONRPCBase
from .error import (
        JSONRPCErrors,
        )


class DefaultErrorParser:

    def translate(self, error):
        code = error['error']['code']
        message = error['error']['message']
        if type(code).__name__ != 'int':
            raise ValueError('error code is not int by {} in error {}'.format(type(code), error))
        
        exc = None
        try:
            exc = JSONRPCErrors.get(code, message)
        except KeyError:
            return JSONRPCUndefinedError(code, message)


def jsonrpc_template(request_id=None):
    if request_id == None:
        request_id = str(uuid.uuid4())

    return {
        'jsonrpc': JSONRPCBase.version_string,
        'id': request_id,
        'method': None,
        'params': [],
            }


def jsonrpc_request(method, request_id=None):
    req = jsonrpc_template(request_id=request_id)
    req['method'] = method
    return req


def jsonrpc_result(o, ep):
    if o.get('error') != None:
        raise ep.translate(o)
    return o['result']


def jsonrpc_response(request_id, result):
    return {
        'jsonrpc': JSONRPCBase.version_string,
        'id': request_id,
        'result': result,
        }


def jsonrpc_error(request_id, code, message=None):
    e = JSONRPCErrors.get(code, message)
    return {
        'jsonrpc': JSONRPCBase.version_string,
        'id': request_id,
        'error': {
            'code': code,
            'message': str(e),
            },
        }


def jsonrpc_is_response_to(request, response):
    return request['id'] == response['id']



