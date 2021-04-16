# coding: utf-8

###############################################################
#
#   STANDARD IMPORTS
#

import http.server
import io
import json
import os.path

###############################################################
#
#   REFINITIV IMPORTS
#


###############################################################
#
#   LOCAL IMPORTS
#

###############################################################
#
#   GLOBAL VARIABLES
#

server_address = ('127.0.0.1', 10015)


###############################################################
#
#   CLASSES
#


class RdpHttpRequestHandler(http.server.BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server):
        http.server.BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def _getMockResponseData(self):
        return self.server.mockScenarioResponseData

    #   override functions
    def do_GET(self):
        """ handle GET request """
        self._handleRequest()
        # print( 'do_GET()' )
        # print( 'header = {}'.format( self.headers ) )
        # print( 'request_line = {}'.format( self.requestline ) )
        # print( 'client_address = {}'.format( self.client_address ) )
        # print( 'path = {}'.format( self.path ) )

    def do_POST(self):
        """ handle POST request """
        self._handleRequest()
        # print( 'do_POST()' )
        # print( 'header = {}'.format( self.headers ) )
        # print( 'request_line = {}'.format( self.requestline ) )
        # print( 'client_address = {}'.format( self.client_address ) )
        # print( 'path = {}'.format( self.path ) )

    def _handleRequest(self):
        """ handle the request by response with mock data """

        #   get response data
        mockReponseData = self._getMockResponseData()
        assert (mockReponseData != None)

        #   response the POST request
        self.send_response(mockReponseData['response_code'])
        #       header
        self.send_header('content-type', '/json')
        self.end_headers()

        #   body
        response = io.BytesIO()
        response.write(bytes(json.dumps(mockReponseData['response_data']), 'utf-8'))
        self.wfile.write(response.getvalue())


class RdpHttpServer(http.server.ThreadingHTTPServer):
    def __init__(self, server_address, mock_server_data_filename, requestHandlerClass=RdpHttpRequestHandler):
        http.server.ThreadingHTTPServer.__init__(self, server_address, requestHandlerClass)

        #   store mock data set file name for server
        self.mockServerDataFileName = mock_server_data_filename

        #   store the response server data and scenario data
        self.mockServerReponseData = None
        self.mockScenarioResponseData = None

        #   initialize server with mock data
        self._initialize(mock_server_data_filename)

    def _initialize(self, mockServerDataFileName):
        """ load the mock data from file """

        #   read mock data from json file and convert to obj
        mockServerDataFileName_abspath = os.path.join(os.path.dirname(__file__), mockServerDataFileName)
        with open(mockServerDataFileName_abspath, 'r') as f:
            self.mockServerReponseData = json.loads(f.read())

    def set_scenario(self, scenario):
        """ set the mock data scenario """
        assert ('request_response' in self.mockServerReponseData[scenario])
        self.mockScenarioResponseData = self.mockServerReponseData[scenario]['request_response']
