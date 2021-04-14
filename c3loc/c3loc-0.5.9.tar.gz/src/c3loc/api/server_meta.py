import pkg_resources

from aiohttp import web
from aiohttp_cors import CorsViewMixin

from ..config import CONFIG


class ServerMetaView(web.View, CorsViewMixin):
    async def get(self):
        be_version = pkg_resources.require("c3loc")[0].version
        return web.json_response({
            "api_version": "1.3",
            "backend_version": be_version,
            "api_result_limit": CONFIG['API_RESULT_LIMIT']})