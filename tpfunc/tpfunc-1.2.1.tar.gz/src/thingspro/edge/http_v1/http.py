#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import json
import queue
import threading
import grpc

from .rpc import reverseproxy_pb2
from .rpc import reverseproxy_pb2_grpc

class message_queue:
    def __init__(self):
        self.q = queue.Queue()
    
    def pop(self):
        try:
          return self.q.get(True)
        except queue.Empty:
          return None

    def push(self, item):
        if self.q.full():
            self.q.get_nowait()
        self.q.put(item)


class proxy_agent():
    def __init__(self, method, endpoint, handler):
        self.method = method
        self.endpoint = endpoint
        self.handler = handler
        self._mq = message_queue()
        self.__connect_to_server()

    def __connect_to_server(self):
        try:
            self._channel = grpc.insecure_channel(target='unix:/host/run/tpfunc/proxy.sock')
            self._conn = reverseproxy_pb2_grpc.TriggerStub(self._channel)

            profile = reverseproxy_pb2.Profile(method=self.method, endpoint=self.endpoint)
            confirm = self._conn.Register(profile)
            if confirm is not None:
                threading.Thread(target=self.__listen_for_message, daemon=True).start()
            else:
                raise Exception('register http profile failed')
        except Exception as e:
            print(e)

    def __construct_request(self, message):
        try:
            if len(message) > 0:
                return json.loads(message)
        except Exception as e:
            return message

    def __wait_response(self, method, endpoint, queue):
        # notify server to know http service start
        profile = reverseproxy_pb2.Profile(method=method, endpoint=endpoint)
        reply = reverseproxy_pb2.Reply(profile=profile)
        yield reply

        # wait blocking for response
        while True:
            yield queue.pop()

    def __construct_response(self, resp):
        data = ""
        try:
            if isinstance(resp.data, dict):
                data = json.dumps(resp.data)
            elif isinstance(resp.data, str):
                data = resp.data
            else:
                raise Exception('response data type either string or dict')
            return self.__empty_response(code=resp.code, payload=data)
        except Exception as e:
            return self.__empty_response(code=400, payload="{{\"message\":\"{}\"}}".format(e))

    def __empty_response(self, code=200, headers="{}", payload="{}"):
        return reverseproxy_pb2.Reply(code=code, headers=headers, payload=payload)

    def __listen_for_message(self):
        try:
            reply = self.__empty_response()
            response_iterator = self.__wait_response(self.method, self.endpoint, self._mq)
            requests = self._conn.Fire(response_iterator)
            for request in requests:
                reply = self.__empty_response()
                if self.handler is not None:
                    resp = self.handler(resource=request.resource, headers=request.headers, message=request.payload)
                    if resp is not None:
                        reply = self.__construct_response(resp)
                self._mq.push(reply)
        except Exception as e:
            print(e)


class Response():
    def __init__(self, code=200, data={}):
        """ Constructor """
        self.code = code
        self.data = data


def http_get(resource=''):
    def decorator(func):
        def proxy_get():
            proxy_agent(method='GET', endpoint=resource, handler=func)
        return proxy_get
    return decorator


def http_put(func, resource=''):
    def proxy_put():
        proxy_agent('PUT', resource, func)
    return proxy_put


def http_post(func, resource=''):
    def proxy_post():
        proxy_agent('POST', resource, func)
    return proxy_post


def http_delete(func, resource=''):
    def proxy_delete():
        proxy_agent('DELETE', resource, func)
    return proxy_delete


class Server():
    @staticmethod
    def GET(resource='', handler=None):
        proxy_agent('GET', resource, handler)

    @staticmethod
    def PUT(resource='', handler=None):
        proxy_agent('PUT', resource, handler)

    @staticmethod
    def POST(resource='', handler=None):
        proxy_agent('POST', resource, handler)

    @staticmethod
    def DELETE(resource='', handler=None):
        proxy_agent('DELETE', resource, handler)

