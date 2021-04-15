# -*- coding: utf-8 -*-

import configuration
import re

from bravaweb.utils import ResponseCode
from bravaweb.utils.log import *

async def Options(headers, send):
    try:
        if headers["origin"] in configuration.api.domains:
            await send({
                'type': 'http.response.start',
                'status': ResponseCode.OK.code,
                'headers': [
                    (b"Access-Control-Allow-Headers",
                     b"Authorization, Content-Type, Uuid"),
                    (b"Access-Control-Allow-Origin",
                     headers["origin"].encode(configuration.api.encoding)),
                    (b"Access-Control-Allow-Methods",
                     b"GET, POST, OPTIONS, PUT, DELETE"),
                    (b"Accept-Ranges", b"bytes"),
                    (b"X-Frame-Options", b"Deny")
                ]
            })
        else:
            Debug(f"Origin not allowed or not present: {cls.enviroment.method}  - expected {required}")
            await send({
                'type': 'http.response.start',
                'status': ResponseCode.Forbidden.code,
                'headers': [
                    (b"X-Frame-Options", b"Deny")
                ]
            })
        await send({
            'type': 'http.response.body',
            'body': b'',
        })
    except Exception as e:
        raise e


def TestPermissionRule(_var, _key, _rule):
    if _rule == "*":
        return True
    elif not _key in _var:
        return False
    else:
        return bool(re.match(_rule, _var[_key]))


def Permitted(headers, scope):
    permitted = False
    if "origin" in headers and headers["origin"] in configuration.api.domains:
        Debug(f"Origin {headers['origin']} is present in permission list")
        permitted = True
    if not permitted:
        Debug(f"Origin {headers['origin']} isn't  present in permission list"  if "origin" in headers else "Origin/Referrer isn't present in Header")
        permitted = any([TestPermissionRule(scope, "path", exc["path"]) and TestPermissionRule(
            headers, "referer", exc["referer"]) for exc in configuration.api.access_exceptions])
        if not permitted:
            if 'origin' in headers:
                Debug(f"Origin {headers['origin']} and this route isn't present in access exceptions list")
    return permitted


def Static(scope):
    return scope["path"] == "/favicon.ico"


async def Forbidden(send):

    await send({
        'type': 'http.response.start',
        'status': ResponseCode.Forbidden.code,
        'headers': [
            (b"X-Frame-Options", b"Deny")
        ]
    })

    await send({
        'type': 'http.response.body',
        'body': b'403: Forbidden',
    })


async def NotFound(send):

    await send({
        'type': 'http.response.start',
        'status': ResponseCode.NotFound.code,
        'headers': [
            (b"X-Frame-Options", b"Deny")
        ]
    })

    await send({
        'type': 'http.response.body',
        'body': b'404: Not Found',
    })
