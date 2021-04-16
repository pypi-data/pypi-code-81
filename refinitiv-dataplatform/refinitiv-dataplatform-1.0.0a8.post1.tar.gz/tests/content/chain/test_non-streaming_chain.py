# # coding: utf-8
#
# ###############################################################
# #
# #   STANDARD IMPORTS
# #
#
# from threading import Thread
#
# #   unittest
# from unittest import TestCase, mock
#
# from unittest.mock import MagicMock
#
# ###############################################################
# #
# #   REFINITIV IMPORTS
# #
#
# import refinitiv.dataplatform as rdp
#
# ###############################################################
# #
# #   LOCAL IMPORTS
# #
#
# #   RDP HTTP webserver
# import http_server.mock_http_webserver as mock_http_webserver
#
# ###############################################################
# #
# #   GLOBAL VARIABLES
# #
#
# #   local server address
# #       RDP http server
# rdp_server_address = ('127.0.0.1', 10015)
#
#
# ###############################################################
# #
# #   FUNCTIONS
# #
#
# def platform_open(obj):
#     obj._state = rdp.core.Session.State.Open
#
#
# def platform_close(obj):
#     pass
#
#
# def platform_get_rdp_url_root(obj):
#     return u'http://{}:{}'.format(*rdp_server_address)
#
#
# ###############################################################
# #
# #   CLASSES
# #
#
# class TestNonStreamingChainApi(TestCase):
#
#     def setUp(self):
#         #   RDP http server
#         self.rdpServer = mock_http_webserver.RdpHttpServer(rdp_server_address,
#                                                            mock_server_data_filename='mock_server_search_data_set.json')
#         self.rdpThreadServer = Thread(target=self.rdpServer.serve_forever)
#         self.rdpThreadServer.start()
#
#     def tearDown(self):
#         #   close RDP http server
#         self.rdpServer.shutdown()
#         self.rdpServer.server_close()
#         self.rdpThreadServer.join()
#
#     @mock.patch.object(rdp.core.PlatformSession, 'open', platform_open)
#     @mock.patch.object(rdp.core.PlatformSession, 'close', platform_close)
#     @mock.patch.object(rdp.core.PlatformSession, '_get_rdp_url_root', platform_get_rdp_url_root)
#     def test_nonstreaming_chain_ok(self):
#         #   setup scenario for this test
#         self.rdpServer.set_scenario('simple_non-streaming_chain')
#
#         #  construct session
#         on_state = MagicMock()
#         on_event = MagicMock()
#         mock_session = rdp.CoreFactory.create_session((rdp.core.PlatformSession.Params().app_key('1112')
#                                                        .grant_type(rdp.GrantPassword(
#             username='test@test.com',
#             password='test1234'))
#                                                        .on_state(on_state)
#                                                        .on_event(on_event)))
#
#         # mock_session.set_log_level(logging.DEBUG)
#         mock_session.open()
#
#         ###########################################################
#         #   request the non-streaming chain apis
#
#         response = rdp.content.Chain.decode(session=mock_session,
#                                             universe='0#.DJI',
#                                             )
#
#         dataframe = response.data.df
#
#         #   validate row
#         self.assertTrue(len(dataframe.index) == 31)
#
#         #   validate values
#         dji = dataframe['0#.DJI'].values
#         self.assertTrue(dji[0] == '.DJI')
#         self.assertTrue(dji[1] == 'AAPL.OQ')
#         self.assertTrue(dji[2] == 'AXP.N')
#         self.assertTrue(dji[3] == 'BA.N')
#         self.assertTrue(dji[4] == 'CAT.N')
#         self.assertTrue(dji[5] == 'CSCO.OQ')
#         self.assertTrue(dji[6] == 'CVX.N')
#         self.assertTrue(dji[7] == 'DIS.N')
#         self.assertTrue(dji[8] == 'DOW.N')
#         self.assertTrue(dji[9] == 'GS.N')
#         self.assertTrue(dji[10] == 'HD.N')
#         self.assertTrue(dji[11] == 'IBM.N')
#         self.assertTrue(dji[12] == 'INTC.OQ')
#         self.assertTrue(dji[13] == 'JNJ.N')
#         self.assertTrue(dji[14] == 'JPM.N')
#         self.assertTrue(dji[15] == 'KO.N')
#         self.assertTrue(dji[16] == 'MCD.N')
#         self.assertTrue(dji[17] == 'MMM.N')
#         self.assertTrue(dji[18] == 'MRK.N')
#         self.assertTrue(dji[19] == 'MSFT.OQ')
#         self.assertTrue(dji[20] == 'NKE.N')
#         self.assertTrue(dji[21] == 'PFE.N')
#         self.assertTrue(dji[22] == 'PG.N')
#         self.assertTrue(dji[23] == 'TRV.N')
#         self.assertTrue(dji[24] == 'UNH.N')
#         self.assertTrue(dji[25] == 'UTX.N')
#         self.assertTrue(dji[26] == 'V.N')
#         self.assertTrue(dji[27] == 'VZ.N')
#         self.assertTrue(dji[28] == 'WBA.OQ')
#         self.assertTrue(dji[29] == 'WMT.N')
#         self.assertTrue(dji[30] == 'XOM.N')
#
#         #   done close session
#         mock_session.close()
