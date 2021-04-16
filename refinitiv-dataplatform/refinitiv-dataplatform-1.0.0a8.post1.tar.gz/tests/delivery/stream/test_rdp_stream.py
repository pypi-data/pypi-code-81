# coding: utf-8

###############################################################
#
#   STANDARD IMPORTS
#

import pytest

from unittest.mock import MagicMock

import asyncio

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

def test_with_api():
    ############################################
    #   prepare things
    session = MagicMock()

    ############################################
    #   test
    rdp_stream = rdp.RDPStream(session, api='foo')

    assert rdp_stream.api == 'foo'

def test_access_properties():

    ############################################
    #   prepare things
    session = MagicMock()

    ############################################
    #   test
    rdp_stream = rdp.RDPStream(session, api='abcde')

    rdp_stream._service = 'foo'
    rdp_stream._universe = ['bar']
    rdp_stream._views = 'abc'
    rdp_stream._parameters = {'xyz':1}

    assert rdp_stream.service == 'foo'
    assert rdp_stream.universe == ['bar']
    assert rdp_stream.views == 'abc'
    assert rdp_stream.parameters == {'xyz':1}

def test_set_properties():

    ############################################
    #   prepare things
    session = MagicMock()

    ############################################
    #   test
    rdp_stream = rdp.RDPStream(session, api='abcde')

    rdp_stream.service = 'foo'
    rdp_stream.universe = ['bar']
    rdp_stream.views = 'abc'
    rdp_stream.parameters = {'xyz':1}

    assert rdp_stream.service == 'foo'
    assert rdp_stream.universe == ['bar']
    assert rdp_stream.views == 'abc'
    assert rdp_stream.parameters == {'xyz':1}

def test_get_subscription_request_message():
    ############################################
    #   prepare things
    session = MagicMock()

    ############################################
    #   test
    rdp_stream = rdp.RDPStream(session, api='abcde')

    rdp_stream._stream_id = 1
    rdp_stream.service = 'foo'
    rdp_stream.universe = ['bar']
    rdp_stream.views = 'abc'
    rdp_stream.parameters = {'xyz':1}

    subscription_request_message = rdp_stream._get_subscription_request_message()
    assert subscription_request_message['streamID'] == f'{rdp_stream._stream_id}'
    assert subscription_request_message['method'] == 'Subscribe'
    assert subscription_request_message['universe'] == rdp_stream.universe
    assert subscription_request_message['service'] == rdp_stream.service
    assert subscription_request_message['views'] == rdp_stream.views
    assert subscription_request_message['parameters'] == rdp_stream.parameters

def test_get_subscription_request_message_tds():
    ############################################
    #   prepare things
    session = MagicMock()

    ############################################
    #   test
    rdp_stream = rdp.RDPStream(session, api='abcde')

    rdp_stream._stream_id = 1
    rdp_stream.universe = ['bar']
    rdp_stream.parameters = {'xyz':1}

    subscription_request_message = rdp_stream._get_subscription_request_message()
    assert subscription_request_message['streamID'] == f'{rdp_stream._stream_id}'
    assert subscription_request_message['method'] == 'Subscribe'
    assert subscription_request_message['universe'] == rdp_stream.universe
    assert subscription_request_message['parameters'] == rdp_stream.parameters

    assert 'service' not in subscription_request_message
    assert 'views' not in subscription_request_message


def test_get_subscription_request_message_elektron():
    ############################################
    #   prepare things
    session = MagicMock()

    ############################################
    #   test
    rdp_stream = rdp.RDPStream(session, api='abcde')

    rdp_stream._stream_id = 1
    rdp_stream.service = 'elektron/market-price'
    rdp_stream.universe = ['bar']

    subscription_request_message = rdp_stream._get_subscription_request_message()
    assert subscription_request_message['streamID'] == f'{rdp_stream._stream_id}'
    assert subscription_request_message['method'] == 'Subscribe'
    assert subscription_request_message['service'] == rdp_stream.service
    assert subscription_request_message['universe'] == rdp_stream.universe

    assert 'parameters' not in subscription_request_message
    assert 'views' not in subscription_request_message

################################################
#    callback functions

def test_on_status():
    ############################################
    #   prepare things
    session = MagicMock()

    ############################################
    #   test
    rdp_stream = rdp.RDPStream(session, api='abcde')

    rdp_stream._stream_id = 1

    rdp_stream._on_status({'status':'foo'})


def test_on_ack():
    ############################################
    #   prepare things
    session = MagicMock()

    ############################################
    #   test
    rdp_stream = rdp.RDPStream(session, api='abcde')

    rdp_stream._on_status( {
                                "streamID": "44", 
                                "type": "Ack", 
                                "state": {
                                "code": 200, 
                                "text": "item updated"
                                }
                            }
                        )

def test_on_response_from_pending_state():
    ############################################
    #   prepare things
    session = MagicMock()

    ############################################
    #   test
    rdp_stream = rdp.RDPStream(session, api='abcde')
    rdp_stream._subscribe_response_future = asyncio.get_event_loop().create_future()
    rdp_stream._state = rdp.delivery.StreamState.Closed

    rdp_stream._on_response( {
                                "streamID": "42", 
                                "type": "Response", 
                                "data": [
                                [
                                    "ReceivedLeg[Curr:'EUR' Type:'Float']", 
                                    "2019-01-18T00:00:00Z", 
                                    "2017-07-28T00:00:00Z", 
                                    "2020-07-28T00:00:00Z", 
                                    "EMU", 
                                    None, 
                                    -150.458065320113, 
                                    0.0273972602739726, 
                                    0.0261199520780213, 
                                    "Swap vs 6M Euribor", 
                                    "Swap vs 6M Euribor", 
                                    ""
                                ]
                                ]
                            } 
                        )

    assert rdp_stream._subscribe_response_future.done()
    assert rdp_stream._state == rdp.delivery.StreamState.Open

def test_on_response_from_closed_state():
    ############################################
    #   prepare things
    session = MagicMock()

    ############################################
    #   test
    rdp_stream = rdp.RDPStream(session, api='abcde')
    rdp_stream._subscribe_response_future = asyncio.get_event_loop().create_future()
    rdp_stream._state = rdp.delivery.StreamState.Closed

    rdp_stream._on_response( {
                                "streamID": "42", 
                                "type": "Response", 
                                "data": [
                                [
                                    "ReceivedLeg[Curr:'EUR' Type:'Float']", 
                                    "2019-01-18T00:00:00Z", 
                                    "2017-07-28T00:00:00Z", 
                                    "2020-07-28T00:00:00Z", 
                                    "EMU", 
                                    None, 
                                    -150.458065320113, 
                                    0.0273972602739726, 
                                    0.0261199520780213, 
                                    "Swap vs 6M Euribor", 
                                    "Swap vs 6M Euribor", 
                                    ""
                                ]
                                ]
                            } 
                        )

    assert rdp_stream._subscribe_response_future.done()
    assert rdp_stream._state == rdp.delivery.StreamState.Open
    
    
def test_on_update():
    ############################################
    #   prepare things
    session = MagicMock()

    ############################################
    #   test
    rdp_stream = rdp.RDPStream(session, api='abcde')

    rdp_stream._on_update( {
                            "streamID": "43", 
                            "type": "Update", 
                            "fields": {
                            "ASK": 401.54, 
                            "ASKSIZE": 10, 
                            "ASKXID": "NAS", 
                            "ASK_MMID1": "NAS", 
                            "BID": 401.5, 
                            "BIDSIZE": 18, 
                            "BIDXID": "NAS", 
                            "BID_MMID1": "NAS", 
                            "BID_NET_CH": 3.49, 
                            "BID_TICK_1": "þ", 
                            "GV1_TEXT": "-", 
                            "QUOTIM": "14:40:32:000:000:000", 
                            "QUOTIM_MS": 52832000
                            }, 
                            "name": "TRI.N", 
                            "updateType": "Quote"
                        }
                    )

def test_on_alarm():

    ############################################
    #   prepare things
    session = MagicMock()

    ############################################
    #   test
    rdp_stream = rdp.RDPStream(session, api='abcde')

    rdp_stream._on_alarm( {
                            "streamID": "", 
                            "type": "Alarm", 
                            "data": [
                                {
                                    "context": "alert/ric", 
                                    "message": "latest BID price was higher than throttle for 5 times", 
                                    "date": "2020-02-21Z10:22:21Z-5", 
                                    "ric": "EUR=", 
                                    "BID": 1.222, 
                                    "throttle": 1.2
                                }
                                ]
                            }
                        )