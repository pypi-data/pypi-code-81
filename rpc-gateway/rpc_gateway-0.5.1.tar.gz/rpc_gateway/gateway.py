from typing import Optional, List, Dict, Any
import logging
import time
import asyncio
import websockets
import json
import urllib
import threading
import re
from concurrent.futures._base import CancelledError
from dataclasses import asdict
from aiohttp import web
from rpc_gateway import errors, messages_pb2, utils, http_gateway
from rpc_gateway.websocket_connection import WebsocketConnection, next_message_id
from rpc_gateway.utils import await_sync

logger = logging.getLogger(__name__)


class Gateway(http_gateway.MessageHandler):
    SERVER_MESSAGES = (messages_pb2.Method.GET, messages_pb2.Method.SET, messages_pb2.Method.CALL, messages_pb2.Method.LOCK,
                       messages_pb2.Method.UNLOCK, messages_pb2.Method.METADATA)

    def __init__(self, host: str = 'localhost', port: int = 8888, http_port: int = 8887, auth_key: str = 'DEFAULT_KEY', event_loop: Optional[asyncio.AbstractEventLoop] = None):
        self.host = host
        self.port = port
        self.auth_key = auth_key
        self.logger = logger.getChild(self.__class__.__name__)
        self.websocket_connections: List[WebsocketConnection] = []
        self.websocket: Optional[websockets.WebSocketServer] = None
        self.http_gateway = http_gateway.HttpGateway(self, host, http_port, auth_key)
        self.event_loop = event_loop or asyncio.get_event_loop()
        self.instances: Dict[str, WebsocketConnection] = {}
        self.instance_groups: Dict[str, List[str]] = {}
        self.websocket_instances: Dict[WebsocketConnection, List[str]] = {}
        self.check_connections_task: Optional[asyncio.Task] = None
        self.running = False

    def start(self, wait = True):
        self.event_loop.run_until_complete(self._start(wait=False))

        if wait:
            await_sync(self._wait())

    async def _start(self, wait = True):
        self.logger.info(f'Starting on ws://{self.host}:{self.port}')
        self.websocket = await websockets.serve(self.on_connection, self.host, self.port)
        await self.http_gateway.start()
        self.running = True
        self.check_connections_task = self.check_connections()

        if wait:
            await self._wait()

    def wait(self):
        await_sync(self._wait(), self.event_loop)

    async def _wait(self):
        if self.websocket is not None:
            await self.websocket.wait_closed()

        self.logger.info(f'Done')

    def stop(self):
        await_sync(self._stop(), self.event_loop)

    async def _stop(self):
        self.running = False
        await self.http_gateway.stop()
        try:
            await asyncio.gather(*[websocket_connection.stop() for websocket_connection in self.websocket_connections])
        except asyncio.exceptions.CancelledError:
            pass
        self.websocket.close()
        await self.check_connections_task

    async def on_connection(self, connection: websockets.WebSocketServerProtocol, path: str):
        self.logger.info(f'New connection from {connection.remote_address} path: {path}')
        connection_params = urllib.parse.parse_qs(path[1:]) if path != '' else {}

        if 'auth_key' not in connection_params or connection_params['auth_key'][0] != self.auth_key:
            await connection.close(1008, 'Invalid auth_key')  # 1008 is the "Policy Violation" websocket status code
            return

        websocket_connection = WebsocketConnection(connection, request_handler=self.handle_request, close_handler=self.handle_close)
        self.websocket_connections.append(websocket_connection)
        self.websocket_instances[websocket_connection] = []

        await websocket_connection.start()

    async def _unlock_instance(self, instance_name: str) -> messages_pb2.Message:
        server = self.instances[instance_name]
        return await server.send_request(messages_pb2.Method.UNLOCK, instance=instance_name, raise_error=False)

    def is_registered(self, group: str, instance: str) -> bool:
        if group not in self.instance_groups:
            return False

        return instance in self.instance_groups[group]

    async def check_connections(self):
        while self.running:
            for websocket_connection in self.websocket_connections:
                if not websocket_connection.connected:
                    await self.handle_close(websocket_connection)

            time.sleep(1)

    #
    # Request Handlers
    #

    async def handle_forward_request(self, request: messages_pb2.Message) -> messages_pb2.Message:
        self.logger.info(f'Forwarding request to server: {request}')
        instance_name = request.request.instance

        if instance_name not in self.instances:
            return utils.build_error_response(errors.InstanceNotFoundError(f'Instance not found: {instance_name}'))

        server = self.instances[instance_name]

        response = await server.request(request, raise_error=False)
        self.logger.info(f'Forwarding response to client: {response}')

        return response

    async def handle_available_request(self, request: messages_pb2.Message) -> messages_pb2.Message:
        if request.request.instance not in self.instances:
            return utils.build_response(status=messages_pb2.Status.NOT_FOUND)

        server = self.instances[request.request.instance]
        return await server.request(request)

    async def handle_list_request(self, request: messages_pb2.Message) -> messages_pb2.Message:
        group = utils.decode_data(request.data, request.encoding)

        if not group:
            instances = self.instance_groups
        else:
            if group not in self.instance_groups:
                return utils.build_error_response(errors.GroupNotFoundError(f'Group not found: {group}'))

            instances = {group: self.instance_groups[group]}

        return utils.build_response(instances)

    async def handle_register_request(self, websocket_connection: WebsocketConnection, request: messages_pb2.Message) -> messages_pb2.Message:
        instances = utils.decode_data(request.data, request.encoding)

        self.logger.info(f'Registering instances: {instances}')

        # check to see if this instance
        for instance_name, instance_group in instances:
            if instance_name is None:
                return utils.build_error_response(errors.InvalidMessageError(f'Cannot register instance with name: {instance_name}'))

            if instance_group is None:
                return utils.build_error_response(errors.InvalidMessageError(f'Cannot register instance with group: {instance_group}'))

            if self.is_registered(instance_group, instance_name):
                return utils.build_error_response(errors.InstanceAlreadyRegisteredError(f'Instance "{instance_name}" already registered with "{instance_group}" group'))

        for instance_name, instance_group in instances:
            if instance_group not in self.instance_groups:
                self.instance_groups[instance_group] = []

            self.instance_groups[instance_group].append(instance_name)
            self.instances[instance_name] = websocket_connection
            self.websocket_instances[websocket_connection].append(instance_name)

        return utils.build_response()

    async def handle_deregister_request(self, websocket_connection: WebsocketConnection, request: messages_pb2.Message) -> messages_pb2.Message:
        instances = utils.decode_data(request.data, request.encoding)
        self.logger.info(f'Deregistering instances: {instances}')

        # find instance to deregister
        for instance_name in instances:
            if instance_name not in self.instances:
                return utils.build_error_response(errors.InstanceNotFoundError(f'Instance "{instance_name}" not found'))

            instance_connection = self.instances[instance_name]
            self.instances.pop(instance_name)
            self.websocket_instances[instance_connection].remove(instance_name)

            for group, group_instances in self.instance_groups.items():
                if instance_name in group_instances:
                    group_instances.remove(instance_name)

        return utils.build_response()

    # this is called by the WebsocketConnection MessagePump when a new request is received
    async def handle_request(self, websocket_connection: WebsocketConnection, message: messages_pb2.Message) -> messages_pb2.Message:
        method = message.request.method

        if method in self.SERVER_MESSAGES:
            return await self.handle_forward_request(message)

        if method == messages_pb2.Method.AVAILABLE:
            return await self.handle_available_request(message)

        if method == messages_pb2.Method.REGISTER:
            return await self.handle_register_request(websocket_connection, message)

        if method == messages_pb2.Method.DEREGISTER:
            return await self.handle_deregister_request(websocket_connection, message)

        if method == messages_pb2.Method.LIST:
            return await self.handle_list_request(message)

        return utils.build_error_response(errors.InvalidMethodError(f'Invalid method: {method}'))

    async def handle_close(self, websocket_connection: WebsocketConnection):
        # check if this is a server connection
        if websocket_connection in self.websocket_instances:
            instances = self.websocket_instances[websocket_connection]

            # remove registered instances
            for instance_name in instances:
                if instance_name in self.instances:
                    self.instances.pop(instance_name)

                groups_to_remove = []

                for group, group_instances in self.instance_groups.items():
                    if instance_name in group_instances:
                        group_instances.remove(instance_name)

                    if len(group_instances) == 0:
                        groups_to_remove.append(group)

                for group in groups_to_remove:
                    if group in self.instance_groups:
                        self.instance_groups.pop(group)

            self.websocket_instances.pop(websocket_connection)

        # send an error response for any in-progress requests
        for request_id, response_queue in websocket_connection.receive_queues.items():
            await response_queue.put(utils.build_error_response(errors.ServerConnectionLostError(f'Server connection lost')))

        self.websocket_connections.remove(websocket_connection)

        self.logger.info(f'Connection from {websocket_connection.connection.remote_address} closed')


class GatewayClient:
    def __init__(self, gateway_url: str = 'ws://localhost:8888', auth_key: str = 'DEFAULT_KEY'):
        self.logger = logger.getChild(self.__class__.__name__)
        self.gateway_url = gateway_url[:-1] if gateway_url.endswith('/') else gateway_url
        self.gateway_auth_key = auth_key
        self.websocket_connection = WebsocketConnection(request_handler=self._log_and_handle_request, close_handler=self._handle_close)
        self.event_loop = asyncio.get_event_loop()
        self.connect_retry_timeout = 2.0
        self.start_thread = threading.Thread(name='RPC gateway client', target=self._start_sync, daemon=True)

    @property
    def connected(self) -> bool:
        return self.websocket_connection.connection is not None

    async def _connect(self):
        while True:
            try:
                self.logger.info(f'Connecting to {self.gateway_url}')
                self.connection = await websockets.connect(self.gateway_url + '/socket&auth_key=' + self.gateway_auth_key)
                return
            except OSError:
                self.logger.warning(f'Error connecting to {self.gateway_url}, retrying in {self.connect_retry_timeout} seconds')
                time.sleep(self.connect_retry_timeout)

    def start(self, wait=True):
        self.start_thread.start()
        if wait:
            self.start_thread.join()

    def _start_sync(self):
        await_sync(self._start(), self.event_loop)

    async def _start(self):
        await self._connect()
        await self.websocket_connection.start(wait=False, connection=self.connection)
        await self._on_start()
        await self._wait()

    def wait(self):
        self.start_thread.join()

    async def _wait(self):
        await self.websocket_connection.wait()

    async def _on_start(self):
        pass

    async def _on_stop(self):
        pass

    def stop(self):
        try:
            await_sync(self._stop(), self.event_loop)
        except CancelledError:
            pass

        self.start_thread.join()

    async def _stop(self):
        await self._on_stop()
        await self.websocket_connection.stop()

    async def _log_and_handle_request(self, websocket_connection: WebsocketConnection, request: messages_pb2.Message) -> messages_pb2.Message:
        self.logger.debug(f'Request from {websocket_connection}: {request}')
        response = await self._handle_request(websocket_connection, request)
        self.logger.debug(f'Response to {websocket_connection}: {response}')

        return response

    async def _handle_request(self, websocket_connection: WebsocketConnection, request: messages_pb2.Message) -> messages_pb2.Message:
        pass

    async def _handle_close(self, websocket_connection: WebsocketConnection):
        await self._connect()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    gateway = Gateway()
    gateway.start()