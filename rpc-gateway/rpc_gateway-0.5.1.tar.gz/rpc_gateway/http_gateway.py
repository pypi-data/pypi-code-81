import json
from typing import Optional, Any, Dict, List
import logging
import re
from aiohttp import web
from rpc_gateway import messages_pb2, websocket_connection, utils, errors

logger = logging.getLogger(__name__)


class MessageHandler:
    SERVER_MESSAGES = []

    def handle_forward_request(self, message: messages_pb2.Message) -> messages_pb2.Message:
        pass

    def handle_available_request(self, message: messages_pb2.Message) -> messages_pb2.Message:
        pass

    def handle_list_request(self, message: messages_pb2.Message) -> messages_pb2.Message:
        pass


class HttpGateway:
    def __init__(self, message_handler: MessageHandler, host: str, port: int, auth_key: str):
        self.logger = logger.getChild(self.__class__.__name__)
        self.host = host
        self.port = port
        self.message_handler = message_handler
        self.auth_key = auth_key
        self.app = web.Application(middlewares=[self.authenticate])
        self.runner = web.AppRunner(self.app)
        self.site: Optional[web.TCPSite] = None
        self.running = False

        self.app.add_routes([web.get('/instance/{instance}/{attribute}', self.get),
                             web.put('/instance/{instance}/{attribute}', self.set),
                             web.post('/instance/{instance}/{attribute}', self.call),
                             web.get('/available/{instance}', self.available),
                             web.get('/metadata/{instance}', self.metadata),
                             web.get('/list/{group}', self.list),
                             web.post('/', self.legacy_request)])

    async def start(self):
        self.logger.info(f'Starting HTTP server on http://{self.host}:{self.port}, auth_key={self.auth_key}')
        await self.runner.setup()
        self.site = web.TCPSite(self.runner, self.host, self.port)
        await self.site.start()
        self.running = True

    async def stop(self):
        await self.site.stop()
        self.running = False

    @web.middleware
    async def authenticate(self, request: web.BaseRequest, handler) -> web.StreamResponse:
        if 'Authentication' in request.headers:
            auth_header = request.headers['Authentication']

            if auth_header.startswith('AuthKey '):
                auth_type, auth_key = auth_header.split(' ', maxsplit=2)

                if auth_key == self.auth_key:
                    return await handler(request)

        elif 'auth_key' in request.query and request.query['auth_key'] == self.auth_key:
            return await handler(request)

        return web.json_response('Unauthorized', status=401)

    async def get(self, request: web.Request) -> web.StreamResponse:
        response = await self.message_handler.handle_forward_request(utils.build_request(method=messages_pb2.Method.GET,
                                                                                         instance=request.match_info.get('instance'),
                                                                                         attribute=request.match_info.get('attribute')))

        return utils.build_http_response(response)

    async def set(self, request: web.Request) -> web.StreamResponse:
        encoded_data = utils.encode_data(request.json(), messages_pb2.Encoding.PICKLE)
        response = await self.message_handler.handle_forward_request(utils.build_request(method=messages_pb2.Method.SET,
                                                                                         instance=request.match_info.get('instance'),
                                                                                         attribute=request.match_info.get('attribute'),
                                                                                         data=encoded_data))

        return utils.build_http_response(response)

    async def call(self, request: web.Request) -> web.StreamResponse:
        data: Dict = (await request.json()) or {}
        query = {k: v for k, v in request.query.items() if k != 'AUTH_KEY'}
        kwargs = {**data.get('kwargs', {}), **query}
        args = data.get('args', [])
        encoded_data = utils.encode_data({'args': args, 'kwargs': kwargs}, messages_pb2.Encoding.PICKLE)
        response = await self.message_handler.handle_forward_request(utils.build_request(method=messages_pb2.Method.CALL,
                                                                                         instance=request.match_info.get('instance'),
                                                                                         attribute=request.match_info.get('attribute'),
                                                                                         data=encoded_data))

        return utils.build_http_response(response)

    async def available(self, request: web.Request) -> web.StreamResponse:
        response = await self.message_handler.handle_available_request(utils.build_request(method=messages_pb2.Method.AVAILABLE,
                                                                                           instance=request.match_info.get('instance')))

        return utils.build_http_response(response)

    async def metadata(self, request: web.Request) -> web.StreamResponse:
        response = await self.message_handler.handle_forward_request(utils.build_request(method=messages_pb2.Method.METADATA,
                                                                                         instance=request.match_info.get('instance')))

        return utils.build_http_response(response)

    async def list(self, request: web.Request) -> web.StreamResponse:
        data = utils.encode_data(request.match_info.get('group', None), messages_pb2.Encoding.PICKLE)
        response = await self.message_handler.handle_list_request(utils.build_request(method=messages_pb2.Method.LIST,
                                                                                      data=data))

        return utils.build_http_response(response)

    async def legacy_request(self, request: web.Request) -> web.StreamResponse:
        if request.method != 'POST':
            return web.HTTPMethodNotAllowed(request.method, ['POST'])

        message_raw = await request.read()

        try:
            self.logger.info(f'Handling request: {message_raw}')
            message = json.loads(message_raw)
            method = messages_pb2.Method.Value(message['method'].upper())
            request = messages_pb2.Message()
            request.request.method = method

            if 'instance' in message['data']:
                request.request.instance = message['data'].pop('instance')

            if 'attribute' in message['data']:
                request.request.attribute = message['data'].pop('attribute')

            request.data = utils.encode_data(message['data'], messages_pb2.Encoding.PICKLE)

            if method in self.message_handler.SERVER_MESSAGES:
                response = await self.message_handler.handle_forward_request(request)
            elif method == messages_pb2.Method.AVAILABLE:
                response = await self.message_handler.handle_available_request(request)
            elif method == messages_pb2.Method.LIST:
                response = await self.message_handler.handle_list_request(request)
            else:
                response = utils.build_error_response(errors.InvalidMethodError(f'Invalid method: {request.method}'))

        except (KeyError, json.decoder.JSONDecodeError):
            response = utils.build_error_response(errors.InvalidMessageError(f'Invalid message: {message_raw}'))

        response_dict = {'status': messages_pb2.Status.Name(response.response.status).lower()}

        if response.response.status == messages_pb2.Status.ERROR:
            response_dict['data'] = repr(utils.decode_data(response.data, response.encoding))
        elif response.data:
            response_dict['data'] = utils.decode_data(response.data, response.encoding)

        return web.json_response(response_dict)