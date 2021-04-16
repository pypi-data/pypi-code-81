# -*- coding: utf-8 -*-
"""
Description:
    This module contains all of the common util used for a test framework.

Author:
    Ray Gomez

Date:
    12/7/20
"""
import socket
import time

import requests

from epython import errors
from epython.environment import _LOG

VALID_PORT_STATES = ["UP", "DOWN"]


def wait_for_http_status_code(url, status_code=200, interval=1, timeout=90):
    """ Wait for a specific HTTP Status code from a given url

    Args:
        url (str): The url to wait to resolve
        status_code (int): The HTTP Status code to wait for
        timeout (int): The timeout in seconds (Default: 90)
        interval (int): The interval between retries in seconds (Default: 1)
    """

    _LOG.info("Waiting for url: %s to return status code: %s", url, status_code)
    start_time = time.time()
    while True:
        # Ignore connection issues
        try:
            rsp = requests.get(url)
            if rsp.status_code == status_code:
                return
        # pylint: disable=W0703
        except Exception:
            pass
        # pylint: enable=W0703

        if time.time() - start_time > timeout:
            break
        time.sleep(interval)
    raise errors.util.EPythonUtilException(f"Failed to receive status code: {status_code} from url: "
                                           f"{url} after {timeout} seconds")


def is_port_listening(host, port, wait_interval=2):
    """ Check if a port is up and listening

    Args:
        host (str): The FQDN or the IP address of the system in question
        port (int): The port to check
        wait_interval (int): The interval to wait before determining a port is down

    Returns:

    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        socket.setdefaulttimeout(wait_interval)
        result = sock.connect_ex((host, port))
        if result == 0:
            return True
        return False
    # pylint: disable=W0703
    except Exception:
        sock.close()
        return False
    # pylint: enable=W0703


def wait_for_port_down(host, port, max_wait=300, check_interval=10):
    """ Wait for a specified port to not be listening (down)

    Args:
        host (str): The FQDN or the IP address of the system in question
        port (int): The port to check
        max_wait (int): The maximum amount of time to wait for a port to have connectivity
        check_interval (int): The interval to wait before determining a port is down
    """
    wait_for_port_state(host, port, "DOWN", max_wait=max_wait, check_interval=check_interval)


def wait_for_port_state(host, port, state, max_wait=300, check_interval=10):
    """ Waits for a specified state (UP or DOWN) from a given port

    Args:
        host (str): The FQDN or the IP address of the system in question
        port (int): The port to check
        state (str): The state to wait for (UP, DOWN)
        max_wait (int): The maximum amount of time to wait for a port to have connectivity
        check_interval (int): The interval to wait before determining a port is down
    """

    # Guarantee uppercase
    state = state.upper()

    # Make sure we have a valid sate
    if state not in VALID_PORT_STATES:
        raise errors.network.EInvalidPortState(f"The state: '{state}' is not a recognized state, "
                                               f"please specify a valid state: {VALID_PORT_STATES}")

    # Determine whether or not the port should be listening
    listening = False
    if state.upper() == "UP":
        listening = True

    start_time = time.time()
    while time.time() - start_time < max_wait:
        if listening:
            if is_port_listening(host, port):
                _LOG.debug(f"Host '{host}' is listening on port '{port}', moving on...")
                return
            _LOG.debug(f"Host '{host}' is not listening on port '{port}', "
                       f"waiting {check_interval}s before trying again...")
        else:
            if not is_port_listening(host, port):
                _LOG.debug(f"Host '{host}' is no longer listening on port '{port}', moving on...")
                return
            _LOG.debug(f"Host '{host}' is still listening on port '{port}', "
                       f"waiting {check_interval}s before trying again...")
        time.sleep(check_interval)

    raise errors.network.EConnectivityException(f"Port {port} on host {host} failed to reach a(n) '{state}' "
                                                f"state in {max_wait} seconds.")


def wait_for_port_up(host, port, max_wait=300, check_interval=10):
    """ Wait for a specified port to be up (listening)

    Args:
        host (str): The FQDN or the IP address of the system in question
        port (int): The port to check
        max_wait (int): The maximum amount of time to wait for a port to have connectivity
        check_interval (int): The interval to wait before determining a port is down
    """
    wait_for_port_state(host, port, "UP", max_wait=max_wait, check_interval=check_interval)
