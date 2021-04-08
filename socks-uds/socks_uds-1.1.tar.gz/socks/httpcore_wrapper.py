import asyncio
from pathlib import Path

from httpcore import AsyncConnectionPool
from httpcore._async.connection import AsyncHTTPConnection # noqa
from httpcore._backends.asyncio import SocketStream # noqa
from httpcore._utils import url_to_origin  # noqa
from httpcore import ConnectTimeout, ConnectError

from .socks import SocksValueError, socks_unix_connect, socks_connect, start_tls, SocksOSError
from .utils import check_either

__all__ = ('AsyncProxyTransport',)


class AsyncProxyTransport(AsyncConnectionPool):
    def __init__(self, *,
                 socks_path: Path = None,
                 socks_host: str = None,
                 socks_port: int = None,
                 socks_username: str = None,
                 socks_password: str = None,
                 http2=False,
                 ssl_context=None,
                 **kwargs):
        self.socks_path = socks_path
        self.socks_host = socks_host
        self.socks_port = socks_port
        self.socks_username = socks_username
        self.socks_password = socks_password
        if not check_either(socks_path, (socks_host, socks_port)):
            raise SocksValueError("Either pass socks_host or both socks_host and socks_port")
        super().__init__(http2=http2, ssl_context=ssl_context, **kwargs)

    async def arequest(self, method, url, headers=None, stream=None,
                       ext=None):
        origin = url_to_origin(url)
        connection = await self._get_connection_from_pool(origin)

        ext = {} if ext is None else ext
        timeout = ext.get('timeout', {})
        connect_timeout = timeout.get('connect')
        if connection is None:
            try:
                socket_stream = await asyncio.wait_for(self._connect_to_proxy(*origin), connect_timeout)
            except asyncio.TimeoutError as te:
                raise ConnectTimeout() from te
            except SocksOSError as oe:
                raise ConnectError() from oe

            connection = AsyncHTTPConnection(
                origin=origin,
                http2=self._http2,
                ssl_context=self._ssl_context,
                socket=socket_stream
            )
            await self._add_to_pool(connection=connection, timeout=timeout)
        response = await connection.arequest(
            method=method,
            url=url,
            headers=headers,
            stream=stream,
            ext=ext
        )
        return response

    async def _connect_to_proxy(self, scheme, hostname, port):
        host = hostname.decode('ascii')  # ?
        if self.socks_path:
            reader, writer = await socks_unix_connect(host, port, self.socks_path, self.socks_username, self.socks_password)
        else:
            reader, writer = await socks_connect(host, port, self.socks_host, self.socks_port, self.socks_username, self.socks_password)

        if scheme == b'https':
            reader, writer = await start_tls(host, writer.transport, self._ssl_context)

        return SocketStream(stream_reader=reader, stream_writer=writer)
