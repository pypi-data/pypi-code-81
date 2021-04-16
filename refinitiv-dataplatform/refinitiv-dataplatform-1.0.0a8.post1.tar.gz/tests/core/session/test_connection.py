# coding: utf-8

###############################################################
#
#   STANDARD IMPORTS
#

import pytest

from unittest.mock import MagicMock, patch

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

def test_RefinitivDataConnection_get_omm_login_message_key_data():
    ############################################
    #   prepare things

    session = MagicMock()
    session._access_token = 'foo'
    session._dacs_params.dacs_application_id = '1234'
    session._dacs_params.dacs_position = 'abcd1234'

    rdp.core.connection.RefinitivDataConnection.__init__ = lambda *args: None

    ############################################
    #   test

    connection = rdp.core.connection.RefinitivDataConnection(session)
    connection._session = session

    message_data = connection.get_omm_login_message_key_data()

    assert isinstance(message_data, dict)
    assert 'NameType' in message_data
    assert message_data['NameType'] == 'AuthnToken'

    assert 'Elements' in message_data
    elements = message_data['Elements']
    assert isinstance(elements, dict)
    
    assert 'AuthenticationToken' in elements
    assert elements['AuthenticationToken'] == 'foo'

    assert 'ApplicationId' in elements
    assert elements['ApplicationId'] == '1234'

    assert 'Position' in elements
    assert elements['Position'] == 'abcd1234'


def test_DeployedConnection_get_omm_login_message_key_data():
    ############################################
    #   prepare things

    session = MagicMock()
    session._dacs_params.deployed_platform_username = 'foo'
    session._dacs_params.dacs_application_id = '1234'
    session._dacs_params.dacs_position = 'abcd1234'

    rdp.core.connection.DeployedConnection.__init__ = lambda *args: None

    ############################################
    #   test

    connection = rdp.core.connection.DeployedConnection(session)
    connection._session = session

    message_data = connection.get_omm_login_message_key_data()

    assert isinstance(message_data, dict)
    assert 'Name' in message_data
    assert message_data['Name'] == 'foo'

    assert 'Elements' in message_data
    elements = message_data['Elements']
    assert isinstance(elements, dict)

    assert 'ApplicationId' in elements
    assert elements['ApplicationId'] == '1234'

    assert 'Position' in elements
    assert elements['Position'] == 'abcd1234'

def test_RefinitivDataAndDeployedConnection_get_omm_login_message_key_data():
    ############################################
    #   prepare things

    session = MagicMock()
    session._dacs_params.deployed_platform_username = 'foo'
    session._dacs_params.dacs_application_id = '1234'
    session._dacs_params.dacs_position = 'abcd1234'

    rdp.core.connection.RefinitivDataAndDeployedConnection.__init__ = lambda *args: None

    ############################################
    #   test

    connection = rdp.core.connection.RefinitivDataAndDeployedConnection(session)
    connection._session = session

    message_data = connection.get_omm_login_message_key_data()

    assert isinstance(message_data, dict)
    assert 'Name' in message_data
    assert message_data['Name'] == 'foo'

    assert 'Elements' in message_data
    elements = message_data['Elements']
    assert isinstance(elements, dict)

    assert 'ApplicationId' in elements
    assert elements['ApplicationId'] == '1234'

    assert 'Position' in elements
    assert elements['Position'] == 'abcd1234'


@pytest.mark.asyncio
async def test_RefinitivDataConnection_get_stream_connection_configuration_case_1_discovery_endpoint_with_path():
    ############################################
    #   prepare things

    session = MagicMock()
    streaming_connection_endpoint_websocket_url = None
    streaming_connection_discovery_endpoint_url = 'https://api.ppe.refinitiv.com/streaming/pricing/v1/'
    streaming_connection_supported_protocols = ['RDP']

    session.get_streaming_websocket_endpoint_url = lambda *args: streaming_connection_endpoint_websocket_url
    session.get_streaming_discovery_endpoint_url = lambda *args: streaming_connection_discovery_endpoint_url
    session.get_streaming_protocols = lambda *args: streaming_connection_supported_protocols

    rdp.core.connection.RefinitivDataConnection.__init__ = lambda *args: None
    async def mock_get_stream_service_information(*args, **kwargs):
        return [rdp.core._StreamServiceInformation(scheme='wss', host='foo', port=1234, path='hello/world', 
                                                    data_formats=['rdp_streaming'], location=['bar']), ]

    rdp.core._PlatformStreamServiceDiscoveryHandler.get_stream_service_information = lambda *args, **kwargs: mock_get_stream_service_information(*args, **kwargs)
    
    
    ############################################
    #   test

    connection = rdp.core.connection.RefinitivDataConnection(session)
    connection._session = session

    stream_connection_configuration = await connection.get_stream_connection_configuration('foo')
    
    assert isinstance(stream_connection_configuration, rdp.core._RealtimeDistributionSystemConnectionConfiguration)
    assert stream_connection_configuration.url == 'wss://foo:1234/hello/world'
    assert stream_connection_configuration.url_scheme == 'wss'
    assert stream_connection_configuration.urls == ['wss://foo:1234/hello/world']
    assert stream_connection_configuration.headers == []
    assert stream_connection_configuration.data_formats == ['rdp_streaming']
    assert stream_connection_configuration.supported_protocols == ['RDP']

@pytest.mark.asyncio
async def test_RefinitivDataConnection_get_stream_connection_configuration_case_2_discovery_endpoint_with_path():
    ############################################
    #   prepare things

    session = MagicMock()
    streaming_connection_endpoint_websocket_url = None
    streaming_connection_discovery_endpoint_url = 'https://api.ppe.refinitiv.com/streaming/pricing/v1/'
    streaming_connection_supported_protocols = ['RDP']

    session.get_streaming_websocket_endpoint_url = lambda *args: streaming_connection_endpoint_websocket_url
    session.get_streaming_discovery_endpoint_url = lambda *args: streaming_connection_discovery_endpoint_url
    session.get_streaming_protocols = lambda *args: streaming_connection_supported_protocols

    rdp.core.connection.RefinitivDataConnection.__init__ = lambda *args: None
    async def mock_get_stream_service_information(*args, **kwargs):
        return [rdp.core._StreamServiceInformation(scheme='wss', host='foo', port=1234, path='hello/world', 
                                                    data_formats=['rdp_streaming'], location=['bar']),
                rdp.core._StreamServiceInformation(scheme='ws', host='bar', port=5678, path='abc/def', 
                                                    data_formats=['rdp_streaming'], location=['foo']), ]

    rdp.core._PlatformStreamServiceDiscoveryHandler.get_stream_service_information = lambda *args, **kwargs: mock_get_stream_service_information(*args, **kwargs)
    
    
    ############################################
    #   test

    connection = rdp.core.connection.RefinitivDataConnection(session)
    connection._session = session

    stream_connection_configuration = await connection.get_stream_connection_configuration('foo')
    
    assert isinstance(stream_connection_configuration, rdp.core._RealtimeDistributionSystemConnectionConfiguration)
    assert stream_connection_configuration.url == 'wss://foo:1234/hello/world'
    assert stream_connection_configuration.url_scheme == 'wss'
    assert stream_connection_configuration.urls == ['wss://foo:1234/hello/world', 'ws://bar:5678/abc/def']
    assert stream_connection_configuration.headers == []
    assert stream_connection_configuration.data_formats == ['rdp_streaming']
    assert stream_connection_configuration.supported_protocols == ['RDP']


@pytest.mark.asyncio
async def test_RefinitivDataConnection_get_stream_connection_configuration_case_3_discovery_endpoint_without_path():
    ############################################
    #   prepare things

    session = MagicMock()
    streaming_connection_endpoint_websocket_url = None
    streaming_connection_discovery_endpoint_url = 'https://api.ppe.refinitiv.com/streaming/pricing/v1/'
    streaming_connection_supported_protocols = ['RDP']

    session.get_streaming_websocket_endpoint_url = lambda *args: streaming_connection_endpoint_websocket_url
    session.get_streaming_discovery_endpoint_url = lambda *args: streaming_connection_discovery_endpoint_url
    session.get_streaming_protocols = lambda *args: streaming_connection_supported_protocols

    rdp.core.connection.RefinitivDataConnection.__init__ = lambda *args: None
    async def mock_get_stream_service_information(*args, **kwargs):
        return [rdp.core._StreamServiceInformation(scheme='wss', host='foo', port=1234, path=None, 
                                                    data_formats=['rdp_streaming'], location=['bar']),
                rdp.core._StreamServiceInformation(scheme='ws', host='bar', port=5678, path='abc/def', 
                                                    data_formats=['rdp_streaming'], location=['foo']), ]

    rdp.core._PlatformStreamServiceDiscoveryHandler.get_stream_service_information = lambda *args, **kwargs: mock_get_stream_service_information(*args, **kwargs)
    
    
    ############################################
    #   test

    connection = rdp.core.connection.RefinitivDataConnection(session)
    connection._session = session

    stream_connection_configuration = await connection.get_stream_connection_configuration('foo')
    
    assert isinstance(stream_connection_configuration, rdp.core._RealtimeDistributionSystemConnectionConfiguration)
    assert stream_connection_configuration.url == 'wss://foo:1234/WebSocket'
    assert stream_connection_configuration.url_scheme == 'wss'
    assert stream_connection_configuration.urls == ['wss://foo:1234/WebSocket', 'ws://bar:5678/abc/def']
    assert stream_connection_configuration.headers == []
    assert stream_connection_configuration.data_formats == ['rdp_streaming']
    assert stream_connection_configuration.supported_protocols == ['RDP']

@pytest.mark.asyncio
async def test_RefinitivDataConnection_get_stream_connection_configuration_case_5_direct_websocket_endpoint_without_path():
    ############################################
    #   prepare things

    session = MagicMock()
    streaming_connection_endpoint_websocket_url = 'ws://127.0.0.1:23456'
    streaming_connection_discovery_endpoint_url = None
    streaming_connection_supported_protocols = ['OMM', 'RDP']

    session.get_streaming_websocket_endpoint_url = lambda *args: streaming_connection_endpoint_websocket_url
    session.get_streaming_discovery_endpoint_url = lambda *args: streaming_connection_discovery_endpoint_url
    session.get_streaming_protocols = lambda *args: streaming_connection_supported_protocols

    rdp.core.connection.RefinitivDataConnection.__init__ = lambda *args: None
    async def mock_get_stream_service_information(*args, **kwargs):
        assert False
    rdp.core._PlatformStreamServiceDiscoveryHandler.get_stream_service_information = lambda *args, **kwargs: mock_get_stream_service_information(*args, **kwargs)
    
    
    ############################################
    #   test

    connection = rdp.core.connection.RefinitivDataConnection(session)
    connection._session = session

    stream_connection_configuration = await connection.get_stream_connection_configuration('foo')
    
    assert isinstance(stream_connection_configuration, rdp.core._RealtimeDistributionSystemConnectionConfiguration)
    assert stream_connection_configuration.url == 'ws://127.0.0.1:23456/WebSocket'
    assert stream_connection_configuration.url_scheme == 'ws'
    assert stream_connection_configuration.urls == ['ws://127.0.0.1:23456/WebSocket',]
    assert stream_connection_configuration.headers == []
    assert stream_connection_configuration.data_formats == ['unknown']
    assert len(stream_connection_configuration.supported_protocols) == 2
    assert 'OMM' in stream_connection_configuration.supported_protocols
    assert 'RDP' in stream_connection_configuration.supported_protocols


@pytest.mark.asyncio
async def test_RefinitivDataConnection_get_stream_connection_configuration_case_5_direct_websocket_endpoint_with_path():
    ############################################
    #   prepare things

    session = MagicMock()
    streaming_connection_endpoint_websocket_url = 'ws://127.0.0.1:23456/foo/bar'
    streaming_connection_discovery_endpoint_url = None
    streaming_connection_supported_protocols = ['OMM']

    session.get_streaming_websocket_endpoint_url = lambda *args: streaming_connection_endpoint_websocket_url
    session.get_streaming_discovery_endpoint_url = lambda *args: streaming_connection_discovery_endpoint_url
    session.get_streaming_protocols = lambda *args: streaming_connection_supported_protocols

    rdp.core.connection.RefinitivDataConnection.__init__ = lambda *args: None
    async def mock_get_stream_service_information(*args, **kwargs):
        assert False
    rdp.core._PlatformStreamServiceDiscoveryHandler.get_stream_service_information = lambda *args, **kwargs: mock_get_stream_service_information(*args, **kwargs)
    
    
    ############################################
    #   test

    connection = rdp.core.connection.RefinitivDataConnection(session)
    connection._session = session

    stream_connection_configuration = await connection.get_stream_connection_configuration('foo')
    
    assert isinstance(stream_connection_configuration, rdp.core._RealtimeDistributionSystemConnectionConfiguration)
    assert stream_connection_configuration.url == 'ws://127.0.0.1:23456/foo/bar'
    assert stream_connection_configuration.url_scheme == 'ws'
    assert stream_connection_configuration.urls == ['ws://127.0.0.1:23456/foo/bar',]
    assert stream_connection_configuration.headers == []
    assert stream_connection_configuration.data_formats == ['unknown']
    assert len(stream_connection_configuration.supported_protocols) == 1
    assert 'OMM' in stream_connection_configuration.supported_protocols


@pytest.mark.asyncio
async def test_RefinitivDataConnection_get_stream_connection_configuration_case_5_direct_websocket_endpoint_with_path():
    ############################################
    #   prepare things

    session = MagicMock()
    streaming_connection_endpoint_websocket_url = None
    streaming_connection_discovery_endpoint_url = None
    streaming_connection_supported_protocols = ['OMM']

    session.get_streaming_websocket_endpoint_url = lambda *args: streaming_connection_endpoint_websocket_url
    session.get_streaming_discovery_endpoint_url = lambda *args: streaming_connection_discovery_endpoint_url
    session.get_streaming_protocols = lambda *args: streaming_connection_supported_protocols

    rdp.core.connection.RefinitivDataConnection.__init__ = lambda *args: None
    async def mock_get_stream_service_information(*args, **kwargs):
        assert False
    rdp.core._PlatformStreamServiceDiscoveryHandler.get_stream_service_information = lambda *args, **kwargs: mock_get_stream_service_information(*args, **kwargs)
    
    
    ############################################
    #   test


    connection = rdp.core.connection.RefinitivDataConnection(session)
    connection._session = session

    with pytest.raises(ValueError) as execinfo: 
        stream_connection_configuration = await connection.get_stream_connection_configuration('streaming/pricing/foo')
    
    assert 'ERROR!!! streaming connection needed by specific url and path in endpoint section or specific WebSocket url.' == str(execinfo.value)


@pytest.mark.asyncio
async def test_DeployedConnection_get_stream_connection_configuration_case_1_session_has_deployed_host():
    ############################################
    #   prepare things

    session = MagicMock()
    session._deployed_platform_host = 'localhost:12345'
    
    ############################################
    #   test

    connection = rdp.core.connection.DeployedConnection(session)
    connection._session = session

    stream_connection_configuration = await connection.get_stream_connection_configuration('streaming/pricing/foo')
    
    assert isinstance(stream_connection_configuration, rdp.core._RealtimeDistributionSystemConnectionConfiguration)
    assert stream_connection_configuration.url == 'ws://localhost:12345/WebSocket'
    assert stream_connection_configuration.url_scheme == 'ws'
    assert stream_connection_configuration.urls == ['ws://localhost:12345/WebSocket',]
    assert stream_connection_configuration.headers == []
    assert stream_connection_configuration.data_formats == ['tr_json2']
    assert len(stream_connection_configuration.supported_protocols) == 1
    assert 'OMM' in stream_connection_configuration.supported_protocols


@pytest.mark.asyncio
async def test_DeployedConnection_get_stream_connection_configuration_case_2_refinitiv_distribution_in_config_file():
    ############################################
    #   prepare things

    session = MagicMock()
    session._deployed_platform_host = None

    from refinitiv.dataplatform import configure
    configure.keys.platform_realtime_distribution_system = lambda *args, **kwargs : None
    configure.get_str = lambda  *args, **kwargs : 'ws://foo.bar:1234'

    ############################################
    #   test

    connection = rdp.core.connection.DeployedConnection(session)
    connection._session = session

    stream_connection_configuration = await connection.get_stream_connection_configuration('streaming/pricing/foo')
    
    assert isinstance(stream_connection_configuration, rdp.core._RealtimeDistributionSystemConnectionConfiguration)
    assert stream_connection_configuration.url == 'ws://foo.bar:1234/WebSocket'
    assert stream_connection_configuration.url_scheme == 'ws'
    assert stream_connection_configuration.urls == ['ws://foo.bar:1234/WebSocket',]
    assert stream_connection_configuration.headers == []
    assert stream_connection_configuration.data_formats == ['tr_json2']
    assert len(stream_connection_configuration.supported_protocols) == 1
    assert 'OMM' in stream_connection_configuration.supported_protocols


@pytest.mark.asyncio
async def test_DeployedConnection_get_stream_connection_configuration_case_3():
    ############################################
    #   prepare things

    session = MagicMock()    
    session._deployed_platform_host = 'localhost:12345'

    from refinitiv.dataplatform import configure
    configure.keys.platform_realtime_distribution_system = lambda *args, **kwargs : None
    configure.get_str = lambda  *args, **kwargs : 'ws://foo.bar:1234'

    ############################################
    #   test

    connection = rdp.core.connection.DeployedConnection(session)
    connection._session = session

    stream_connection_configuration = await connection.get_stream_connection_configuration('streaming/pricing/foo')
    
    assert isinstance(stream_connection_configuration, rdp.core._RealtimeDistributionSystemConnectionConfiguration)
    assert stream_connection_configuration.url == 'ws://localhost:12345/WebSocket'
    assert stream_connection_configuration.url_scheme == 'ws'
    assert stream_connection_configuration.urls == ['ws://localhost:12345/WebSocket',]
    assert stream_connection_configuration.headers == []
    assert stream_connection_configuration.data_formats == ['tr_json2']
    assert len(stream_connection_configuration.supported_protocols) == 1
    assert 'OMM' in stream_connection_configuration.supported_protocols


@pytest.mark.asyncio
async def test_RefinitivDataAndDeployedConnection_get_stream_connection_configuration_case_1():
    ############################################
    #   prepare things

    session = MagicMock()
    session._deployed_platform_host = None

    from refinitiv.dataplatform import configure
    configure.keys.platform_realtime_distribution_system = lambda *args, **kwargs : None
    configure.get_str = lambda  *args, **kwargs : 'ws://foo.bar:1234'

    ############################################
    #   test

    connection = rdp.core.connection.RefinitivDataAndDeployedConnection(session)
    connection._session = session

    stream_connection_configuration = await connection.get_stream_connection_configuration('streaming/pricing/foo')
    
    assert isinstance(stream_connection_configuration, rdp.core._RealtimeDistributionSystemConnectionConfiguration)
    assert stream_connection_configuration.url == 'ws://foo.bar:1234/WebSocket'
    assert stream_connection_configuration.url_scheme == 'ws'
    assert stream_connection_configuration.urls == ['ws://foo.bar:1234/WebSocket',]
    assert stream_connection_configuration.headers == []
    assert stream_connection_configuration.data_formats == ['tr_json2']
    assert len(stream_connection_configuration.supported_protocols) == 1
    assert 'OMM' in stream_connection_configuration.supported_protocols

@pytest.mark.asyncio
async def test_RefinitivDataAndDeployedConnection_get_stream_connection_configuration_case_1():
    ############################################
    #   prepare things

    session = MagicMock()
    session._deployed_platform_host = None

    streaming_connection_endpoint_websocket_url = None
    streaming_connection_discovery_endpoint_url = 'https://api.ppe.refinitiv.com/streaming/pricing/v1/'
    streaming_connection_supported_protocols = ['RDP']

    from refinitiv.dataplatform import configure
    configure.keys.platform_realtime_distribution_system = lambda *args, **kwargs : None
    configure.get_str = lambda  *args, **kwargs : 'ws://hello.bar:4567'

    session.get_streaming_websocket_endpoint_url = lambda *args: streaming_connection_endpoint_websocket_url
    session.get_streaming_discovery_endpoint_url = lambda *args: streaming_connection_discovery_endpoint_url
    session.get_streaming_protocols = lambda *args: streaming_connection_supported_protocols

    rdp.core.connection.RefinitivDataConnection.__init__ = lambda *args: None
    async def mock_get_stream_service_information(*args, **kwargs):
        return [rdp.core._StreamServiceInformation(scheme='wss', host='foo', port=1234, path='hello/world', 
                                                    data_formats=['rdp_streaming'], location=['bar']), ]

    rdp.core._PlatformStreamServiceDiscoveryHandler.get_stream_service_information = lambda *args, **kwargs: mock_get_stream_service_information(*args, **kwargs)
    
    ############################################
    #   test

    connection = rdp.core.connection.RefinitivDataAndDeployedConnection(session)
    connection._session = session

    stream_connection_configuration = await connection.get_stream_connection_configuration('streaming/trading-analytics/bar')
    
    assert isinstance(stream_connection_configuration, rdp.core._RealtimeDistributionSystemConnectionConfiguration)
    assert stream_connection_configuration.url == 'wss://foo:1234/hello/world'
    assert stream_connection_configuration.url_scheme == 'wss'
    assert stream_connection_configuration.urls == ['wss://foo:1234/hello/world',]
    assert stream_connection_configuration.headers == []
    assert stream_connection_configuration.data_formats == ['rdp_streaming']
    assert len(stream_connection_configuration.supported_protocols) == 1
    assert 'RDP' in stream_connection_configuration.supported_protocols