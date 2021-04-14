# coding=utf-8
from __future__ import absolute_import, print_function

import time
import socketio

from suanpan.api import auth


def sio(*args, **kwargs):
    ctx = dict(connected=False)
    kwargs["headers"] = {**auth.defaultHeaders(), **kwargs.pop("headers", {})}
    client = socketio.Client()
    client.on("connect", lambda: ctx.update(connected=True))
    client.connect(*args, **kwargs)
    while not ctx.get("connected", False):
        time.sleep(0.1)
    return client
