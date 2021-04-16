import typing as T

from aiohttp import web
from aiohttp_cors import ResourceOptions

Context = T.Dict[str, T.Any]
CorsConfig = T.Dict[str, ResourceOptions]
EndpointMethod = T.Callable[[web.Request, Context], T.Awaitable[web.StreamResponse]]
