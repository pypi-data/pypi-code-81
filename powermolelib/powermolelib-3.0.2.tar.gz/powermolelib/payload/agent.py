#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: agent.py
#
# Copyright 2021 Vincent Schouten
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
#

"""
Main code for Agent.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import socket
import os
import logging.config
# import coloredlogs
import threading
import http.server
import socketserver
import json
import subprocess
import select
import sys
import atexit
import signal
from abc import ABC
from struct import pack, unpack
from time import sleep

# Constants
LOCAL_PORT_AGENT = 44191  # the local port the agent uses to listen for instructions from Instructor.
# IMPORTANT NOTE: other ports are sent via an Instructor class which receives it from the CLI.

# Configuration for SOCKS proxy server classes
MAX_THREADS = 200
BUFSIZE = 2048
TIMEOUT_SOCKET = 5
VER = b'\x05'  # PROTOCOL VERSION 5
M_NOAUTH = b'\x00'  # '00' NO AUTHENTICATION REQUIRE
M_NOTAVAILABLE = b'\xff'  # 'FF' NO ACCEPTABLE METHODS
CMD_CONNECT = b'\x01'  # CONNECT '01'
ATYP_IPV4 = b'\x01'  # IP V4 address '01'
ATYP_DOMAINNAME = b'\x03'  # DOMAINNAME '03'

# Logging
LOGGER = logging.getLogger()  # not used?
LOGGER_BASENAME = '''Agent'''


class LoggerMixin:  # pylint: disable=too-few-public-methods
    """Contains a logger method for use by other classes."""

    def __init__(self):
        """Initialize the LoggerMixin object."""
        self._logger = logging.getLogger(f'{LOGGER_BASENAME}.{self.__class__.__name__}')


class TransferError(Exception):
    """Something went wrong during transfer of the file."""


def validate_http_instruction(request):
    """Validates the data structure of the content of an incoming HTTP request.

    These requests are received by the Agent.
    """
    process = ['transfer_server_start', 'file_server_stop', 'proxy_server_start', 'proxy_server_stop',
               'heartbeat_responder_start', 'heartbeat_responder_stop', 'command_server_start', 'command_server_stop',
               'stop']  # 'authenticate_host'
    if not all([request.get('process') in process,
                isinstance(request.get('arguments'), dict)]):
        raise InvalidDataStructure
    return request.get('process'), request.get('arguments', {})


def validate_http_command(request):
    """Validates the data structure of the content of an incoming HTTP request.

    These requests are received by the CommandServer and contains Linux commands.
    """
    if isinstance(request.get('command'), str):
        return request
    raise InvalidDataStructure


class InvalidDataStructure(Exception):
    """The data structure is invalid."""

    def __init__(self):
        super().__init__("the data structure is invalid.")


class Agent(LoggerMixin):
    """Listens for instructions send by *Instructor."""

    def __init__(self, local_port_agent):
        """Initialize the Agent object.

        Args:
            local_port_agent (basestring): The local port used to listen for instructions from *Instructor.

        """
        super().__init__()
        self.listening_port = local_port_agent
        self.httpd = None
        self.terminate = False
        self.transfer_server = None
        self.command_server = None
        self.heartbeat_responder = None
        self.proxy_server = None
        self.authenticate = None

    def __str__(self):
        return 'Agent'

    def start(self):
        """Listens for incoming HTTP POST request."""
        self._logger.debug('starting agent')
        threading.Thread(target=self._watcher).start()
        agent = self

        class Handler(http.server.SimpleHTTPRequestHandler):
            """Parses HTTP requests."""

            logger_name = u'{base}.{suffix}'.format(base=LOGGER_BASENAME,
                                                    suffix='Handler')
            _logger = logging.getLogger(logger_name)
            socketserver.TCPServer.allow_reuse_address = True

            def do_POST(self):
                """Creates the response."""
                try:
                    data = self.rfile.read(int(self.headers['Content-Length']))  # b'{"process":"heartbeat_responder"}
                    self._logger.debug('the following request was received from *Instructor: %s', data)
                    instruction_string = data.decode('utf-8')  # convert byte to string (to original JSON document)
                    instruction_dict = json.loads(instruction_string)  # convert JSON to dict
                    # example: {'process': 'transfer_server_start', 'arguments': {'local_port': 44194}}
                    # validate structure of content of req:
                    process, arguments = validate_http_instruction(instruction_dict)
                except json.decoder.JSONDecodeError:  # json.loads()
                    self._logger.error('the content is incorrectly parsed in JSON')
                    process = 'default'  # to enter exit branch
                    arguments = {}
                except InvalidDataStructure:  # validate_http_instruction()
                    self._logger.error('data structure (dict) validation failed')
                    process = 'default'  # to enter exit branch
                    arguments = {}

                if getattr(agent, f'{process}')(**arguments):  # getattr(agent, transfer_server_start(local_port:44194))
                    self.send_response(200)
                    self.end_headers()
                    json_instruction = json.dumps({'result': True})
                    data = json_instruction.encode('utf-8')  # from string to byte
                    self.wfile.write(data)
                else:
                    self.send_response(200)
                    self.end_headers()
                    json_instruction = json.dumps({'result': False})
                    data = json_instruction.encode('utf-8')  # from string to byte
                    self.wfile.write(data)

        with socketserver.TCPServer(("", self.listening_port), Handler) as agent.httpd:
            self._logger.debug('serving at port %s', self.listening_port)
            agent.httpd.serve_forever()

    def _watcher(self):
        while True:
            if self.terminate:
                self._logger.debug('sending shutdown()')
                self.httpd.shutdown()
                break

    def stop(self):
        """Stops the Agent."""
        self._logger.debug('stopping heartbeat responder, and transfer, command and proxy server if running')
        self.file_server_stop()
        self.proxy_server_stop()
        self.heartbeat_responder_stop()
        self.command_server_stop()
        self._logger.debug('stopping agent')
        self.terminate = True
        return True

    def transfer_server_start(self, **kwargs):
        """Starts the transfer server."""
        local_port = kwargs.get('local_port')
        self.transfer_server = TransferServer(local_port=local_port)
        return self.transfer_server.start()

    def file_server_stop(self):
        """Stops the transfer server."""
        return self.transfer_server.stop()

    def proxy_server_start(self, **kwargs):
        """Starts the proxy server."""
        local_addr_i = kwargs.get('remote_address_i')
        local_port_i = kwargs.get('remote_port_i')
        local_addr_e = kwargs.get('remote_address_e')
        self.proxy_server = ProxyServer(local_addr_i=local_addr_i,
                                        local_port_i=local_port_i,
                                        local_addr_e=local_addr_e)
        return self.proxy_server.start()

    def proxy_server_stop(self):
        """Stops the proxy server."""
        return True if self.proxy_server is None else self.proxy_server.stop()

    def command_server_start(self, **kwargs):
        """Starts the command server."""
        local_port = kwargs.get('local_port')
        self.command_server = CommandServer(local_port=local_port)
        return self.command_server.start()

    def command_server_stop(self):
        """Stops the command server."""
        return self.command_server.stop()

    def heartbeat_responder_start(self, **kwargs):
        """Starts the heartbeat responder."""
        local_port = kwargs.get('local_port')
        self.heartbeat_responder = HeartbeatResponder(local_port=local_port)
        return self.heartbeat_responder.start()

    def heartbeat_responder_stop(self):
        """Stops the heartbeat responder."""
        return True if self.heartbeat_responder is None else self.heartbeat_responder.stop()

    def default(self):
        """Stops the Agent."""
        self._logger.debug('the process is unknown')
        self.stop()


class TransferServer(LoggerMixin):
    """Receives file(s) send by *Instructor()."""

    def __init__(self, local_port):
        """Initializes the TransferServer object."""
        super().__init__()
        self.listening_port = local_port
        self.data_protocol = None
        self.terminate = False

    def start(self):
        """Starts transfer server."""
        self._logger.debug('starting transfer server')
        self.data_protocol = DataProtocol(self.listening_port)
        self.data_protocol.start()
        threading.Thread(target=self._receiver).start()
        return True

    def stop(self):
        """Stops transfer server."""
        self._logger.debug('stopping transfer server')
        self.terminate = True
        self.data_protocol.stop()
        return True

    def _receiver(self):
        try:
            while not self.terminate:
                metadata = self.data_protocol.receive_metadata()
                self.data_protocol.receive_file(metadata)
                sleep(0.5)  # is this necessary?
        except TransferError:
            self._logger.error('')


class SocketServer(LoggerMixin):
    """Manages the socket for the transfer server."""

    def __init__(self):
        super().__init__()
        self.socket_ = None
        self.connections = []

    def _create_socket_and_listen(self, listening_port):
        self.socket_ = socket.socket()
        host = ''
        self.socket_.bind((host, listening_port))
        self._logger.debug('serving at port %s', listening_port)
        self.socket_.listen(2)
        self._logger.debug('waiting for a connection...')

    def _handle_connections(self):

        def _conn_handler():
            while self.socket_.fileno() != -1:  # keep listening to new connections
                connection, host_port = self.socket_.accept()  # blocking. calling close() will raise exception
                self._logger.debug('a connection received from %s', str(host_port))
                self.connections.append(connection)

        threading.Thread(target=_conn_handler).start()

    def _close_socket(self):  # https://stackoverflow.com/questions/409783/socket-shutdown-vs-socket-close
        self.socket_.shutdown(socket.SHUT_RDWR)
        # closes the underlying connection and sends a FIN / EOF to the peer regardless of how many processes have
        # handles to the socket. However, it does not deallocate the socket and you still need to call close afterwards
        self.socket_.close()
        # it decrements the handle count by one and if the handle count has reached zero then the socket and associated
        # connection goes through the normal close procedure (effectively sending a FIN / EOF to the peer) and the
        # socket is deallocated. The thing to pay attention to here is that if the handle count does not reach zero
        # because another process still has a handle to the socket then the connection is not closed and the socket is
        # not deallocated.


class DataProtocol(SocketServer):  # Costas, it would be nice to have LoggerMixin as an argument
    """Decodes file metadata and writes received data to a new file."""

    def __init__(self, listening_port):
        """Initializes the DataProtocol object."""
        super().__init__()
        self.listening_port = listening_port

    def start(self):
        """Binds a socket and handles incoming connections."""
        self._create_socket_and_listen(self.listening_port)
        self._handle_connections()

    def stop(self):
        """Closes the socket."""
        self._close_socket()

    def receive_metadata(self):
        """Decodes the metadata."""
        if not self.connections:
            return
        connection = self.connections[-1]
        process = connection.recv(8)
        if process != b'metadata':
            return
        metadata = {'dest_path': None,
                    'file_name': None,
                    'file_size': None
                    }
        for key, value in metadata.items():
            try:
                length_binary = connection.recv(16)
                length_int = int(length_binary, 2)
                metadata[key] = connection.recv(length_int)
                self._logger.debug('%s: %s received' % (key, metadata[key]))
            except IOError:
                self._send_status_code(connection, 'metadata', 1)
        self._send_status_code(connection, 'metadata', 0)
        return metadata  # {'dest_path': b'/tmp', 'file_name': b'amsterdam.jpg', 'file_size': b'98130'

    def receive_file(self, metadata):
        """Writes the received data to a file."""
        if not metadata:
            return
        connection = self.connections.pop()
        process = connection.recv(8)
        if process != b'filedata':
            return
        file_size = int(metadata['file_size'])
        try:
            file_to_write = open(os.path.join(metadata['dest_path'],
                                              metadata['file_name']), 'wb')  # can raise: "No such file or directory"
            chunksize = 4096
            while file_size > 0:
                if file_size < chunksize:
                    chunksize = file_size
                    self._logger.debug('receiving last chunk of data...')
                data = connection.recv(chunksize)
                file_to_write.write(data)
                file_size -= len(data)
            file_to_write.close()
            self._logger.debug('received all chunks of data')
        except OSError:  # raised by open() or socket()
            self._send_status_code(connection, 'filedata', 1)
        self._send_status_code(connection, 'filedata', 0)

    def _send_status_code(self, connection, process, status_code):
        if process == 'metadata' and status_code == 0:
            self._logger.debug('metadata is received successfully')
        elif process == 'filedata' and status_code == 0:
            self._logger.debug('filedata is received successfully')
        else:
            self._logger.debug('something went wrong')
        msg = {'process': f'{process}', 'status_code': int(status_code)}
        json_instruction = json.dumps(msg)  # from dict to JSON
        data = json_instruction.encode('utf-8')  # from string to byte
        connection.sendall(data)


class CommandServer(LoggerMixin):
    """Listens for Linux commands send by *Instructor() and responds with result."""

    #  determine first whether port is bind or not
    #  < code >
    #  self._logger.error('Port already bind. Probably by having executed this method twice.')

    def __init__(self, local_port):
        """Initialize the CommandServer object.

        Args:
            local_port (basestring): <>

        """
        super().__init__()
        self.listening_port = local_port
        self.httpd = None
        self.terminate = False

    def start(self):
        """Listens for connections."""
        self._logger.debug('starting command server...')
        threading.Thread(target=self._watcher).start()
        threading.Thread(target=self._serve).start()
        return True

    def _serve(self):
        """Listens for incoming HTTP POST request."""
        instance = self

        class Handler(http.server.SimpleHTTPRequestHandler):
            """Parses HTTP requests."""

            logger_name = u'{base}.{suffix}'.format(base=LOGGER_BASENAME,
                                                    suffix='Handler')
            _logger = logging.getLogger(logger_name)
            # socketserver.BaseRequestHandler.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            socketserver.TCPServer.allow_reuse_address = True

            def do_POST(self):  # pylint: disable=invalid-name
                """Creates the response containing the result."""
                try:
                    data = self.rfile.read(int(self.headers['Content-Length']))  # b'{"command":"ls -l /"}
                    self._logger.debug('following raw Linux command was received from instructor: %s', data)
                    command_string = data.decode('utf-8')  # convert byte to string in JSON format
                    command_dict = json.loads(command_string)  # convert JSON to dict
                    command_val = validate_http_command(command_dict)  # validate the structure of the content of req.
                    command = command_val.get('command')
                    instance._logger.debug('following Linux command was received from instructor: %s', command)
                    # eg. b'{"command": "hostname"}'
                except json.decoder.JSONDecodeError:  # json.loads()
                    self._logger.error('the content is incorrectly parsed in JSON')
                    return False
                except InvalidDataStructure:  # validate_http_instruction()
                    self._logger.error('data structure (dict) validation failed')
                    return False
                result_command = instance._issue_command(command.split())
                self.send_response(200)
                self.end_headers()
                self.wfile.write(result_command)
                result = True
                return result

        with socketserver.TCPServer(("", self.listening_port), Handler) as instance.httpd:
            self._logger.debug('serving at port %s', self.listening_port)
            instance.httpd.serve_forever()

    def _watcher(self):
        while True:
            if self.terminate:
                self._logger.debug('sending shutdown()')
                self.httpd.shutdown()
                break

    def _issue_command(self, command):
        result = b'ERROR: command not recognized'
        try:
            result = subprocess.check_output(command).rstrip()
            self._logger.debug('result of Linux commando is %s', result)  # eg. b'server.enterprise.com'
        except FileNotFoundError:
            self._logger.error('Linux command could not be executed')
        finally:
            return result

    def stop(self):
        """Stops the command server."""
        self._logger.debug('stopping command server')
        self.terminate = True
        return True


class HeartbeatResponder(LoggerMixin):
    """Responds to GET requests from powermolecli with HTTP code 200."""

    #  determine first whether port is bind or not
    #  self._logger.error('Port already bind. Probably by having executed this method twice.')

    def __init__(self, local_port):
        super().__init__()
        self.listening_port = local_port
        self.httpd = None
        self.terminate = False

    def start(self):
        """Executes the HTTP server that responds to GET requests (heartbeats) from powermolecli."""
        self._logger.debug('starting heartbeat responder...')
        threading.Thread(target=self._watcher).start()
        threading.Thread(target=self._serve).start()
        return True

    def _serve(self):
        instance = self

        class Handler(http.server.SimpleHTTPRequestHandler):
            """Parses HTTP requests."""

            def __init__(self, *args, **kwargs):
                # kwargs['directory'] = directory  # I had to comment out, because -->
                super().__init__(*args, **kwargs)  # --> "TypeError: __init__ got an unexpected kwarg 'directory'"

            def do_GET(self):
                """Creates the response."""
                instance._logger.debug('GET request received')
                self.send_response(200)
                self.end_headers()

        with socketserver.TCPServer(("", self.listening_port), Handler) as instance.httpd:
            self._logger.debug('serving at port %s', self.listening_port)
            instance.httpd.serve_forever()

    def _watcher(self):
        while True:
            if self.terminate:
                self._logger.debug('sending shutdown()')
                self.httpd.shutdown()
                break

    def stop(self):
        """Terminates the HTTP server responsible for responding to GET request (heartbeats) from powermolecli."""
        self._logger.debug('stopping heartbeat responder')
        self.terminate = True
        return True


# Daemon in Python
# from Costas Tyfoxylos costas.tyf@gmail.com
# 2019-10-17: Refactored by myself (Vincent Schouten)

# Sources:
# [1] Based on http://web.archive.org/
#                        web/20131025230048/http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/
#   The changes are:
#   1 - Uses file open context managers instead of calls to file().
#   2 - Forces stdin to /dev/null. stdout and stderr go to log files.
#   3 - Uses print instead of sys.stdout.write prior to pointing stdout to the log file.
#   4 - Omits try/excepts if they only wrap one error message w/ another.
# [2] https://stackoverflow.com/questions/33560802/pythonhow-os-fork-works
# [3] https://stackoverflow.com/questions/8777602/why-must-detach-from-tty-when-writing-a-linux-daemon


class Daemon(ABC):
    """Instantiates the daemon."""

    def __init__(self, pid_file=None, stdout=None, stderr=None):
        self.stdout = stdout or './daemon_out.log'
        self.stderr = stderr or './daemon_err.log'
        self.pid_file = pid_file or './daemon.pid'

    def _remove_pid(self):
        """Deletes the pid file."""
        os.remove(self.pid_file)

    def _daemonize(self):
        """Double forking of the process."""
        # fork 1 to spin off the child that will spawn the daemon.
        if os.fork() > 0:
            sys.exit(0)  # exit first parent
        # This is the child.

        # 1. clear the session id to clear the controlling TTY.
        # 2. set the umask so we have access to all files created by the daemon.
        os.setsid()
        os.umask(0)

        # fork 2 ensures we can't get a controlling TTY [ttd]?
        if os.fork() > 0:
            sys.exit(0)  # exit from second parent
        # This is a child that can't ever have a controlling TTY.

        # redirect standard file descriptor for *stdin* (essentially shut down stdin)
        with open('/dev/null', 'r') as dev_null:
            os.dup2(dev_null.fileno(), sys.stdin.fileno())  # os.dup <-- duplicate file descriptor

        # redirect standard file descriptor for *stderr* to log file
        sys.stderr.flush()
        with open(self.stderr, 'a+') as stderr:
            os.dup2(stderr.fileno(), sys.stderr.fileno())  # os.dup <-- duplicate file descriptor

        # redirect standard file descriptor for *stdout* to log file
        sys.stdout.flush()
        with open(self.stdout, 'a+') as stdout:
            os.dup2(stdout.fileno(), sys.stdout.fileno())  # os.dup <-- duplicate file descriptor

        # registered functions are executed automatically when the interpreter session is terminated normally.
        atexit.register(self._remove_pid)

        #   py interpreter
        #    |
        #   (fork) < duplicate itself
        #    |
        #    ├─ parent < exit this process!
        #    |
        #   (setsid) < detach from the terminal (ie. no controlling TTY) to avoid certain signals
        #    |
        #   (fork) < duplicate itself
        #    |
        #    ├─ parent < exit this process!
        #    |
        #    └─ child < store the pid of this process
        #
        pid = str(os.getpid())

        # write pid to file
        with open(self.pid_file, 'w') as pid_f:
            pid_f.write('{0}'.format(pid))

    @property
    def pid(self):
        """Returns the pid read from the pid file."""
        try:
            with open(self.pid_file, 'r') as pid_file:
                pid = int(pid_file.read().strip())
            return pid
        except IOError:
            return

    def start(self, function):
        """Starts the daemon."""
        # print('Starting...')
        if self.pid:
            print(('PID file {0} exists. '
                   'Is the daemon already running?').format(self.pid_file))
            sys.exit(1)
        self._daemonize()
        function()

    def stop(self):
        """Stops the daemon."""
        print('Stopping...')
        if not self.pid:
            print(("PID file {0} doesn't exist. "
                   "Is the daemon not running?").format(self.pid_file))
            return
        try:
            while 1:
                os.kill(self.pid, signal.SIGTERM)
                sleep(0.1)
        except OSError as err:
            if 'No such process' in err.strerror and \
                    os.path.exists(self.pid_file):
                os.remove(self.pid_file)
            else:
                print(err)
                sys.exit(1)

    def restart(self, function):
        """Restarts the daemon."""
        self.stop()
        self.start(function)


# Small Socks5 Proxy Server in Python
# from https://github.com/MisterDaneel/
# 2019-10-17: Refactored by myself (Vincent Schouten)


class ProxyServer(LoggerMixin):
    """De-encapsulating incoming (and forwarded) connection from client (localhost).

    This class interacts with the SOCKS proxy server module.

    """

    def __init__(self, local_addr_i, local_port_i, local_addr_e=None):
        """Initializes a Proxy object."""
        super().__init__()
        self.local_addr_i = local_addr_i
        self.local_port_i = local_port_i
        self.local_addr_e = local_addr_e
        self.new_socket = None
        self.thread = None

    def start(self):
        """Starts the SOCKS proxy server."""
        try:
            self.new_socket = SocketServerInternal(self.local_addr_i, self.local_port_i)
            self.new_socket.create_socket_and_listen()
            self.thread = threading.Thread(target=self._execution)
            self.thread.start()
            self._logger.info("SOCKS proxy server started.")
        except Exception:
            self._logger.exception('something broke...')  # Exception need to be specific
            return False
        return True

    def stop(self):
        """Stops the SOCKS proxy server."""
        try:
            ExitStatus.set_status(True)
            self._logger.info("SOCKS proxy server stopped.")
        except Exception:
            self._logger.exception('something broke')
            return False
        return True

    def _execution(self):
        while not ExitStatus.get_status():
            if threading.activeCount() > MAX_THREADS:
                sleep(3)
                continue
            try:
                conn, _ = self.new_socket.sock.accept()
                conn.setblocking(True)  # 1 == True and 0 == False
            except socket.timeout:
                # @Daneel, could you please explain why this exception happens and how this can be mitigated?
                # @Vincent, this exception happens because the socket timeout after TIMEOUT_SOCKET seconds (in script
                # header) Without this timeout, the program will be stuck on accept until a connection happens
                # and cannot manage an EXIT signal (while condition)
                continue
            recv_thread = threading.Thread(target=connection, args=(conn, self.local_addr_e))
            recv_thread.start()
        self._logger.info("closing socket...")
        self.new_socket.sock.close()


class ExitStatus:
    """Manages exit status."""

    exit = False

    @classmethod
    def set_status(cls, status):
        """Sets exist status."""
        cls.exit = status

    @classmethod
    def get_status(cls):
        """Gets exit status."""
        return cls.exit


class Request(LoggerMixin):
    """___________________-.

    Once the method-dependent subnegotiation has completed, the client
    sends the request details.  If the negotiated method includes
    encapsulation for purposes of integrity checking and/or
    confidentiality, these requests MUST be encapsulated in the method-
    dependent encapsulation.

    The SOCKS request is formed as follows:

    +----+-----+-------+------+----------+----------+
    |VER | CMD |  RSV  | ATYP | DST.ADDR | DST.PORT |
    +----+-----+-------+------+----------+----------+
    | 1  |  1  | X'00' |  1   | Variable |    2     |
    +----+-----+-------+------+----------+----------+

    Where:

    o  VER    protocol version: X'05'
    o  CMD
      o  CONNECT X'01'
      o  BIND X'02'
      o  UDP ASSOCIATE X'03'
    o  RSV    RESERVED
    o  ATYP   address type of following address
      o  IP V4 address: X'01'
      o  DOMAINNAME: X'03'
      o  IP V6 address: X'04'
    o  DST.ADDR       desired destination address
    o  DST.PORT desired destination port in network octet
      order

    The SOCKS server will typically evaluate the request based on source
    and destination addresses, and return one or more reply messages, as
    appropriate for the request type.
    """

    def __init__(self,
                 wrapper,
                 local_addr_e):
        """Initializes an Request object."""
        super().__init__()
        self.wrapper = wrapper
        self.local_addr_e = local_addr_e
        self.socket_src = None
        self.socket_dst = None

    def proxy_loop(self):
        """_______________.

        The select function blocks the thread until data is available
        on a specified socket
        Then the data is forwarded to the right recipient.
        """
        while not ExitStatus.get_status():
            try:
                reader, _, _ = select.select([self.wrapper, self.socket_dst], [], [], 1)
            except select.error as err:
                self._logger.debug('Select failed: %s', err)
                return
            if not reader:
                continue
            try:
                for sock in reader:
                    data = sock.recv(BUFSIZE)
                    if not data:
                        return
                    if sock is self.socket_dst:
                        self.wrapper.send(data)
                    else:
                        self.socket_dst.send(data)
            except socket.error as err:
                self._logger.debug('Loop failed: %s', err)
                return

    def request_client(self):
        """Returns the destination address and port found in the SOCKS request."""
        # +----+-----+-------+------+----------+----------+
        # |VER | CMD |  RSV  | ATYP | DST.ADDR | DST.PORT |
        # +----+-----+-------+------+----------+----------+
        try:
            s5_request = self.wrapper.recv(BUFSIZE)
        except ConnectionResetError:
            if self.wrapper != 0:
                self.wrapper.close()
            self._logger.debug("Error")
            return False
        # Check VER, CMD and RSV
        if (
                s5_request[0:1] != VER or
                s5_request[1:2] != CMD_CONNECT or
                s5_request[2:3] != b'\x00'
        ):
            return False
        # IPV4
        if s5_request[3:4] == ATYP_IPV4:
            dst_addr = socket.inet_ntoa(s5_request[4:-2])
            dst_port = unpack('>H', s5_request[8:len(s5_request)])[0]
        # DOMAIN NAME
        elif s5_request[3:4] == ATYP_DOMAINNAME:
            sz_domain_name = s5_request[4]
            dst_addr = s5_request[5: 5 + sz_domain_name - len(s5_request)]
            port_to_unpack = s5_request[5 + sz_domain_name:len(s5_request)]
            dst_port = unpack('>H', port_to_unpack)[0]
        else:
            return False
        return dst_addr, dst_port

    def request(self):
        """.

        The SOCKS request information is sent by the client as soon as it has
        established a connection to the SOCKS server, and completed the
        authentication negotiations.  The server evaluates the request, and
        returns a reply
        """
        dst = self.request_client()
        # Server Reply
        # +----+-----+-------+------+----------+----------+
        # |VER | REP |  RSV  | ATYP | BND.ADDR | BND.PORT |
        # +----+-----+-------+------+----------+----------+
        rep = b'\x07'
        bnd = b'\x00' + b'\x00' + b'\x00' + b'\x00' + b'\x00' + b'\x00'
        if dst:
            sse = SocketServerExternal(dst[0], dst[1], self.local_addr_e)
            self.socket_dst = sse.connect_to_dst()
        if not dst or self.socket_dst == 0:
            rep = b'\x01'
        else:
            rep = b'\x00'
            bnd = socket.inet_aton(self.socket_dst.getsockname()[0])
            bnd += pack(">H", self.socket_dst.getsockname()[1])
        reply = VER + rep + b'\x00' + ATYP_IPV4 + bnd
        try:
            self.wrapper.sendall(reply)
        except socket.error:
            if self.wrapper != 0:
                self.wrapper.close()
            return
        # start proxy
        if rep == b'\x00':
            self.proxy_loop()
        if self.wrapper != 0:
            self.wrapper.close()
        if self.socket_dst != 0:
            self.socket_dst.close()


class Subnegotiation(LoggerMixin):
    """____<summary in one line>___.

    The client connects to the server, and sends a version
    identifier/method selection message:

                    +----+----------+----------+
                    |VER | NMETHODS | METHODS  |
                    +----+----------+----------+
                    | 1  |    1     | 1 to 255 |
                    +----+----------+----------+

    The VER field is set to X'05' for this version of the protocol.  The
    NMETHODS field contains the number of method identifier octets that
    appear in the METHODS field.

    The server selects from one of the methods given in METHODS, and
    sends a METHOD selection message:

                          +----+--------+
                          |VER | METHOD |
                          +----+--------+
                          | 1  |   1    |
                          +----+--------+

    If the selected METHOD is X'FF', none of the methods listed by the
    client are acceptable, and the client MUST close the connection.

    The values currently defined for METHOD are:

           o  X'00' NO AUTHENTICATION REQUIRED
           o  X'01' GSSAPI
           o  X'02' USERNAME/PASSWORD
           o  X'03' to X'7F' IANA ASSIGNED
           o  X'80' to X'FE' RESERVED FOR PRIVATE METHODS
           o  X'FF' NO ACCEPTABLE METHODS

    The client and server then enter a method-specific sub-negotiation.
    """

    def __init__(self, wrapper):
        """Initializes a Subnegotiation object."""
        super().__init__()
        self.wrapper = wrapper

    def subnegotiation_client(self):
        """.

        The client connects to the server, and sends a version
        identifier/method selection message
        """
        # Client Version identifier/method selection message
        # +----+----------+----------+
        # |VER | NMETHODS | METHODS  |
        # +----+----------+----------+
        try:
            identification_packet = self.wrapper.recv(BUFSIZE)
        except socket.error:
            self._logger.debug("Error")
            return M_NOTAVAILABLE
        # VER field
        if VER != identification_packet[0:1]:
            return M_NOTAVAILABLE
        # METHODS fields
        nmethods = identification_packet[1]
        methods = identification_packet[2:]
        if len(methods) != nmethods:
            return M_NOTAVAILABLE
        for method in methods:
            if method == ord(M_NOAUTH):
                return M_NOAUTH
        return M_NOTAVAILABLE

    def subnegotiation(self):
        """.

        The client connects to the server, and sends a version
        identifier/method selection message
        The server selects from one of the methods given in METHODS, and
        sends a METHOD selection message
        """
        method = self.subnegotiation_client()
        # Server Method selection message
        # +----+--------+
        # |VER | METHOD |
        # +----+--------+
        if method != M_NOAUTH:
            return False
        reply = VER + method
        try:
            self.wrapper.sendall(reply)
        except socket.error:
            self._logger.debug("Error")
            return False
        return True


class SocketServerExternal(LoggerMixin):  # pylint: disable=too-few-public-methods
    """Creates an INET, STREAMing socket for outgoing connections, *not* SOCKS encapsulated."""

    def __init__(self,
                 dst_addr,
                 dst_port,
                 local_addr_e):
        """Initializes a SocketServerExternal object."""
        super().__init__()
        self.dst_addr = dst_addr
        self.dst_port = dst_port
        self.local_addr_e = local_addr_e
        self.sock = None

    def connect_to_dst(self):
        """Returns a connected remote socket at desired address (found in SOCKS request)."""
        sock = self._create_socket()
        if self.local_addr_e:
            try:
                sock.setsockopt(
                    socket.SOL_SOCKET,
                    socket.AF_INET,
                    self.local_addr_e.encode()
                )
            except socket.error as err:
                self._logger.info("Error: %s", err)
                ExitStatus.set_status(True)
        try:
            sock.connect((self.dst_addr, self.dst_port))
            self._logger.info("Local external address: %s. Destination address: %s:%s.",
                              self.local_addr_e, self.dst_addr, self.dst_port)
            return sock
        except socket.error:
            self._logger.debug("Failed to connect to Destination")
            return 0

    def _create_socket(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(TIMEOUT_SOCKET)
        except socket.error as err:
            self._logger.debug("failed to create socket: %s", err)
            SystemExit(0)
        return self.sock


class SocketServerInternal(LoggerMixin):  # pylint: disable=too-few-public-methods
    """Creates an INET, STREAMing socket for incoming connections, SOCKS encapsulated."""

    def __init__(self,
                 local_addr,
                 local_port):
        """Initializes a SocketServerInternal object."""
        super().__init__()
        self.sock = None
        self.local_addr = local_addr
        self.local_port = local_port

    def create_socket_and_listen(self):
        """Creates a socket, binds it, and listens for incoming connections."""
        self._create_socket()
        self._bind()
        self._listen()

    def _create_socket(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(TIMEOUT_SOCKET)
        except socket.error as err:
            self._logger.debug("failed to create socket: %s", err)
            SystemExit(0)

    def _bind(self):
        try:
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((self.local_addr, self.local_port))
            self._logger.info("local internal address: %s:%s", self.local_addr, str(self.local_port))
        except socket.error as err:
            self._logger.debug("bind failed %s", err)
            self.sock.close()
            SystemExit(0)

    def _listen(self):
        try:
            self.sock.listen(10)
        except socket.error:
            self._logger.exception("listen failed")
            self.sock.close()
            SystemExit(0)
        return self.sock


def connection(wrapper, local_addr_e):
    """Identifies SOCKS request and sets up connection to destination."""
    subnegotiation = Subnegotiation(wrapper)
    if subnegotiation.subnegotiation():
        request = Request(wrapper, local_addr_e)
        request.request()


def main():
    """Main method."""
    logging.basicConfig(level='DEBUG',
                        filename='/tmp/log',
                        filemode='w',
                        format='%(asctime)s %(name)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    # coloredlogs.install(level='DEBUG')
    agent = Agent(LOCAL_PORT_AGENT)
    try:
        agent.start()
    except KeyboardInterrupt:
        agent.stop()
        raise SystemExit(0)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        deploy_path = sys.argv[1]
        pid_file = os.path.join(deploy_path, 'agent.pid')
        stdout = os.path.join(deploy_path, 'daemon_out.log')
        stderr = os.path.join(deploy_path, 'daemon_err.log')
        d = Daemon(pid_file=pid_file, stdout=stdout, stderr=stderr)
        d.start(main)
    else:
        print("no working path given")
#
#
# TransferServer  # I dont want to care about connections.
#     data_protol = DataProtocol
#
#     listen() --> accept
#
#     receive_file
#         data_protol.()
#
#
# DataProtocol(socketserver)
#
#     listen()
#     receive() + send_acknowledgment()
