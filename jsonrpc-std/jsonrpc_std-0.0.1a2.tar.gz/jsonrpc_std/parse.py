# standard imports
import json

# local imports
from .base import JSONRPCBase
from .error import (
        JSONRPCParseError,
        JSONRPCInvalidRequestError,
        )
from .interface import (
        jsonrpc_request,
        )


def jsonrpc_validate_dict(o):
    version = o.get('jsonrpc')
    if version == None:
        raise JSONRPCParseError('missing jsonrpc version field')
    elif version != JSONRPCBase.version_string:
        raise JSONRPCInvalidRequestError('Invalid version {}'.format(version))

    method = o.get('method')
    if method == None:
        raise JSONRPCParseError('missing method field')
    elif type(method).__name__ != 'str':
        raise JSONRPCInvalidRequestError('method must be str')

    params = o.get('params')
    if params == None:
        raise JSONRPCParseError('missing params field')
    elif type(params).__name__ != 'list':
        raise JSONRPCParseError('params field must be array')

    request_id = o.get('id')
    if request_id == None:
        raise JSONRPCParseError('missing id field')
    if type(request_id).__name__ not in ['str', 'int']:
        raise JSONRPCInvalidRequestError('invalid id value, must be string or integer')

    return o 


def jsonrpc_from_str(s):
    o = json.loads(s)
    return jsonrpc_from_dict(o)


def jsonrpc_from_dict(o):
    o_parsed = jsonrpc_validate_dict(o)
    req = jsonrpc_request(o_parsed['method'], request_id=o_parsed['id'])
    req['params'] = o_parsed['params']
    return req


def jsonrpc_from_file(f):
    o = json.load(f)
    return jsonrpc_from_dict(o)
