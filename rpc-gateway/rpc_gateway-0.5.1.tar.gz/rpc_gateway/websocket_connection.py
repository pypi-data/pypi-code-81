from typing import Optional, Dict, Any, Callable, Awaitable, Union
import asyncio
import pickle
import json
import logging
import websockets
from concurrent import futures
from google.protobuf.message import EncodeError, DecodeError
from rpc_gateway import errors, utils, messages_pb2

logger = logging.getLogger(__name__)
RequestHandlerType = Callable[['WebsocketConnection', messages_pb2.Message], Awaitable[messages_pb2.Message]]
CloseHandlerType = Callable[['MessagePump'], Awaitable]
MAX_MESSAGE_ID = 99999
last_message_id = 0


def next_message_id() -> int:
    global last_message_id
    last_message_id += 1
    return last_message_id % MAX_MESSAGE_ID


class WebsocketConnection:
    next_id = 0

    def __init__(self,
                 connection: Optional[websockets.WebSocketCommonProtocol] = None,
                 request_handler: Optional[RequestHandlerType] = None,
                 close_handler: Optional[CloseHandlerType] = None,
                 message_queues: Optional[Dict[int, asyncio.Queue]] = None):
        self.id = WebsocketConnection.next_id
        WebsocketConnection.next_id += 1
        self.logger = logger.getChild(self.__class__.__name__)
        self.connection = connection
        self.request_handler = request_handler
        self.close_handler = close_handler
        self.event_loop = asyncio.get_event_loop()
        self.send_queue = asyncio.Queue()
        self.receive_queues = {} if message_queues is None else message_queues
        self.message_send_task: Optional[asyncio.Task] = None
        self.message_receive_task: Optional[asyncio.Task] = None
        self.running = False

    @property
    def connected(self) -> bool:
        return self.connection.open

    async def start(self, wait=True, connection: Optional[websockets.WebSocketCommonProtocol] = None):
        if connection is not None:
            self.connection = connection

        self.running = True
        self.message_send_task = asyncio.Task(self._message_receive())
        self.message_receive_task = asyncio.Task(self._message_send())

        if wait:
            await self.wait()

    async def wait(self):
        try:
            await self.message_send_task
            await self.message_receive_task
        except futures.CancelledError:
            pass

    async def stop(self):
        self.running = False
        await self.connection.close()
        await self.connection.wait_closed()
        self.message_send_task.cancel()
        self.message_receive_task.cancel()
        try:
            await self.message_receive_task
            await self.message_send_task
        except futures.CancelledError:
            pass

    def send_message_sync(self, message: messages_pb2.Message):
        utils.await_sync(self.send_message(message), self.event_loop)

    async def send_message(self, message: messages_pb2.Message):
        if self.connection is None:
            raise errors.NotConnectedError('Must be connected to send message: {message}')

        await self.send_queue.put(message)

    def send_request_sync(self, method: str, instance: Optional[str] = None, attribute: Optional[str] = None,
                          data: Any = None, encoding: messages_pb2.Encoding = messages_pb2.Encoding.PICKLE) -> messages_pb2.Message:
        return utils.await_sync(self.send_request(method, instance, attribute, data, encoding), self.event_loop)

    async def send_request(self, method: str, instance: Optional[str] = None, attribute: Optional[str] = None,
                          data: Any = None, encoding: messages_pb2.Encoding = messages_pb2.Encoding.PICKLE, raise_error: bool = True) -> messages_pb2.Message:
        encoded_data = utils.encode_data(data, encoding)
        request = messages_pb2.Request(method=method, instance=instance, attribute=attribute)
        message = messages_pb2.Message(data=encoded_data, encoding=encoding, request=request)
        return await self.request(message, raise_error=raise_error)

    def request_sync(self, request: messages_pb2.Message, raise_error=True) -> messages_pb2.Message:
        return utils.await_sync(self.request(request, raise_error))

    async def request(self, request: messages_pb2.Message, raise_error=True) -> messages_pb2.Message:
        request.id = next_message_id()
        queue = self.receive_queues[request.id] = asyncio.Queue()
        await self.send_message(request)

        try:
            response: messages_pb2.Message = await queue.get()
            self.receive_queues.pop(request.id)
        except asyncio.TimeoutError:
            self.receive_queues.pop(request.id)
            raise errors.RequestTimeoutError(f'Request timed out while waiting for response: {request}')

        # raise an error if this is an error response
        if response.response.status == messages_pb2.Status.ERROR and raise_error:
            decoded_error = utils.decode_data(response.data, response.encoding)

            if response.encoding == messages_pb2.Encoding.JSON:
                raise Exception(decoded_error)

            if response.encoding == messages_pb2.Encoding.PICKLE:
                raise decoded_error

            raise errors.InvalidEncodingError(f'Invalid response encoding: {response.encoding}')

        return response

    async def _handle_request(self, request: messages_pb2.Message):
        id = request.id
        response: messages_pb2.Message = await self.request_handler(self, request)
        response.id = id
        await self.send_message(response)

    async def _message_send(self):
        while self.running:
            message: messages_pb2.Message = await self.send_queue.get()

            try:
                message_bytes = message.SerializeToString()
            except EncodeError:
                error = errors.SerializationError(f'Cannot serialize response data')
                message = messages_pb2.Message(id=message.id, data=utils.encode_error(error, message.encoding))
                message.response.status = messages_pb2.Status.ERROR
                message_bytes = message.SerializeToString()

            self.logger.info(f'[{self.id}] > {message}')
            await self.connection.send(message_bytes)

    async def _message_receive(self):
        try:
            while self.running:
                message_bytes = await self.connection.recv()
                try:
                    message = messages_pb2.Message()
                    message.ParseFromString(message_bytes)
                except DecodeError:
                    self.logger.error(f'Invalid message: {message_bytes}')
                    continue

                self.logger.info(f'[{self.id}] < {message}')

                if message.HasField('response'):
                    if message.id not in self.receive_queues:
                        raise errors.InvalidMessageIdError(f'No request found for response ID: {message.id}')

                    queue = self.receive_queues[message.id]
                    await queue.put(message)

                elif message.HasField('request'):  # request
                    if self.request_handler is not None:
                        asyncio.create_task(self._handle_request(message))

                else:
                    self.logger.error(f'Invalid message: {message}')

        except websockets.ConnectionClosed as err:
            self.logger.info(f'[{self.id}] Connection closed')

            if isinstance(err, websockets.ConnectionClosedError):
                self.logger.error(err)

            if self.close_handler is not None:
                await self.close_handler(self)