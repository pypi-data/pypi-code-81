#!/usr/bin/env python
#
# Copyright (C) 2019 Majormode.  All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import logging
import os
import sys

import psutil

from majormode.perseus.bootstrap import tornado_handler
import settings


DEFAULT_ADDRESS = '127.0.0.1'

DEFAULT_LOGGING_FORMATTER = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(getattr(settings, 'LOGGING_FORMATTER', DEFAULT_LOGGING_FORMATTER))
    return console_handler


def get_opened_port_processes():
    """
    Return the list of processes that have opened TCP or UDP ports.


    :return: A dictionary where the key corresponds to a port number and
        the value corresponds to the `psutil.Process` that has opened this
        port.


    :warning: multiple processes may bind a socket with the same port.
        This function only returns one process.
    """
    opened_port_processes = {}

    for process in psutil.process_iter():
        try:
            for connection in process.connections():
                if connection.status == psutil.CONN_LISTEN:
                    opened_port_processes[connection.laddr.port] = process

        except (psutil.AccessDenied, psutil.NoSuchProcess):
            pass

    return opened_port_processes


def reload(ports=None):
    raise NotImplementedError


def setup_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(getattr(settings, 'LOGGING_LEVEL', logging.INFO))
    logger.addHandler(get_console_handler())
    logger.propagate = False
    return logger


def start(ports, address=None):
    """
    Run the server application on the specified port(s).


    :param ports: A list of Internet Protocol port numbers which server
        application instances will listen at.  If more than one port is
        specified, the function will fork as many processes to listen at
        these additional ports.
        
    :param address: Address to bound the listening socket to.  Address may
        be either an IP address or hostname.  If it’s a hostname, the
        server will listen on all IP addresses associated with the name.
        Address may be an empty string or `None` to listen on all
        available interfaces.


    :raise Exception: if some of the specified ports are not currently
        available.

    :raise TypeError: if the argument `ports` is not a list.

    :raise ValueError: if no ports are specified.
    """
    if isinstance(ports, int):
        ports = [ports]
    elif not isinstance(ports, (list, tuple, set)):  # @note: better to test if ports is iterable
        raise TypeError('A list of ports is expected')
    elif len(ports) == 0:
        raise ValueError('No port number has been specified')

    # Retrieve the logger with the specified name or, if name is `None`,
    # the logger which is the root logger of the hierarchy.
    logger = setup_logger(getattr(settings, 'LOGGER_NAME'))

    # Check whether some of the specified port numbers are already used by
    # other processes.
    opened_ports = get_opened_port_processes()
    unavailable_ports = [port for port in ports if port in opened_ports]

    if len(unavailable_ports) > 0:
        raise Exception(
            'The following ports are already used: %s'
            % ', '.join([str(port) for port in unavailable_ports]))

    # Fork the process to run as many instances as the number of ports
    # passed to this function, including this instance.
    for port in ports[1:]:
        pid = os.fork()
        if pid == 0:  # Child process
            logger.info(f'Boot RESTful API server instance ({port})')
            tornado_handler.boot(port, settings.APP_PATH, address=address or DEFAULT_ADDRESS)

    logger.info(f'Boot RESTful API server instance ({ports[0]})')
    tornado_handler.boot(ports[0], settings.APP_PATH, address=address or DEFAULT_ADDRESS)


def stop(ports):
    """
    Terminate the current processes running that are listening TCP and
    UPD connections on the specified ports.


    :param ports: A list of Internet Protocol port numbers which the server
        application instances to stop are listening at.


    :return: A list of tuple `(psutil.Process, port)` of the processes
        that the function has terminated.
    """
    if isinstance(ports, int):
        ports = [ports]
    elif not isinstance(ports, (list, tuple, set)):  # @note: better to test if ports is iterable
        raise TypeError('A list of ports is expected')
    elif len(ports) == 0:
        raise ValueError('No port number has been specified')

    logger = setup_logger(getattr(settings, 'LOGGER_NAME'))
    logger.info('Stop RESTful API server application')

    terminated_processes = []

    for port, process in get_opened_port_processes().items():
        try:
            if port in ports and process.name().startswith('python'):
                process.terminate()
                process.wait(5000)
                terminated_processes.append((process, port))

        except psutil.AccessDenied:
            pass

    return terminated_processes
