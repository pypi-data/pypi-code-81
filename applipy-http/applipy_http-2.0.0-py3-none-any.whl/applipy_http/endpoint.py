import typing as T

from aiohttp import web

from applipy_http.types import CorsConfig, EndpointMethod, Context


def _disabled(
        func: EndpointMethod
) -> EndpointMethod:
    async def wrapper(
        request: web.Request,
        context: Context
    ) -> web.StreamResponse:
        return await func(request, context)

    setattr(wrapper, '_endpoint_method_disabled', True)
    return wrapper


class Endpoint:

    global_cors_config: T.Optional[CorsConfig] = None

    @_disabled
    async def get(self, request: web.Request, context: Context) -> web.StreamResponse:
        raise web.HTTPMethodNotAllowed()

    @_disabled
    async def head(self, request: web.Request, context: Context) -> web.StreamResponse:
        raise web.HTTPMethodNotAllowed()

    @_disabled
    async def post(self, request: web.Request, context: Context) -> web.StreamResponse:
        raise web.HTTPMethodNotAllowed()

    @_disabled
    async def put(self, request: web.Request, context: Context) -> web.StreamResponse:
        raise web.HTTPMethodNotAllowed()

    @_disabled
    async def delete(self, request: web.Request, context: Context) -> web.StreamResponse:
        raise web.HTTPMethodNotAllowed()

    @_disabled
    async def connect(self, request: web.Request, context: Context) -> web.StreamResponse:
        raise web.HTTPMethodNotAllowed()

    @_disabled
    async def options(self, request: web.Request, context: Context) -> web.StreamResponse:
        raise web.HTTPMethodNotAllowed()

    @_disabled
    async def trace(self, request: web.Request, context: Context) -> web.StreamResponse:
        raise web.HTTPMethodNotAllowed()

    @_disabled
    async def patch(self, request: web.Request, context: Context) -> web.StreamResponse:
        raise web.HTTPMethodNotAllowed()

    def path(self) -> str:
        raise NotImplementedError()
