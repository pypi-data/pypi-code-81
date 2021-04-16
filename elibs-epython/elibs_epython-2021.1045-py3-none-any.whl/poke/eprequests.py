# -*- coding: utf-8 -*-
"""
Description:
    This module houses the Poke class, and the wrapped requests methods.

Author:
    Ray Gomez

Date:
    3/16/21
"""

import requests

from epython.environment import EPYTHON_REQUEST_ID, EPYTHON_REQUEST_RETRIES, EPYTHON_REQUEST_INTERVAL
from epython.handlers import basic_retry_handler

POKE_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-Request-ID": EPYTHON_REQUEST_ID
}

# These are the most common requests exceptions that will trigger a retry
# (this is explicit to show what is actually being retried on)
COMMON_REQUEST_EXCEPTIONS = (requests.exceptions.RequestException,
                             requests.exceptions.HTTPError,
                             requests.exceptions.ConnectionError,
                             requests.exceptions.Timeout,
                             requests.exceptions.ConnectTimeout,
                             requests.exceptions.ReadTimeout)


def get(url, params=None, data=None, auth=None, headers=None, timeout=None,
        verify=None, retries=EPYTHON_REQUEST_RETRIES, interval=EPYTHON_REQUEST_INTERVAL, **kwargs):
    """ Issue an HTTP GET request

    Args:
        url (str): The URL for the request
        params (dict): The parameters to send in the query string for a request
        data (obj): dict, list of tuples, bytes, or file-like object to send in the body of request
        auth (tuple): Auth tuple to enable Basic/Digest/Custom HTTP Auth
        headers (dict): HTTP Headers to send with the request
        timeout (int): How many seconds to wait for the server to send data
        verify (bool): Whether to verify the server's TLS certificate or not
        retries (int): The number of times to retry a request
        interval (int): The interval of wait time between each retry

    Returns:
        (obj): The vanilla response object, or a ResponseProcessor if one was requested.
    """
    if headers is None:
        headers = POKE_HEADERS

    @basic_retry_handler(COMMON_REQUEST_EXCEPTIONS, retries=retries, interval=interval)
    def __req():
        return requests.get(url, params=params, data=data, auth=auth, headers=headers, timeout=timeout,
                            verify=verify, **kwargs)
    return __req()


def put(url, params=None, data=None, auth=None, headers=None, timeout=None,
        verify=None, retries=EPYTHON_REQUEST_RETRIES, interval=EPYTHON_REQUEST_INTERVAL, **kwargs):
    """ Issue an HTTP PUT request

    Args:
        url (str): The URL for the request
        params (dict): The parameters to send in the query string for a request
        data (obj): dict, list of tuples, bytes, or file-like object to send in the body of request
        auth (tuple): Auth tuple to enable Basic/Digest/Custom HTTP Auth
        headers (dict): HTTP Headers to send with the request
        timeout (int): How many seconds to wait for the server to send data
        verify (bool): Whether to verify the server's TLS certificate or not
        retries (int): The number of times to retry a request
        interval (int): The interval of wait time between each retry

    Returns:
        (obj): The vanilla response object, or a ResponseProcessor if one was requested.
    """

    if headers is None:
        headers = POKE_HEADERS

    @basic_retry_handler(COMMON_REQUEST_EXCEPTIONS, retries=retries, interval=interval)
    def __req():
        return requests.put(url, params=params, data=data, auth=auth, headers=headers, timeout=timeout,
                            verify=verify, **kwargs)
    return __req()


def post(url, params=None, data=None, auth=None, headers=None, timeout=None,
         verify=None, retries=EPYTHON_REQUEST_RETRIES, interval=EPYTHON_REQUEST_INTERVAL, **kwargs):
    """ Issue an HTTP POST request

    Args:
        url (str): The URL for the request
        params (dict): The parameters to send in the query string for a request
        data (obj): dict, list of tuples, bytes, or file-like object to send in the body of request
        auth (tuple): Auth tuple to enable Basic/Digest/Custom HTTP Auth
        headers (dict): HTTP Headers to send with the request
        timeout (int): How many seconds to wait for the server to send data
        verify (bool): Whether to verify the server's TLS certificate or not
        retries (int): The number of times to retry a request
        interval (int): The interval of wait time between each retry

    Returns:
        (obj): The vanilla response object, or a ResponseProcessor if one was requested.
    """

    if headers is None:
        headers = POKE_HEADERS

    @basic_retry_handler(COMMON_REQUEST_EXCEPTIONS, retries=retries, interval=interval)
    def __req():
        return requests.post(url, params=params, data=data, auth=auth, headers=headers, timeout=timeout,
                             verify=verify, **kwargs)
    return __req()


def delete(url, params=None, data=None, auth=None, headers=None, timeout=None,
           verify=None, retries=EPYTHON_REQUEST_RETRIES, interval=EPYTHON_REQUEST_INTERVAL, **kwargs):
    """ Issue an HTTP DELETE request

    Args:
        url (str): The URL for the request
        params (dict): The parameters to send in the query string for a request
        data (obj): dict, list of tuples, bytes, or file-like object to send in the body of request
        auth (tuple): Auth tuple to enable Basic/Digest/Custom HTTP Auth
        headers (dict): HTTP Headers to send with the request
        timeout (int): How many seconds to wait for the server to send data
        verify (bool): Whether to verify the server's TLS certificate or not
        retries (int): The number of times to retry a request
        interval (int): The interval of wait time between each retry

    Returns:
        (obj): The vanilla response object, or a ResponseProcessor if one was requested.
    """

    if headers is None:
        headers = POKE_HEADERS

    @basic_retry_handler(COMMON_REQUEST_EXCEPTIONS, retries=retries, interval=interval)
    def __req():
        return requests.delete(url, params=params, data=data, auth=auth, headers=headers,
                               timeout=timeout, verify=verify, **kwargs)
    return __req()
