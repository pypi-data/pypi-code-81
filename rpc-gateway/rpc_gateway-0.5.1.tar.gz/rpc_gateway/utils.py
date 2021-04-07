from typing import Optional, Awaitable, Any
import asyncio
import pickle
import json
from aiohttp import web
from rpc_gateway import messages_pb2, errors


def await_sync(awaitable: Awaitable, loop: Optional[asyncio.AbstractEventLoop] = None, timeout: Optional[float] = None) -> Any:
    loop = loop or asyncio.get_event_loop()
    if loop.is_running():
        future = asyncio.run_coroutine_threadsafe(awaitable, loop or asyncio.get_event_loop())
        return future.result(timeout=timeout)
    else:
        try:
            return loop.run_until_complete(awaitable)
        except asyncio.CancelledError:
            pass


def encode_data(data: Any, encoding: messages_pb2.Encoding) -> bytes:
    if encoding == messages_pb2.Encoding.PICKLE:
        return pickle.dumps(data)

    if encoding == messages_pb2.Encoding.JSON:
        return json.dumps(data).encode()

    raise errors.InvalidEncodingError(f'Invalid message encoding: {encoding}')


def encode_error(error: Exception, encoding: messages_pb2.Encoding) -> bytes:
    if encoding == messages_pb2.Encoding.PICKLE:
        return pickle.dumps(error)

    if encoding == messages_pb2.Encoding.JSON:
        return json.dumps(str(error)).encode()

    raise errors.InvalidEncodingError(f'Invalid message encoding: {encoding}')


def decode_data(data: bytes, encoding: messages_pb2.Encoding) -> Any:
    if len(data) == 0:
        return None

    if encoding == messages_pb2.Encoding.PICKLE:
        return pickle.loads(data)

    if encoding == messages_pb2.Encoding.JSON:
        return json.loads(data.decode())

    raise errors.InvalidEncodingError(f'Invalid message encoding: {encoding}')


def build_response(data: Optional[Any] = None, serialized_data: Optional[bytes] = None, status: Optional['messages_pb2.Status.V'] = messages_pb2.Status.SUCCESS,
                   id: Optional[int] = None, encoding: Optional['messages_pb2.Encoding.V'] = None):
    message = messages_pb2.Message(encoding=encoding)
    message.response.status = status

    if data is not None:
        message.data = pickle.dumps(data)

    if serialized_data is not None:
        message.data = serialized_data

    if id is not None:
        message.id = id

    return message


def build_error_response(error: Optional[Exception]) -> messages_pb2.Message:
    return build_response(status=messages_pb2.Status.ERROR, data=error)


def build_request(method: str, instance: Optional[str] = None, attribute: Optional[str] = None, id: Optional[int] = None,
                  data: Any = None, encoding: Optional['messages_pb2.Encoding.V'] = None) -> messages_pb2.Message:
    request = messages_pb2.Request(method=method, instance=instance, attribute=attribute)
    return messages_pb2.Message(id=id, data=data, encoding=encoding, request=request)


def build_http_response(response: messages_pb2.Message) -> web.Response:
    data = decode_data(response.data, response.encoding)
    return web.json_response(data, status=http_status(response.response.status), headers={'RPC-Status': str(response.response.status)})


def http_status(response_status: 'messages_pb2.Status.V') -> int:
    if response_status == messages_pb2.Status.NOT_FOUND:
        return 404

    if response_status == messages_pb2.Status.LOCKED:
        return 423

    if response_status == messages_pb2.Status.ERROR:
        return 503

    return 200