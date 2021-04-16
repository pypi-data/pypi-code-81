# coding: utf-8

###############################################################
#
#   STANDARD IMPORTS
#

import pytest

from unittest.mock import MagicMock
from unittest.mock import call

import asyncio

import json

###############################################################
#
#   REFINITIV IMPORTS
#

import refinitiv.dataplatform as rdp

from refinitiv.dataplatform import configure


###############################################################
#
#   LOCAL IMPORTS
#

###############################################################
#
#   TEST CASES
#


@pytest.mark.skip
@pytest.mark.asyncio
async def test_omm_stream_connection_ok(event_loop):
    thread_name = "name"
    stream_connection_name = ""
    mock_session = mock.AsyncMock()
    mock_session.name = "AsyncMock"
    mock_session._loop = event_loop
    mock_response = mock.MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"services": [{"dataFormat": ["tr_json2"],
                                                     "endpoint": "endpoint",
                                                     "location": ["location"],
                                                     "port": "port",
                                                     "provider": "provider",
                                                     "transport": "websocket"}],
                                       "locations": ["locations"]}
    mock_session.http_request_async = mock.AsyncMock(return_value=mock_response)
    connection_config = configure.config.get_dict('streaming.connections')

    stream_config = await StreamingConnectionConfiguration.build_streaming_connection_configuration(
        mock_session, "pricing", "platform_url", connection_config,
        dacs_position="", dacs_application_id=""
        )

    connection = rdp.OMMStreamConnection(thread_name, mock_session, stream_connection_name, stream_config)
    connection.start()
    assert connection is not None


def test_get_login_message():
    ############################################
    #   prepare things
    session = MagicMock()
    session.name = 'foo_logger'
    session._loop = asyncio.get_event_loop()
    session._get_new_id = lambda: 1

    config = MagicMock()

    ############################################
    #   test

    omm_stream_connection = rdp.delivery.OMMStreamConnection('foo_thread',
                                                             session,
                                                             'bar_connection',
                                                             config)

    login_message = omm_stream_connection._get_login_message()

    assert 'Domain' in login_message
    assert 'Login' == login_message['Domain']
    assert 'ID' in login_message
    assert type(login_message['ID']) == int
    assert 'Key' in login_message


def test_get_close_message():
    ############################################
    #   prepare things
    session = MagicMock()
    session.name = 'foo_logger'
    session._loop = asyncio.get_event_loop()

    config = MagicMock()

    ############################################
    #   test

    omm_stream_connection = rdp.delivery.OMMStreamConnection('foo_thread',
                                                             session,
                                                             'bar_connection',
                                                             config)
    omm_stream_connection._login_stream_event_id = 1

    login_message = omm_stream_connection._get_close_message()

    assert 'Domain' in login_message
    assert 'ID' in login_message
    assert 1 == login_message['ID']
    assert 'Type' in login_message
    assert 'Close' == login_message['Type']


def test_get_auth_message():
    ############################################
    #   prepare things
    session = MagicMock()
    session.name = 'foo_logger'
    session._loop = asyncio.get_event_loop()
    session._get_new_id = lambda: 1

    config = MagicMock()

    ############################################
    #   test

    omm_stream_connection = rdp.delivery.OMMStreamConnection('foo_thread',
                                                             session,
                                                             'bar_connection',
                                                             config)
    omm_stream_connection._login_stream_event_id = 2

    login_message = omm_stream_connection._get_auth_message()

    assert 'Domain' in login_message
    assert 'Login' == login_message['Domain']
    assert 'ID' in login_message
    assert type(login_message['ID']) == int
    assert 2 == login_message['ID']
    assert 'Key' in login_message


@pytest.mark.asyncio
async def test_set_stream_authentication_token():
    ############################################
    #   prepare things
    session = MagicMock()
    session.name = 'foo_logger'
    session._loop = asyncio.get_event_loop()

    config = MagicMock()

    ############################################
    #   test

    omm_stream_connection = rdp.delivery.OMMStreamConnection('foo_thread',
                                                             session,
                                                             'bar_connection',
                                                             config)
    omm_stream_connection._login_response_future = None
    omm_stream_connection.send = MagicMock()

    async def wait_and_process_login_response_message():
        return True

    omm_stream_connection._wait_and_process_login_response_message = wait_and_process_login_response_message

    await omm_stream_connection._set_stream_authentication_token('foo')

    omm_stream_connection.send.assert_called()


def test_ping():
    ############################################
    #   prepare things
    session = MagicMock()
    session.name = 'foo_logger'
    session._loop = asyncio.get_event_loop()

    config = MagicMock()

    ############################################
    #   test

    omm_stream_connection = rdp.delivery.OMMStreamConnection('foo_thread',
                                                             session,
                                                             'bar_connection',
                                                             config)
    omm_stream_connection.send = MagicMock()

    omm_stream_connection._ping()

    omm_stream_connection.send.assert_called()
    omm_stream_connection.send.assert_has_calls([call({'Type': 'Ping'})])


def test_pong():
    ############################################
    #   prepare things
    session = MagicMock()
    session.name = 'foo_logger'
    session._loop = asyncio.get_event_loop()

    config = MagicMock()

    ############################################
    #   test

    omm_stream_connection = rdp.delivery.OMMStreamConnection('foo_thread',
                                                             session,
                                                             'bar_connection',
                                                             config)
    omm_stream_connection.send = MagicMock()

    omm_stream_connection._pong()

    omm_stream_connection.send.assert_called()
    omm_stream_connection.send.assert_has_calls([call({'Type': 'Pong'})])


def test_on_message():
    ############################################
    #   prepare things
    session = MagicMock()
    session.name = 'foo_logger'
    session._loop = asyncio.get_event_loop()

    config = MagicMock()

    ############################################
    #   test

    omm_stream_connection = rdp.delivery.OMMStreamConnection('foo_thread',
                                                             session,
                                                             'bar_connection',
                                                             config)
    omm_stream_connection._process_response_message = MagicMock()

    omm_stream_connection._on_messages(json.dumps(['foo', 'bar']))

    assert omm_stream_connection._process_response_message.called is True
    omm_stream_connection._process_response_message.assert_has_calls([call('foo'), call('bar')])


def test_process_response_message_login():
    ############################################
    #   prepare things
    session = MagicMock()
    session.name = 'foo_logger'
    session._loop = asyncio.get_event_loop()

    config = MagicMock()

    ############################################
    #   test

    omm_stream_connection = rdp.delivery.OMMStreamConnection('foo_thread',
                                                             session,
                                                             'bar_connection',
                                                             config)
    omm_stream_connection._process_login_response_message = MagicMock()
    omm_stream_connection._process_refresh_message = MagicMock()
    omm_stream_connection._process_update_message = MagicMock()
    omm_stream_connection._process_status_message = MagicMock()
    omm_stream_connection._process_error_message = MagicMock()
    omm_stream_connection._pong = MagicMock()

    omm_stream_connection._on_ready = MagicMock()

    login_message = {
        "Domain": "Login",
        "Elements": {
            "MaxMsgSize": 61440,
            "PingTimeout": 30
            },
        "ID": 1,
        "Key": {
            "Elements": {
                "AllowSuspectData": 1,
                "ApplicationId": "555",
                "ApplicationName": "ADS",
                "AuthenticationErrorCode": 0,
                "AuthenticationErrorText": "Success",
                "Position": "127.0.0.1",
                "ProvidePermissionExpressions": 1,
                "ProvidePermissionProfile": 0,
                "SingleOpen": 1,
                "SupportBatchRequests": 7,
                "SupportEnhancedSymbolList": 1,
                "SupportOMMPost": 1,
                "SupportOptimizedPauseResume": 1,
                "SupportPauseResume": 1,
                "SupportStandby": 0,
                "SupportViewRequests": 1
                },
            "Name": "user"
            },
        "State": {
            "Data": "Ok",
            "Stream": "Open",
            "Text": "Login accepted by host."
            },
        "Type": "Refresh"
        }
    omm_stream_connection._process_response_message(login_message)

    omm_stream_connection._process_login_response_message.assert_called_once()
    omm_stream_connection._process_login_response_message.assert_called_once_with(login_message)

    omm_stream_connection._process_refresh_message.assert_not_called()
    omm_stream_connection._process_update_message.assert_not_called()
    omm_stream_connection._process_status_message.assert_not_called()
    omm_stream_connection._process_error_message.assert_not_called()
    omm_stream_connection._pong.assert_not_called()


def test_process_response_message_refresh():
    ############################################
    #   prepare things
    session = MagicMock()
    session.name = 'foo_logger'
    session._loop = asyncio.get_event_loop()

    config = MagicMock()

    ############################################
    #   test

    omm_stream_connection = rdp.delivery.OMMStreamConnection('foo_thread',
                                                             session,
                                                             'bar_connection',
                                                             config)
    omm_stream_connection._process_login_response_message = MagicMock()
    omm_stream_connection._process_refresh_message = MagicMock()
    omm_stream_connection._process_update_message = MagicMock()
    omm_stream_connection._process_status_message = MagicMock()
    omm_stream_connection._process_error_message = MagicMock()
    omm_stream_connection._pong = MagicMock()

    omm_stream_connection._on_ready = MagicMock()

    message = {
        "Fields": {
            "ASK": 9000,
            "BID": 0.01,
            "BIDSIZE": 1
            },
        "ID": 2,
        "Key": {
            "Name": "TRI.N",
            "Service": "DF_RMDS"
            },
        "QOS": {
            "Rate": "TickByTick",
            "Timeliness": "Realtime"
            },
        "State": {
            "Data": "Ok",
            "Stream": "Open",
            "Text": "All is well"
            },
        "Type": "Refresh"
        }

    omm_stream_connection._process_response_message(message)

    omm_stream_connection._process_refresh_message.assert_called_once()
    omm_stream_connection._process_refresh_message.assert_called_once_with(2, message)

    omm_stream_connection._process_login_response_message.assert_not_called()
    omm_stream_connection._process_update_message.assert_not_called()
    omm_stream_connection._process_status_message.assert_not_called()
    omm_stream_connection._process_error_message.assert_not_called()
    omm_stream_connection._pong.assert_not_called()


def test_process_response_message_update():
    ############################################
    #   prepare things
    session = MagicMock()
    session.name = 'foo_logger'
    session._loop = asyncio.get_event_loop()

    config = MagicMock()

    ############################################
    #   test

    omm_stream_connection = rdp.delivery.OMMStreamConnection('foo_thread',
                                                             session,
                                                             'bar_connection',
                                                             config)
    omm_stream_connection._process_login_response_message = MagicMock()
    omm_stream_connection._process_refresh_message = MagicMock()
    omm_stream_connection._process_update_message = MagicMock()
    omm_stream_connection._process_status_message = MagicMock()
    omm_stream_connection._process_error_message = MagicMock()
    omm_stream_connection._pong = MagicMock()

    omm_stream_connection._on_ready = MagicMock()

    message = {
        "Fields": {
            "ASK": 401.54,
            "BID": 401.5,
            "BIDSIZE": 18
            },
        "ID": 3,
        "Key": {
            "Name": "TRI.N",
            "Service": "DF_RMDS"
            },
        "Type": "Update",
        "UpdateType": "Quote"
        }

    omm_stream_connection._process_response_message(message)

    omm_stream_connection._process_update_message.assert_called_once()
    omm_stream_connection._process_update_message(3, message)

    omm_stream_connection._process_login_response_message.assert_not_called()
    omm_stream_connection._process_refresh_message.assert_not_called()
    omm_stream_connection._process_status_message.assert_not_called()
    omm_stream_connection._process_error_message.assert_not_called()
    omm_stream_connection._pong.assert_not_called()


def test_process_response_message_status():
    ############################################
    #   prepare things
    session = MagicMock()
    session.name = 'foo_logger'
    session._loop = asyncio.get_event_loop()

    config = MagicMock()

    ############################################
    #   test

    omm_stream_connection = rdp.delivery.OMMStreamConnection('foo_thread',
                                                             session,
                                                             'bar_connection',
                                                             config)
    omm_stream_connection._process_login_response_message = MagicMock()
    omm_stream_connection._process_refresh_message = MagicMock()
    omm_stream_connection._process_update_message = MagicMock()
    omm_stream_connection._process_status_message = MagicMock()
    omm_stream_connection._process_error_message = MagicMock()
    omm_stream_connection._pong = MagicMock()

    omm_stream_connection._on_ready = MagicMock()

    message = {
        "ID": 4,
        "State": {
            "Code": "UnsupportedViewType",
            "Data": "Suspect",
            "Stream": "Closed"
            },
        "Type": "Status",
        }

    omm_stream_connection._process_response_message(message)

    omm_stream_connection._process_status_message.assert_called_once()
    omm_stream_connection._process_status_message(4, message)

    omm_stream_connection._process_login_response_message.assert_not_called()
    omm_stream_connection._process_refresh_message.assert_not_called()
    omm_stream_connection._process_update_message.assert_not_called()
    omm_stream_connection._process_error_message.assert_not_called()
    omm_stream_connection._pong.assert_not_called()


def test_process_response_message_error():
    ############################################
    #   prepare things
    session = MagicMock()
    session.name = 'foo_logger'
    session._loop = asyncio.get_event_loop()

    config = MagicMock()

    ############################################
    #   test

    omm_stream_connection = rdp.delivery.OMMStreamConnection('foo_thread',
                                                             session,
                                                             'bar_connection',
                                                             config)
    omm_stream_connection._process_login_response_message = MagicMock()
    omm_stream_connection._process_refresh_message = MagicMock()
    omm_stream_connection._process_update_message = MagicMock()
    omm_stream_connection._process_status_message = MagicMock()
    omm_stream_connection._process_error_message = MagicMock()
    omm_stream_connection._pong = MagicMock()

    omm_stream_connection._on_ready = MagicMock()

    message = {
        "ID": 5,
        "Text": 'f00',
        "Type": "Error"
        }

    omm_stream_connection._process_response_message(message)

    omm_stream_connection._process_error_message.assert_called_once()
    omm_stream_connection._process_error_message(5, message)

    omm_stream_connection._process_login_response_message.assert_not_called()
    omm_stream_connection._process_refresh_message.assert_not_called()
    omm_stream_connection._process_update_message.assert_not_called()
    omm_stream_connection._process_status_message.assert_not_called()
    omm_stream_connection._pong.assert_not_called()


def test_process_response_message_ping():
    ############################################
    #   prepare things
    session = MagicMock()
    session.name = 'foo_logger'
    session._loop = asyncio.get_event_loop()

    config = MagicMock()

    ############################################
    #   test

    omm_stream_connection = rdp.delivery.OMMStreamConnection('foo_thread',
                                                             session,
                                                             'bar_connection',
                                                             config)
    omm_stream_connection._process_login_response_message = MagicMock()
    omm_stream_connection._process_refresh_message = MagicMock()
    omm_stream_connection._process_update_message = MagicMock()
    omm_stream_connection._process_status_message = MagicMock()
    omm_stream_connection._process_error_message = MagicMock()
    omm_stream_connection._pong = MagicMock()

    omm_stream_connection._on_ready = MagicMock()

    message = {
        "ID": 6,
        "Type": "Ping"
        }

    omm_stream_connection._process_response_message(message)

    omm_stream_connection._pong.assert_called_once()
    omm_stream_connection._pong(6, message)

    omm_stream_connection._process_login_response_message.assert_not_called()
    omm_stream_connection._process_refresh_message.assert_not_called()
    omm_stream_connection._process_update_message.assert_not_called()
    omm_stream_connection._process_status_message.assert_not_called()
    omm_stream_connection._process_error_message.assert_not_called()


def test_process_response_message_unknown():
    ############################################
    #   prepare things
    session = MagicMock()
    session.name = 'foo_logger'
    session._loop = asyncio.get_event_loop()

    config = MagicMock()

    ############################################
    #   test

    omm_stream_connection = rdp.delivery.OMMStreamConnection('foo_thread',
                                                             session,
                                                             'bar_connection',
                                                             config)
    omm_stream_connection._process_login_response_message = MagicMock()
    omm_stream_connection._process_refresh_message = MagicMock()
    omm_stream_connection._process_update_message = MagicMock()
    omm_stream_connection._process_status_message = MagicMock()
    omm_stream_connection._process_error_message = MagicMock()
    omm_stream_connection._pong = MagicMock()

    omm_stream_connection._on_ready = MagicMock()

    message = {
        "ID": 6,
        "Type": "foo"
        }

    omm_stream_connection._process_response_message(message)

    omm_stream_connection._process_login_response_message.assert_not_called()
    omm_stream_connection._process_refresh_message.assert_not_called()
    omm_stream_connection._process_update_message.assert_not_called()
    omm_stream_connection._process_status_message.assert_not_called()
    omm_stream_connection._process_error_message.assert_not_called()
    omm_stream_connection._pong.assert_not_called()

# @pytest.mark.asyncio
# async def test_wait_and_process_close_response_message():

#     ############################################
#     #   prepare things
#     session = MagicMock()
#     session.name = 'foo_logger'
#     session._loop = asyncio.get_event_loop()

#     config = MagicMock()

#     ############################################
#     #   test

#     omm_stream_connection = rdp.delivery.OMMStreamConnection('foo_thread',
#                                                                 session,
#                                                                 'bar_connection',
#                                                                 config)
#     omm_stream_connection._login_response_future = None
#     omm_stream_connection.send = MagicMock()

#     assert await omm_stream_connection._wait_and_process_close_response_message()
