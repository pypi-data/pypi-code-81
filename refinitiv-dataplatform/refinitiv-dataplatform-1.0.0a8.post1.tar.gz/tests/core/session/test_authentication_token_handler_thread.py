# coding: utf-8

###############################################################
#
#   STANDARD IMPORTS
#

import pytest

from unittest.mock import MagicMock, patch

import asyncio

import httpx

import time

import threading

###############################################################
#
#   REFINITIV IMPORTS
#

import refinitiv.dataplatform as rdp

###############################################################
#
#   LOCAL IMPORTS
#

###############################################################
#
#   TEST CASES
#

def test_authentication_token_handler_thread_constructor():
    ############################################
    #   prepare things

    session = MagicMock()
    grant = MagicMock()

    ############################################
    #   test

    authentication_handler = rdp.core._AuthenticationTokenHandlerThread(
                                            session, grant, 'foo')

    assert isinstance(authentication_handler, rdp.core._AuthenticationTokenHandlerThread)
    assert authentication_handler._server_mode == False
    assert authentication_handler._take_exclusive_sign_on_control == True
    assert not authentication_handler._request_new_authentication_token_event.is_set()
    assert not authentication_handler._start_event.is_set()
    assert not authentication_handler._stop_event.is_set()
    assert not authentication_handler._ready.is_set()
    assert not authentication_handler._error.is_set()

def test_authentication_token_handler_thread_constructor_with_optional_parameters():
    ############################################
    #   prepare things

    session = MagicMock()
    grant = rdp.core.GrantPassword()

    ############################################
    #   test

    authentication_handler = rdp.core._AuthenticationTokenHandlerThread(
                                            session, grant, 'foo',
                                            server_mode=True,
                                            take_exclusive_sign_on_control=False)

    assert isinstance(authentication_handler, rdp.core._AuthenticationTokenHandlerThread)
    assert authentication_handler._server_mode == True
    assert authentication_handler._take_exclusive_sign_on_control == False
    assert not authentication_handler._request_new_authentication_token_event.is_set()
    assert not authentication_handler._start_event.is_set()
    assert not authentication_handler._stop_event.is_set()
    assert not authentication_handler._ready.is_set()
    assert not authentication_handler._error.is_set()

def test_authentication_token_handler_thread_last_exception():
    ############################################
    #   prepare things

    session = MagicMock()
    grant = rdp.core.GrantPassword()

    ############################################
    #   test

    authentication_handler = rdp.core._AuthenticationTokenHandlerThread(
                                            session, grant, 'foo',
                                            server_mode=True,
                                            take_exclusive_sign_on_control=False)

    assert isinstance(authentication_handler, rdp.core._AuthenticationTokenHandlerThread)
    
    assert authentication_handler.last_exception == None

    authentication_handler._last_exception = 'bar'
    assert authentication_handler.last_exception == 'bar'

def test_authentication_token_handler_thread_is_error():
    ############################################
    #   prepare things

    session = MagicMock()
    grant = rdp.core.GrantPassword()

    ############################################
    #   test

    authentication_handler = rdp.core._AuthenticationTokenHandlerThread(
                                            session, grant, 'foo',
                                            server_mode=True,
                                            take_exclusive_sign_on_control=False)

    assert isinstance(authentication_handler, rdp.core._AuthenticationTokenHandlerThread)
    
    assert not authentication_handler.is_error()

    authentication_handler._error.set()
    assert authentication_handler.is_error()


def test_authentication_token_handler_thread_is_passsword_grant():
    ############################################
    #   prepare things

    session = MagicMock()
    grant = rdp.core.GrantPassword()

    ############################################
    #   test

    authentication_handler = rdp.core._AuthenticationTokenHandlerThread(
                                            session, grant, 'foo',
                                            server_mode=True,
                                            take_exclusive_sign_on_control=False)

    assert isinstance(authentication_handler, rdp.core._AuthenticationTokenHandlerThread)
    
    assert authentication_handler.is_passsword_grant()

def test_authentication_token_handler_thread_is_passsword_grant():
    ############################################
    #   prepare things

    session = MagicMock()
    grant = rdp.core.GrantRefreshToken()

    ############################################
    #   test

    authentication_handler = rdp.core._AuthenticationTokenHandlerThread(
                                            session, grant, 'foo',
                                            server_mode=True,
                                            take_exclusive_sign_on_control=False)

    assert isinstance(authentication_handler, rdp.core._AuthenticationTokenHandlerThread)
    
    assert not authentication_handler.is_passsword_grant()


def test_authentication_token_handler_thread_run():
    ############################################
    #   prepare things

    session = MagicMock()
    grant = rdp.core.GrantRefreshToken()

    ############################################
    #   test

    authentication_handler = rdp.core._AuthenticationTokenHandlerThread(
                                            session, grant, 'foo',
                                            server_mode=True,
                                            take_exclusive_sign_on_control=False)

    assert isinstance(authentication_handler, rdp.core._AuthenticationTokenHandlerThread)
    
    authentication_handler._authorize = lambda *args: None
    authentication_handler._request_refresh_token = lambda *args: time.sleep(1)
    authentication_handler._token_requested_time = time.time()
    authentication_handler._token_expires_in_secs = 10
    
    thread = threading.Thread(target=authentication_handler.run)
    
    #   wait for a token expired
    time.sleep(5)

    assert authentication_handler._ready.is_set()

    time.sleep(5)
    
    assert authentication_handler._request_new_authentication_token_event.is_set()

    time.sleep(2)

    assert authentication_handler._request_new_authentication_token_event.is_set()
    assert not authentication_handler._request_new_authentication_token_event.is_set()

    thread.join()

def test_authentication_token_handler_thread_stop():
    ############################################
    #   prepare things

    session = MagicMock()
    grant = rdp.core.GrantRefreshToken()

    ############################################
    #   test

    authentication_handler = rdp.core._AuthenticationTokenHandlerThread(
                                            session, grant, 'foo',
                                            server_mode=True,
                                            take_exclusive_sign_on_control=False)

    assert isinstance(authentication_handler, rdp.core._AuthenticationTokenHandlerThread)
    
    authentication_handler.join = lambda *args: None
    
    authentication_handler.stop()

    assert authentication_handler._stop_event.is_set()

def test_authentication_token_handler_thread_wait_for_authorize_ready():
    ############################################
    #   prepare things

    session = MagicMock()
    grant = rdp.core.GrantRefreshToken()

    ############################################
    #   test

    authentication_handler = rdp.core._AuthenticationTokenHandlerThread(
                                            session, grant, 'foo',
                                            server_mode=True,
                                            take_exclusive_sign_on_control=False)

    assert isinstance(authentication_handler, rdp.core._AuthenticationTokenHandlerThread)
    
    assert not authentication_handler._ready.is_set()
    
    start_time = time.time()
    authentication_handler.wait_for_authorize_ready()
    assert time.time() - start_time >= 5

    authentication_handler._ready.set()
    assert authentication_handler._ready.is_set()
    
    start_time = time.time()
    authentication_handler.wait_for_authorize_ready()
    assert time.time() - start_time <= 1