from typing import Any, Iterable, Optional, List, Dict, Callable
import time
import logging
import asyncio
from rpc_gateway import errors, gateway, messages_pb2, utils


class Client(gateway.GatewayClient):
    @staticmethod
    def join_attribute_paths(*paths):
        return '.'.join([path for path in paths if path != ''])

    def connect(self, timeout: float = 10.0):
        if not self.connected:
            self.start(wait=False)

            start_time = time.time()
            while not self.connected:
                if time.time() - start_time > timeout:
                    raise errors.ConnectionError(f'Timeout while waiting for client to connect')

                time.sleep(0.01)

    def get_instance(self, instance_name, read_only: bool = False) -> Any:
        if not read_only:
            if self.instance_locked(instance_name):
                raise errors.InstanceLockedError(f'Instance locked: {instance_name}')

            self.lock(instance_name)

        return self.proxy_attribute(instance_name, '', read_only=read_only)

    def proxy_method(self, instance_name: str, method_path: str, read_only: bool = False) -> Callable:
        def _proxy_method(*args, **kwargs):
            if read_only:
                raise errors.InstanceReadOnly(f'Cannot call method {method_path} on read-only instance')

            return self.call(instance_name, method_path, args, kwargs)

        return _proxy_method

    def proxy_attribute(self, instance_name: str, attribute_path: str, read_only: bool = False) -> object:
        client = self

        class _Proxy:
            def __dir__(self) -> Iterable[str]:
                return client.call(instance_name, client.join_attribute_paths(attribute_path, '__dir__'))

            def __getattr__(self, key):
                return client.get(instance_name, client.join_attribute_paths(attribute_path, key))

            def __setattr__(self, key, value):
                if read_only:
                    raise errors.InstanceReadOnly(f'Cannot set attribute {key} on read-only instance')

                return client.set(instance_name, client.join_attribute_paths(attribute_path, key), value)

            def __repr__(self):
                return client.call(instance_name, client.join_attribute_paths(attribute_path, '__repr__'))

            def __str__(self):
                return client.call(instance_name, client.join_attribute_paths(attribute_path, '__str__'))

        return _Proxy()

    def instance_exists(self, instance_name: str) -> bool:
        self.connect()

        response = self.websocket_connection.send_request_sync(messages_pb2.Method.AVAILABLE, instance=instance_name)

        return response.response.status != messages_pb2.Status.NOT_FOUND

    def instance_available(self, instance_name: str) -> bool:
        self.connect()

        response = self.websocket_connection.send_request_sync(messages_pb2.Method.AVAILABLE, instance=instance_name)
        return response.response.status == messages_pb2.Status.SUCCESS

    def instance_locked(self, instance_name: str) -> bool:
        self.connect()

        response = self.websocket_connection.send_request_sync(messages_pb2.Method.AVAILABLE, instance=instance_name)

        if response.response.status == messages_pb2.Status.NOT_FOUND:
            raise errors.InstanceNotFoundError(f'Instance not found: {instance_name}')

        return response.response.status == messages_pb2.Status.LOCKED

    def lock(self, instance_name: str):
        self.connect()

        self.websocket_connection.send_request_sync(messages_pb2.Method.LOCK, instance=instance_name)

    def unlock(self, instance_name: str):
        self.connect()

        self.websocket_connection.send_request_sync(messages_pb2.Method.UNLOCK, instance=instance_name)

    def metadata(self, instance_name: str):
        self.connect()

        response = self.websocket_connection.send_request_sync(messages_pb2.Method.METADATA, instance=instance_name)
        return utils.decode_data(response.data, response.encoding)

    def list(self, group: Optional[str]=None) -> Dict[str, List[str]]:
        self.connect()

        response = self.websocket_connection.send_request_sync(messages_pb2.Method.LIST, data=group)
        return utils.decode_data(response.data, response.encoding)

    def call(self, instance_name: str, method_path: str, args: Optional[Iterable[Any]] = None, kwargs: Optional[Dict[str, Any]] = None) -> Any:
        self.connect()

        data = {'args': args or [], 'kwargs': kwargs or {}}
        response = self.websocket_connection.send_request_sync(messages_pb2.Method.CALL, instance=instance_name, attribute=method_path, data=data)

        return utils.decode_data(response.data, response.encoding)

    def get(self, instance_name: str, attribute_path: str, read_only: bool = False) -> Any:
        self.connect()

        response = self.websocket_connection.send_request_sync(messages_pb2.Method.GET, instance=instance_name, attribute=attribute_path)

        if response.response.status == messages_pb2.Status.METHOD:
            return self.proxy_method(instance_name, attribute_path, read_only=read_only)

        if response.response.status == messages_pb2.Status.PROXY:
            return self.proxy_attribute(instance_name, attribute_path)

        return utils.decode_data(response.data, response.encoding)

    def set(self, instance_name: str, attribute_path: str, value: Any) -> Any:
        self.connect()

        self.websocket_connection.send_request_sync(messages_pb2.Method.SET, instance=instance_name, attribute=attribute_path, data=value)

        return value


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    class TestClass:
        foo = 'bar'

        def method(self):
            return 'baz'

    client = Client()
    test: TestClass = client.get_instance('test')
    print(test.foo)
    # print(test.method())
    # print(test)
