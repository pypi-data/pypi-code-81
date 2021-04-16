import aiohttp_cors
from applipy import Module as Module_
from applipy_http import (
    Api,
    Endpoint,
    EndpointMethod,
    EndpointWrapper,
    HttpModule,
    PathFormatter,
    PrefixPathFormatter,
    cors_config,
)
from applipy_inject import with_names
from .common import ApplipyProcess
from aiohttp import web
import requests
from logging import Logger


class EndpointA(Endpoint):

    def __init__(self, logger: Logger):
        self.logger = logger.getChild(self.__class__.__name__)

    async def get(self, request, ctx):
        self.logger.info('GET')
        return web.Response(body='GET Success')

    async def post(self, request, ctx):
        self.logger.info('POST')
        return web.Response(body='POST Success')

    def path(self):
        return '/testA'


class EndpointB(Endpoint):

    async def put(self, request, ctx):
        return web.Response(body=f'PUT Matched `{request.match_info["var"]}`')

    async def patch(self, request, ctx):
        return web.Response(body=f'PATCH Matched `{request.match_info["var"]}`')

    def path(self):
        return '/testB/{var:.*}'


class EndpointC(Endpoint):

    global_cors_config = {'*': aiohttp_cors.ResourceOptions(allow_credentials=False, allow_methods=('POST',))}

    @cors_config({'http://localhost:8080': aiohttp_cors.ResourceOptions(allow_methods=('GET',))})
    async def get(self, request, ctx):
        return web.Response(body='GET with cors config')

    async def post(self, request, ctx):
        return web.Response(body='POST with cors config')

    def path(self):
        return '/testC'


class TestWrapperA(EndpointWrapper):

    def wrap(self, method: str, path: str, handler: EndpointMethod) -> EndpointMethod:
        async def wrapper(*args, **kwargs):
            response = await handler(*args, **kwargs)
            response.headers['X-wrappers'] = response.headers.get('X-wrappers', '') + '[wrapperA]'
            return response

        return wrapper

    def priority(self) -> int:
        return 10


class TestWrapperB(EndpointWrapper):

    def wrap(self, method: str, path: str, handler: EndpointMethod) -> EndpointMethod:
        async def wrapper(*args, **kwargs):
            response = await handler(*args, **kwargs)
            response.headers['X-wrappers'] = response.headers.get('X-wrappers', '') + '[wrapperB]'
            return response

        return wrapper

    def priority(self) -> int:
        return 20


class Module(Module_):

    def configure(self, bind, register):
        bind(Endpoint, EndpointB, name='other')
        bind(PathFormatter, PrefixPathFormatter('other'), name='other')
        bind(EndpointWrapper, TestWrapperA, name='other')
        bind(EndpointWrapper, TestWrapperB, name='other')
        bind(Api, with_names(Api, 'other'), name='other')

        bind(Endpoint, EndpointA)
        bind(Endpoint, EndpointC)
        bind(PathFormatter)
        bind(Api)

    @classmethod
    def depends_on(cls):
        return HttpModule,


def test_applipy_http():
    with ApplipyProcess('./tests/acceptance', 'test_applipy_http') as p:
        with requests.get('http://0.0.0.0:8080/testA') as r:
            assert r.status_code == 200
            assert r.text == 'GET Success'

        with requests.post('http://0.0.0.0:8080/testA') as r:
            assert r.status_code == 200
            assert r.text == 'POST Success'

        with requests.put('http://0.0.0.0:8081/other/testB/foo') as r:
            assert r.status_code == 200
            assert r.text == 'PUT Matched `foo`'
            assert r.headers['X-wrappers'] == '[wrapperA][wrapperB]'

        with requests.patch('http://0.0.0.0:8081/other/testB/bar') as r:
            assert r.status_code == 200
            assert r.text == 'PATCH Matched `bar`'
            assert r.headers['X-wrappers'] == '[wrapperA][wrapperB]'

        with requests.get('http://0.0.0.0:8080/testC') as r:
            # TODO: This does not check CORS functionality
            assert r.status_code == 200
            assert r.text == 'GET with cors config'

        with requests.post('http://0.0.0.0:8080/testC') as r:
            # TODO: This does not check CORS functionality
            assert r.status_code == 200
            assert r.text == 'POST with cors config'

    assert p.returncode == 0
