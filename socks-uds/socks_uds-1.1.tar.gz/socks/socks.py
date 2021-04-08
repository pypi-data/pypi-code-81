import asyncio
import ssl
from asyncio import StreamReader, StreamWriter, StreamReaderProtocol
from pathlib import Path
import socket
from urllib.request import HTTPHandler, HTTPSHandler
from urllib.request import build_opener as urllib_build_opener

__all__ = ('SocksError',
           'SocksOSError',
           'SocksValueError',
           'socks_async_handshake',
           'socks_aio_handshake',
           'socks_connect',
           'socks_unix_connect',
           'start_tls',
           'socks_sync_handshake',
           'socks_socket_handshake',
           'get_socks_connector_tcp',
           'get_socks_connector_unix',
           'build_opener',
           )

from .utils import check_either


class SocksError(Exception):
    pass


class SocksOSError(SocksError, OSError):
    SOCKS_REPLY = {
        0x01: "general SOCKS server failure",
        0x02: "connection not allowed by rule set",
        0x03: "Network unreachable",
        0x04: "Host unreachable",
        0x05: "Connection refused",
        0x06: "TTL expired",
        0x07: "Command not supported",
        0x08: "Address type not supported",
        # man tor.1 /ExtendedErrors
        0xf0: "Onion Service Descriptor Can Not be Found",
        0xf1: "Onion Service Descriptor Is Invalid",
        0xf2: "Onion Service Introduction Failed",
        0xf3: "Onion Service Rendezvous Failed",
        0xf4: "Onion Service Missing Client Authorization",
        0xf5: "Onion Service Wrong Client Authorization",
        0xf6: "Onion Service Invalid Address",
        0xf7: "Onion Service Introduction Timed Out",
    }

    def __init__(self, info: str, reply=None):
        if reply:
            error = SocksOSError.SOCKS_REPLY.get(reply, "unknown socks reply")
            info = f"{info} {error}"
        self.reply = reply
        super(SocksOSError, self).__init__(info)


class SocksValueError(SocksError, ValueError):
    pass


def as_bytes(*args):
    return b"".join(args)


def as_pair(val: str):
    encoded = val.encode()
    encoded_len = len(encoded).to_bytes(1, 'big')
    return encoded, encoded_len


# Socks Spec: https://tools.ietf.org/html/rfc1928
# Socks user pass auth spec: https://tools.ietf.org/html/rfc1929
# tor specific socks spec: https://github.com/torproject/torspec/blob/master/socks-extensions.txt
def socks_state_machine(domain_name: str, port: int, user: str, password: str):
    version = b"\x05"
    n_methods = b"\x01"
    auth_method_no_auth = b"\x00"
    auth_method_user_pass = b"\x02"
    connect_command = b"\x01"
    user_pass_auth_success = b"\x00"
    reserved_byte = b"\x00"
    address_type_domain = b"\x03"
    address_type_ipv4 = 1
    address_type_ipv6 = 4
    success_reply = 0
    user_pass_neg_version = b"\x01"

    # Auth step
    if (user, password) == (None, None):
        response = yield 2, as_bytes(version, n_methods, auth_method_no_auth)
        if response != as_bytes(version, auth_method_no_auth):
            raise SocksOSError(f"No auth not allowed. {response=}")
    elif not (user and password):
        raise SocksOSError(f"Both user and password should be set")
    else:
        response = yield 2, as_bytes(version, n_methods, auth_method_user_pass)
        if response != as_bytes(version, auth_method_user_pass):
            raise SocksOSError(f"User/Pass auth not allowed. {response=}")

        user, user_len = as_pair(user)
        password, password_len = as_pair(password)
        response = yield 2, as_bytes(user_pass_neg_version, user_len, user, password_len, password)
        if response != as_bytes(user_pass_neg_version, user_pass_auth_success):
            raise SocksOSError(f"User/Pass auth failed. {response=}")

    # Connect step
    dst_address, dst_address_len = as_pair(domain_name)
    dst_port = port.to_bytes(2, 'big')

    connect_line = as_bytes(version, connect_command, reserved_byte, address_type_domain, dst_address_len, dst_address,
                            dst_port)
    response = yield 4, connect_line
    _, reply, _, address_type = response
    if reply != success_reply:
        raise SocksOSError(f"Failed to connect to domain. {response=}", reply=reply)
    if address_type == address_type_ipv4:
        response = yield 4 + 2, None  # ip+port
        assert response == b"\x00" * 6
    elif address_type == address_type_ipv6:
        response = yield 16 + 2, None  # ip+port
        assert response == b"\x00" * 18
    else:
        raise SocksOSError(f"Unexpected response: {address_type=}")


async def socks_async_handshake(read_cb, write_cb, domain_name: str, port: int, username: str, password: str):
    sm = socks_state_machine(domain_name, port, username, password)
    data = None
    try:
        while True:
            read_n, write_b = sm.send(data)
            if write_b:
                await write_cb(write_b)
            if read_n:
                data = await read_cb(read_n)
            else:
                data = None
    except StopIteration:
        return


def socks_sync_handshake(read_cb, write_cb, domain_name: str, port: int, username: str, password: str):
    sm = socks_state_machine(domain_name, port, username, password)
    data = None
    try:
        while True:
            read_n, write_b = sm.send(data)
            if write_b:
                write_cb(write_b)
            if read_n:
                data = read_cb(read_n)
            else:
                data = None
    except StopIteration:
        return


async def socks_aio_handshake(reader: StreamReader, writer: StreamWriter, domain_name: str, port: int, username: str,
                              password: str):
    async def write_cb(b: bytes):
        writer.write(b)

    async def read_cb(n: int):
        return await reader.read(n)

    await socks_async_handshake(read_cb, write_cb, domain_name, port, username, password)


def socks_socket_handshake(sock, domain_name, port, username, password):
    def write_cb(b: bytes):
        sock.sendall(b)

    def read_cb(n: int):
        return sock.recv(n)

    socks_sync_handshake(read_cb, write_cb, domain_name, port, username, password)


async def socks_connect(domain_name: str, port: int, socks_host=None, socks_port=9050, socks_username: str = None,
                        socks_password: str = None):
    reader, writer = await asyncio.open_connection(host=socks_host, port=socks_port)
    await socks_aio_handshake(reader, writer, domain_name, port, socks_username, socks_password)
    return reader, writer


async def socks_unix_connect(domain_name: str, port: int, socks_path: Path, socks_username: str = None,
                             socks_password: str = None):
    reader, writer = await asyncio.open_unix_connection(socks_path)
    await socks_aio_handshake(reader, writer, domain_name, port, socks_username, socks_password)
    return reader, writer


async def start_tls(domain_name, transport, ssl_context=None):
    loop = asyncio.get_running_loop()
    ctx = ssl_context or ssl.create_default_context()
    reader = StreamReader(loop=loop)
    protocol = StreamReaderProtocol(reader)
    new_transport = await loop.start_tls(transport, protocol, sslcontext=ctx, server_hostname=domain_name)
    writer = StreamWriter(new_transport, protocol, reader, loop)
    return reader, writer


def get_socks_connector_tcp(socks_host: str, socks_port: int, socks_username: str, socks_password: str):
    # replace socket.create_connection
    def create_connection(address, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, source_address=None):
        sock = None
        try:
            sock = socket.create_connection((socks_host, socks_port), timeout, source_address)
            host, port = address
            socks_socket_handshake(sock, host, port, socks_username, socks_password)
        except:
            if sock is not None:
                sock.close()
            raise
        return sock

    return create_connection


class UnixSock:
    def __init__(self, real_sock):
        self.real_sock = real_sock

    # noinspection SpellCheckingInspection
    def setsockopt(self, *args):
        # HTTPConnection Tries to set tcp nodelay which is invalid for unix socket
        pass

    def __getattr__(self, item):
        return getattr(self.real_sock, item)


def get_socks_connector_unix(socks_path: Path, username: str, password: str):
    # replace socket.create_connection
    def create_connection(address, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, source_address=None):
        if source_address:
            raise SocksValueError("Source address not supported")
        host, port = address
        sock = None
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            if timeout is not socket._GLOBAL_DEFAULT_TIMEOUT:
                # noinspection PyTypeChecker
                sock.settimeout(timeout)
            sock.connect(str(socks_path))
            socks_socket_handshake(sock, host, port, username, password)
            return UnixSock(sock)
        except:
            if sock is not None:
                sock.close()
            raise

    return create_connection


def build_opener(*handlers,
                 socks_path: Path = None,
                 socks_host: str = None, socks_port: int = None,
                 socks_username: str = None,
                 socks_password: str = None,
                 https_args: (list, dict) = None,
                 ):
    if not check_either(socks_path, (socks_host is not None, socks_port)):
        raise SocksValueError("Pass either (socks_host and socks_port) or socks_path")
    if socks_path:
        connection_opener = get_socks_connector_unix(socks_path, socks_username, socks_password)
    else:
        connection_opener = get_socks_connector_tcp(socks_host, socks_port, socks_username, socks_password)

    def wrapped_connection_class(http_class):
        def inner(*args, **kwargs):
            h = http_class(*args, **kwargs)
            h._create_connection = connection_opener
            return h

        return inner

    class WrappedHandler(HTTPHandler, HTTPSHandler):
        def __init__(self, *args, **kwargs):
            nonlocal https_args
            if https_args:
                https_args, https_kwargs = https_args
                if https_args:
                    args = args + https_args
                if https_kwargs:
                    kwargs.update(https_kwargs)
            super().__init__(*args, **kwargs)

        def do_open(self, http_class, *args, **kwargs):
            return super().do_open(wrapped_connection_class(http_class), *args, **kwargs)

    return urllib_build_opener(*handlers, WrappedHandler)
