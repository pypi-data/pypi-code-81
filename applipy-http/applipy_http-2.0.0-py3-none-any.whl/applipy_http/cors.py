import typing as T

from aiohttp import web

from applipy_http.endpoint import Endpoint
from applipy_http.types import EndpointMethod, CorsConfig, Context


def cors_config(config: CorsConfig) -> T.Callable[[EndpointMethod], EndpointMethod]:
    def func_handler(func: EndpointMethod) -> EndpointMethod:
        async def wrapper(
            self: Endpoint,
            request: web.Request,
            context: Context
        ) -> T.Awaitable[web.StreamResponse]:
            return await func(self, request, context)

        wrapper._cors_config = config

        return wrapper

    return func_handler
