# # coding: utf-8
#
# ###############################################################
# #
# #   STANDARD IMPORTS
# #
#
#
# ###############################################################
# #
# #   REFINITIV IMPORTS
# #
#
# from refinitiv.dataplatform.delivery.stream.streaming_connection_config import StreamingConnectionConfiguration
#
#
# ###############################################################
# #
# #   LOCAL IMPORTS
# #
#
# ###############################################################
# #
# #   TEST CASES
# #
#
#
# def test_constuct_streaming_connnection_config():
#     #  construct config obj
#     streaming_connection_config = StreamingConnectionConfiguration()
#
#     #   config
#     assert (streaming_connection_config is not None)
#
#
# def test_streaming_connnection_config_attribute_getter():
#     #  construct config obj
#     streaming_connection_config = StreamingConnectionConfiguration()
#
#     #   config
#     assert (streaming_connection_config is not None)
#
#     ###############################################################
#     #   getter
#
#     #   uri
#     assert (streaming_connection_config.uri is not None)
#     assert (isinstance(streaming_connection_config.uri, str))
#     assert (streaming_connection_config.uri.startswith('ws://')
#             or streaming_connection_config.uri.startswith('wss://'))
#     assert (streaming_connection_config.uri.endswith('/WebSocket'))
#
#     #   uris
#     assert (streaming_connection_config.uris is not None)
#     assert (isinstance(streaming_connection_config.uris, list))
#     for uri in streaming_connection_config.uris:
#         assert (isinstance(uri, str))
#         assert (uri.startswith('ws://')
#                 or uri.startswith('wss://'))
#         assert (uri.endswith('/WebSocket'))
#
#     #   websocket
#     assert (streaming_connection_config.websocket_endpoints is not None)
#     assert (isinstance(streaming_connection_config.websocket_endpoints, list))
#
#     #   secure
#     assert (streaming_connection_config.secure is not None)
#     assert (isinstance(streaming_connection_config.secure, bool))
#
#     #   reconnection_delay_secs
#     assert (streaming_connection_config.reconnection_delay_secs is not None)
#     assert (isinstance(streaming_connection_config.reconnection_delay_secs, int)
#             or isinstance(streaming_connection_config.reconnection_delay_secs, float))
#
#
# def test_streaming_connnection_config_attribute_setter():
#     #  construct config obj
#     streaming_connection_config = StreamingConnectionConfiguration()
#
#     #   config
#     assert (streaming_connection_config is not None)
#
#     ###############################################################
#     #   setter
#
#     ###############################################################
#     #       secure
#
#     #   secure
#     streaming_connection_config.secure = False
#     assert (streaming_connection_config.secure is not None)
#     assert (isinstance(streaming_connection_config.secure, bool))
#
#     #   uri
#     assert (streaming_connection_config.uri is not None)
#     assert (isinstance(streaming_connection_config.uri, str))
#     assert (streaming_connection_config.uri.startswith('ws://'))
#
#     #   uris
#     assert (streaming_connection_config.uris is not None)
#     assert (isinstance(streaming_connection_config.uris, list))
#     for uri in streaming_connection_config.uris:
#         assert (isinstance(uri, str))
#         assert (uri.startswith('ws://'))
#
#     #   secure
#     streaming_connection_config.secure = True
#     assert (streaming_connection_config.secure is not None)
#     assert (isinstance(streaming_connection_config.secure, bool))
#
#     #   uri
#     assert (streaming_connection_config.uri is not None)
#     assert (isinstance(streaming_connection_config.uri, str))
#     assert (streaming_connection_config.uri.startswith('wss://'))
#
#     #   uris
#     assert (streaming_connection_config.uris is not None)
#     assert (isinstance(streaming_connection_config.uris, list))
#     for uri in streaming_connection_config.uris:
#         assert (isinstance(uri, str))
#         assert (uri.startswith('wss://'))
#
#     ###############################################################
#     #       websocket_endpoints
#
#     websocket_endpoints = ['localhost:8000', 'amer1.pricing.refinitiv.com:443', 'amer2.pricing.refinitiv.com:443']
#     #   websocket_endpoints
#     streaming_connection_config.websocket_endpoints = websocket_endpoints
#     assert (streaming_connection_config.websocket_endpoints is not None)
#     assert (isinstance(streaming_connection_config.websocket_endpoints, list))
#
#     #   uri
#     assert (streaming_connection_config.uri is not None)
#     assert (isinstance(streaming_connection_config.uri, str))
#     assert (websocket_endpoints[0] in streaming_connection_config.uri)
#
#     #   uris
#     assert (streaming_connection_config.uris is not None)
#     assert (isinstance(streaming_connection_config.uris, list))
#     for index, uri in enumerate(streaming_connection_config.uris):
#         assert (isinstance(uri, str))
#         assert (websocket_endpoints[index] in uri)
#
#
# def test_streaming_connnection_config_function():
#     #  construct config obj
#     streaming_connection_config = StreamingConnectionConfiguration()
#
#     #   config
#     assert (streaming_connection_config is not None)
#
#     ###############################################################
#     #   set_next_available_websocket_uri
#
#     assert (callable(streaming_connection_config.set_next_available_websocket_uri))
#
#     #   setup
#     websocket_endpoints = ['localhost:8000', 'amer1.pricing.refinitiv.com:443', 'amer2.pricing.refinitiv.com:443']
#     #   websocket_endpoints
#     streaming_connection_config.websocket_endpoints = websocket_endpoints
#
#     #   test
#     assert (websocket_endpoints[0] in streaming_connection_config.uri)
#     delay_secs = streaming_connection_config.reconnection_delay_secs
#     assert (abs(delay_secs) < 1e-12)
#
#     streaming_connection_config.set_next_available_websocket_uri()
#     assert (websocket_endpoints[1] in streaming_connection_config.uri)
#     assert (streaming_connection_config.reconnection_delay_secs == delay_secs)
#
#     streaming_connection_config.set_next_available_websocket_uri()
#     assert (websocket_endpoints[2] in streaming_connection_config.uri)
#     assert (streaming_connection_config.reconnection_delay_secs == delay_secs)
#
#     streaming_connection_config.set_next_available_websocket_uri()
#     assert (websocket_endpoints[0] in streaming_connection_config.uri)
#     assert (streaming_connection_config.reconnection_delay_secs == delay_secs)
#
#     streaming_connection_config.set_next_available_websocket_uri()
#     assert (websocket_endpoints[1] in streaming_connection_config.uri)
#     assert (
#                 streaming_connection_config.reconnection_delay_secs == StreamingConnectionConfiguration.StreamReconnectionConfiguration._DefaultReconnectionDelayTime_secs)
#
#     streaming_connection_config.set_next_available_websocket_uri()
#     assert (websocket_endpoints[2] in streaming_connection_config.uri)
#     assert (streaming_connection_config.reconnection_delay_secs == 0)
#
#     streaming_connection_config.set_next_available_websocket_uri()
#     assert (websocket_endpoints[0] in streaming_connection_config.uri)
#     assert (streaming_connection_config.reconnection_delay_secs == 0)
#
#     streaming_connection_config.set_next_available_websocket_uri()
#     assert (websocket_endpoints[1] in streaming_connection_config.uri)
#     assert (
#                 streaming_connection_config.reconnection_delay_secs == StreamingConnectionConfiguration.StreamReconnectionConfiguration._DefaultReconnectionDelayTime_secs * 2)
#
#     ###############################################################
#     #   reset_reconnection_config
#
#     assert (callable(streaming_connection_config.reset_reconnection_config))
#
#     #   test
#     streaming_connection_config.reset_reconnection_config()
#     assert (abs(streaming_connection_config.reconnection_delay_secs) < 1e-12)
#
#     assert (websocket_endpoints[1] in streaming_connection_config.uri)
#     delay_secs = streaming_connection_config.reconnection_delay_secs
#     assert (abs(delay_secs) < 1e-12)
#
#     streaming_connection_config.set_next_available_websocket_uri()
#     assert (websocket_endpoints[2] in streaming_connection_config.uri)
#     assert (streaming_connection_config.reconnection_delay_secs == delay_secs)
#
#     streaming_connection_config.set_next_available_websocket_uri()
#     assert (websocket_endpoints[0] in streaming_connection_config.uri)
#     assert (streaming_connection_config.reconnection_delay_secs == delay_secs)
#
#     streaming_connection_config.set_next_available_websocket_uri()
#     assert (websocket_endpoints[1] in streaming_connection_config.uri)
#     assert (streaming_connection_config.reconnection_delay_secs == delay_secs)
#
#     streaming_connection_config.set_next_available_websocket_uri()
#     assert (websocket_endpoints[2] in streaming_connection_config.uri)
#     assert (
#                 streaming_connection_config.reconnection_delay_secs == StreamingConnectionConfiguration.StreamReconnectionConfiguration._DefaultReconnectionDelayTime_secs)
#
#     streaming_connection_config.set_next_available_websocket_uri()
#     assert (websocket_endpoints[0] in streaming_connection_config.uri)
#     assert (streaming_connection_config.reconnection_delay_secs == 0)
#
#     streaming_connection_config.set_next_available_websocket_uri()
#     assert (websocket_endpoints[1] in streaming_connection_config.uri)
#     assert (streaming_connection_config.reconnection_delay_secs == 0)
#
#     streaming_connection_config.set_next_available_websocket_uri()
#     assert (websocket_endpoints[2] in streaming_connection_config.uri)
#     assert (
#                 streaming_connection_config.reconnection_delay_secs == StreamingConnectionConfiguration.StreamReconnectionConfiguration._DefaultReconnectionDelayTime_secs * 2)
