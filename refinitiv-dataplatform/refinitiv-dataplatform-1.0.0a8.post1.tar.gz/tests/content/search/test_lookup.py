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
# ###############################################################
# #
# #   REFINITIV IMPORTS
# #
# from unittest.mock import MagicMock
#
# import refinitiv.dataplatform as rdp
# from refinitiv.dataplatform.content.search import Search, Lookup, ViewMetadata, SearchViews
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
# class TestLookupApi(TestCase):
#
#     def setUp(self):
#         #   RDP http server
#         self.rdpServer = mock_http_webserver.RdpHttpServer(
#             rdp_server_address,
#             mock_server_data_filename='mock_server_search_data_set.json'
#         )
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
#     def test_lookup_ok(self):
#         #   setup scenario for this test
#         self.rdpServer.set_scenario('simple_lookup')
#
#         #   construct session
#         on_state = MagicMock()
#         on_event = MagicMock()
#         mock_session = rdp.CoreFactory.create_session(
#             (
#                 rdp.core.PlatformSession.Params().app_key('1112').grant_type(
#                     rdp.GrantPassword(
#                         username='test@test.com',
#                         password='test1234'
#                     )
#                 ).on_state(on_state).on_event(on_event)
#             )
#         )
#         # mock_session.set_log_level( 20 )
#         mock_session.open()
#
#         ###########################################################
#         #   request the lookup apis
#
#         response = Lookup.lookup(
#             session=mock_session,
#             view=SearchViews.Instruments,  # Required parameter
#             scope='RIC',  # Required parameter
#             terms='MSFT.O,AAPL.O,GOOG.O,KBANK.BK',  # Required parameter
#             select='BusinessEntity,DocumentTitle,CUSIP,SEDOL',  # Required parameter
#         )
#
#         #   dataframe
#         dataframe = response.data.df
#         print('{}'.format(dataframe))
#
#         #   validate row
#         self.assertTrue(len(dataframe.index) == 4)
#         self.assertTrue(dataframe.index[0] == 'MSFT.O')
#         self.assertTrue(dataframe.index[1] == 'AAPL.O')
#         self.assertTrue(dataframe.index[2] == 'GOOG.O')
#         self.assertTrue(dataframe.index[3] == 'KBANK.BK')
#
#         import pandas as pd
#         #   validate data in each row
#         #       cusip
#         cusip = dataframe['CUSIP'].values
#         self.assertTrue(cusip[0] == "594918104")
#         self.assertTrue(cusip[1] == "037833100")
#         self.assertTrue(cusip[2] == "02079K107")
#         self.assertTrue(pd.isna(cusip[3]))
#
#         #       sedol
#         sedol = dataframe['SEDOL'].values
#         self.assertTrue(pd.isna(sedol[0]))
#         self.assertTrue(pd.isna(sedol[1]))
#         self.assertTrue(pd.isna(sedol[2]))
#         self.assertTrue(sedol[3] == "6888783")
#
#         #   done close session
#         mock_session.close()
