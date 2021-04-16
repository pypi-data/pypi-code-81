#     # coding: utf-8
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
#     ###############################################################
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
# import http_server
#
# ###############################################################
# #
# #   GLOBAL VARIABLES
# #
#
# #   local server address
# #       RDP http server
# rdp_server_address = ( '127.0.0.1', 10015 )
#
# ###############################################################
# #
# #   FUNCTIONS
# #
#
# def platform_open(obj):
#     obj._state = rdp.core.Session.State.Open
#
# def platform_close(obj):
#     pass
#
# def platform_get_rdp_url_root(obj):
#     return u'http://{}:{}'.format(*rdp_server_address)
#
# ###############################################################
# #
# #   CLASSES
# #
#
# class TestSearchApi(TestCase):
#
#     def setUp(self):
#
#         #   RDP http server
#         self.rdpServer = http_server.mock_http_webserver.RdpHttpServer( rdp_server_address, mock_server_data_filename = 'mock_server_search_data_set.json' )
#         self.rdpThreadServer = Thread( target=self.rdpServer.serve_forever )
#         self.rdpThreadServer.start()
#
#     def tearDown(self):
#
#         #   close RDP http server
#         self.rdpServer.shutdown()
#         self.rdpServer.server_close()
#         self.rdpThreadServer.join()
#
#     @mock.patch.object(rdp.core.PlatformSession, 'open', platform_open)
#     @mock.patch.object(rdp.core.PlatformSession, 'close', platform_close)
#     @mock.patch.object(rdp.core.PlatformSession, '_get_rdp_url_root', platform_get_rdp_url_root)
#     def test_search_ok(self):
#
#         #   setup scenario for this test
#         self.rdpServer.set_scenario( 'simple_search_people_cto_microsoft' )
#
#
#         #   construct session
#         on_state = MagicMock()
#         on_event = MagicMock()
#         mock_session = rdp.CoreFactory.create_session((rdp.core.PlatformSession.Params().app_key('1112')
#                                                             .grant_type(rdp.GrantPassword(
#                                                                 username='test@test.com',
#                                                                 password='test1234'))
#                                                             .on_state(on_state)
#                                                             .on_event(on_event)))
#         # mock_session.set_log_level( 20 )
#         mock_session.open()
#
#         ###########################################################
#         #   request the search apis
#
#         response = Search.search( session  = mock_session,
#                                     view = SearchViews.People,
#                                     query = 'cto microsoft' )
#
#         #   dataframe
#         dataframe = response.data.df
#         print( '{}'.format( dataframe ) )
#
#         #   validate row
#         self.assertTrue( len( dataframe.index ) == 3 )
#
#         #   validate data in each row
#         #       documentTitile
#         documentTitile = dataframe[ 'DocumentTitle' ].values
#         self.assertTrue( documentTitile[ 0 ] == "Kevin  Scott - Microsoft Corp - Executive Vice President, Chief Technology Officer" )
#         self.assertTrue( documentTitile[ 1 ] == "Ifeanyi  Amah - Microsoft Corp - Ex-Chief Technology Officer" )
#         self.assertTrue( documentTitile[ 2 ] == "Bjorn  Olstad - Microsoft Development Center Norway AS - Ex-Chief Technology Officer" )
#
#         #   done close session
#         mock_session.close()
#