import datetime
import configuration

from bravaweb.utils import ResponseCode

from bravaweb.utils.log import *


async def View(enviroment, data, **args):

    Debug(f"View: Start Response Type {enviroment.response_type.__name__}")

    if not "token" in args and enviroment.auth_token:
        args["token"] = enviroment.auth_token

    response = enviroment.response_type()

    content = response.Response(data=data, route=enviroment.route, action=enviroment.action, **args)

    _headers = [
        response.header,
        (b"Content-Length", str(len(content)).encode(configuration.api.encoding)),
        (b"Accept-Ranges", b"bytes"),
        (b"X-Frame-Options", b"Deny")
    ]

    if enviroment.origin:
        _headers.append((b"Access-Control-Allow-Origin", enviroment.origin.encode(configuration.api.encoding)))

    await enviroment.send({
        'type': 'http.response.start',
        'status': ResponseCode.OK.code,
        'headers': _headers
    })

    await enviroment.send({
        'type': 'http.response.body',
        'body': content
    })
    
    Debug(f"View: Finalized Response")
