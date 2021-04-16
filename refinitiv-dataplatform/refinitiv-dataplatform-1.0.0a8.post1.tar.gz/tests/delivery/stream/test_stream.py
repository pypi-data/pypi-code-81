# coding: utf-8

# import time
# from unittest import TestCase
# from threading import Thread
# from unittest.mock import MagicMock
#
# import refinitiv.dataplatform.delivery.stream.stream_connection
# import websocket_server
#
# local_url = "127.0.0.1"
# local_port = 9001
# edp_amers1 = "ws://amer-1.pricing.streaming.edp.thomsonreuters.com"
# edp_amers1 = "ws://amer-1.pricing.streaming.edp.thomsonreuters.com"
# edp_port = 443
# global_status = None


# class TestStreamConnection(TestCase):
#
#     thread_server = None
#
#     def setUp(self):
#         self.server = websocket_server.mock_websocket_server.SimpleWebSocketServer(local_url, local_port, websocket_server.mock_streaming_websocket.StreamingWebSocket)
#         self.thread_server = Thread(target=self.server.serveforever)
#         self.thread_server.start()
#
#     def tearDown(self):
#         self.server.close()
#
#     def test_streaming_ok(self):
#         self.server.set_scenario("happy_path")
#         on_state = MagicMock()
#         on_event = MagicMock()
#         mock_session = refinitiv.dataplatform.CoreFactory.create_session((refinitiv.dataplatform.core.PlatformSession.Params().app_key("234")
#                                                             .deployed_platform_host("127.0.0.1:9001")
#                                                             .on_state(on_state)
#                                                             .on_event(on_event)))
#         mock_session.set_log_level(1)
#         mock_session.open()
#         print("Session is opened")
#         on_state.assert_called_once()
#
#         on_refresh = MagicMock()
#         on_update = MagicMock()
#         on_status = MagicMock()
#
#         item_stream = refinitiv.dataplatform.DeliveryFactory.create_stream(refinitiv.dataplatform.delivery.OMMItemStream.Params()
#                                                              .session(mock_session)
#                                                              .name("EUR=")
#                                                              .with_service("IDN_RDF")
#                                                              .with_domain("MarketByPrice")
#                                                              .on_refresh(on_refresh)
#                                                              .on_update(on_update)
#                                                              .on_status(on_status))
#         item_stream.open()
#         on_refresh.assert_called_once()
#         time.sleep(10)
#         on_update.assert_called()
#         item_stream.close()
#         mock_session.close()
#
#     def test_streaming_wrong_item(self):
#         self.server.set_scenario("wrong_item")
#         on_state = MagicMock()
#         on_event = MagicMock()
#         mock_session = refinitiv.dataplatform.CoreFactory.create_session((refinitiv.dataplatform.core.DeployedPlatformSession.Params().app_key("234")
#                                                             .deployed_platform_host("127.0.0.1:9001")
#                                                             .on_state(on_state)
#                                                             .on_event(on_event)))
#         # mock_session.streaming_url = "localhost:9001"
#         mock_session.set_log_level(1)
#         mock_session.open()
#         print("Session is opened")
#         on_state.assert_called_once()
#
#         on_refresh = MagicMock()
#         on_update = MagicMock()
#         on_status = MagicMock()
#         on_complete = MagicMock()
#
#         item_stream = refinitiv.dataplatform.DeliveryFactory.create_stream(refinitiv.dataplatform.delivery.OMMItemStream.Params()
#                                                              .session(mock_session)
#                                                              .name("UNKNOWN_ITEM")
#                                                              .with_service("IDN_RDF")
#                                                              .with_domain("MarketPrice")
#                                                              .on_refresh(on_refresh)
#                                                              .on_update(on_update)
#                                                              .on_status(on_status)
#                                                              .on_complete(on_complete))
#         item_stream.open()
#         time.sleep(10)
#         on_complete.assert_called_once()
#         on_status.assert_called_once()
#         item_stream.close()
#         mock_session.close()
#
#
#     def test_streaming_snapshot_item(self):
#         self.server.set_scenario("wrong_item")
#         on_state = MagicMock()
#         on_event = MagicMock()
#         mock_session = refinitiv.dataplatform.CoreFactory.create_session((refinitiv.dataplatform.core.DeployedPlatformSession.Params().app_key("234")
#                                                             .deployed_platform_host("127.0.0.1:9001")
#                                                             .on_state(on_state)
#                                                             .on_event(on_event)))
#         # mock_session.streaming_url = "localhost:9001"
#         mock_session.set_log_level(1)
#         mock_session.open()
#         print("Session is opened")
#         on_state.assert_called_once()
#
#         on_refresh = MagicMock()
#         on_update = MagicMock()
#         on_complete = MagicMock()
#
#         def on_status(stream, status):
#             global global_status
#             global_status = status
#
#         item_stream = refinitiv.dataplatform.DeliveryFactory.create_stream(refinitiv.dataplatform.delivery.OMMItemStream.Params()
#                                                              .session(mock_session)
#                                                              .name("EUR=")
#                                                              .with_service("IDN_RDF")
#                                                              .with_domain("MarketPrice")
#                                                              .on_refresh(on_refresh)
#                                                              .on_update(on_update)
#                                                              .on_status(on_status)
#                                                              .on_complete(on_complete))
#         item_stream.open()
#         time.sleep(10)
#         on_complete.assert_called_once()
#         on_status.assert_called_once()
#         item_stream.close()
#         mock_session.close()
