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

def test__register_stream_case_1_stream_is_None():
    ############################################
    #   prepare things

    mock_stream = None

    ############################################
    #   test

    #   using desktop session for testing the abstract parent session 
    session = rdp.DesktopSession(app_key='foo')

    #   register stream
    with pytest.raises(rdp.errors.SessionError) as execinfo: 
        session._register_stream(mock_stream)
    
    assert 'Try to register None subscription' in str(execinfo.value)

def test__register_stream_case_2_stream_api_is_None():
    ############################################
    #   prepare things

    mock_stream = MagicMock()
    mock_stream.stream_id = 1
    mock_stream.api = None

    ############################################
    #   test

    #   using desktop session for testing the abstract parent session 
    session = rdp.DesktopSession(app_key='foo')
    
    #   register stream
    with pytest.raises(rdp.errors.SessionError) as execinfo: 
        session._register_stream(mock_stream)

    assert 'Try to register but given stream[1] has api property is None.' in str(execinfo.value)


def test__register_stream_case_3_stream_id_already_exists():
    ############################################
    #   prepare things

    mock_stream = MagicMock()
    mock_stream.stream_id = 1
    mock_stream.api = 'bar'

    ############################################
    #   test

    #   using desktop session for testing the abstract parent session 
    session = rdp.DesktopSession(app_key='foo')
    
    #   register stream
    session._register_stream(mock_stream)

    #   try to register with the same stream id
    with pytest.raises(rdp.errors.SessionError) as execinfo: 
        session._register_stream(mock_stream)

    assert 'Subscription 1 is already registered' in str(execinfo.value)
    
def test__register_stream_case_4_stream_id_is_None():
    ############################################
    #   prepare things

    mock_stream = MagicMock()
    mock_stream.stream_id = None
    mock_stream.api = 'bar'

    ############################################
    #   test

    #   using desktop session for testing the abstract parent session 
    session = rdp.DesktopSession(app_key='foo')
    
    #   register stream
    session._register_stream(mock_stream)

    assert mock_stream.stream_id == 1
    assert mock_stream.api in session._stream_connection_name_to_stream_ids_dict
    assert mock_stream.stream_id in session._stream_connection_name_to_stream_ids_dict[mock_stream.api]
    
def test__register_stream_case_5_stream_id_is_not_None():
    ############################################
    #   prepare things

    mock_stream = MagicMock()
    mock_stream.stream_id = 112
    mock_stream.api = 'bar'

    ############################################
    #   test

    #   using desktop session for testing the abstract parent session 
    session = rdp.DesktopSession(app_key='foo')
    
    #   register stream
    session._register_stream(mock_stream)

    assert mock_stream.stream_id == 112
    assert mock_stream.api in session._stream_connection_name_to_stream_ids_dict
    assert mock_stream.stream_id in session._stream_connection_name_to_stream_ids_dict[mock_stream.api]
    
def test__register_stream_case_6_multiple_subscribe_with_same_api():
    ############################################
    #   prepare things

    mock_stream_1 = MagicMock()
    mock_stream_1.stream_id = 4321
    mock_stream_1.api = 'bar'

    mock_stream_2 = MagicMock()()
    mock_stream_2.stream_id = None
    mock_stream_2.api = 'bar'

    ############################################
    #   test

    #   using desktop session for testing the abstract parent session 
    session = rdp.DesktopSession(app_key='foo')
    
    #   register streams
    session._register_stream(mock_stream_1)

    assert mock_stream_1.stream_id == 4321

    session._register_stream(mock_stream_2)

    assert mock_stream_2.stream_id == 1
    assert mock_stream_2.api in session._stream_connection_name_to_stream_ids_dict
    assert mock_stream_2.stream_id in session._stream_connection_name_to_stream_ids_dict[mock_stream_2.api]
    
def test__unregister_stream_case_1_stream_is_None():
    ############################################
    #   prepare things

    mock_stream_1 = None

    ############################################
    #   test

    #   using desktop session for testing the abstract parent session 
    session = rdp.DesktopSession(app_key='foo')
    
    #   un-register streams
    with pytest.raises(rdp.errors.SessionError) as execinfo: 
        session._unregister_stream(mock_stream_1)

    assert 'Try to un-register unavailable stream.' in str(execinfo.value)

def test__unregister_stream_case_2_stream_id_is_None():
    ############################################
    #   prepare things

    mock_stream_1 = MagicMock()
    mock_stream_1.stream_id = None
    mock_stream_1.api = 'bar'

    ############################################
    #   test

    #   using desktop session for testing the abstract parent session 
    session = rdp.DesktopSession(app_key='foo')
    
    #   un-register streams
    with pytest.raises(rdp.errors.SessionError) as execinfo: 
        session._unregister_stream(mock_stream_1)

    assert 'Try to un-register unavailable stream.' in str(execinfo.value)


def test__unregister_stream_case_3_stream_id_never_register():
    ############################################
    #   prepare things

    mock_stream_1 = MagicMock()
    mock_stream_1.stream_id = 123
    mock_stream_1.api = 'bar'

    ############################################
    #   test

    #   using desktop session for testing the abstract parent session 
    session = rdp.DesktopSession(app_key='foo')
    
    #   un-register streams
    with pytest.raises(rdp.errors.SessionError) as execinfo: 
        session._unregister_stream(mock_stream_1)

    assert f'Try to un-register unknown stream[{mock_stream_1.stream_id}] from session ' in str(execinfo.value)
    
  
def test__unregister_stream_case_4_stream_api_is_None():
    ############################################
    #   prepare things

    mock_stream_1 = MagicMock()
    mock_stream_1.stream_id = 123
    mock_stream_1.api = 'foo'

    mock_stream_2 = MagicMock()
    mock_stream_2.stream_id = 123
    mock_stream_2.api = None

    ############################################
    #   test

    #   using desktop session for testing the abstract parent session 
    session = rdp.DesktopSession(app_key='foo')
    
    #   register
    session._register_stream(mock_stream_1)

    #   un-register streams
    with pytest.raises(rdp.errors.SessionError) as execinfo: 
        session._unregister_stream(mock_stream_2)

    assert f'Try to un-register but given stream[{mock_stream_1.stream_id}] has api property is None.' in str(execinfo.value)


def test__unregister_stream_case_5_stream_api_is_invalid():
    ############################################
    #   prepare things

    mock_stream_1 = MagicMock()
    mock_stream_1.stream_id = 123
    mock_stream_1.api = 'bar'

    mock_stream_2 = MagicMock()
    mock_stream_2.stream_id = 123
    mock_stream_2.api = 'foo'

    ############################################
    #   test

    #   using desktop session for testing the abstract parent session 
    session = rdp.DesktopSession(app_key='foo')
    
    #   register
    session._register_stream(mock_stream_1)

    #   un-register streams
    with pytest.raises(rdp.errors.SessionError) as execinfo: 
        session._unregister_stream(mock_stream_2)

    assert f'Try to un-register unknown stream api[{mock_stream_2.api}] of stream[{mock_stream_2.stream_id}].' in str(execinfo.value)
    

def test__unregister_stream_case_6_valid():
    ############################################
    #   prepare things

    mock_stream_1 = MagicMock()
    mock_stream_1.stream_id = 123
    mock_stream_1.api = 'bar'

    mock_stream_2 = MagicMock()
    mock_stream_2.stream_id = 1234
    mock_stream_2.api = 'bar'

    ############################################
    #   test

    #   using desktop session for testing the abstract parent session 
    session = rdp.DesktopSession(app_key='foo')
    
    #   register
    session._register_stream(mock_stream_1)
    session._register_stream(mock_stream_2)

    #   un-register streams
    session._unregister_stream(mock_stream_2)

    assert 'bar' in session._stream_connection_name_to_stream_ids_dict
    assert len(session._stream_connection_name_to_stream_ids_dict) == 1
    assert len(session._stream_connection_name_to_stream_ids_dict['bar']) == 1
    assert mock_stream_1.stream_id in session._stream_connection_name_to_stream_ids_dict['bar']
    assert mock_stream_2.stream_id not in session._stream_connection_name_to_stream_ids_dict['bar']

    assert len(session._all_stream_subscriptions) == 1
    assert mock_stream_1.stream_id in session._all_stream_subscriptions
    