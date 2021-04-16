# coding: utf-8

###############################################################
#
#   STANDARD IMPORTS
#

import argparse

import asyncio

###############################################################
#
#   REFINITIV IMPORTS
#

###############################################################
#
#   LOCAL IMPORTS
#

from context import websocket_server
from websocket_server import SimpleWebSocketServer, StreamingRDPWebSocket

###############################################################
#
#   GLOBAL VARIABLES
#

MockServerHost = "127.0.0.1"
MockServerPort = 9001

###############################################################
#
#   PROGRAM SPECIFIC VARIABLES
#

ProgramNumArgs = 0
ProgramDescription = ''
ProgramVersionStr = 'v0.0'
ProgramUsage = ''


###############################################################
#
#   CLASSES
#

###############################################################
#
#   FUNCTIONS
#

def main():
    # #   parsing arguments
    # parser = argparse.ArgumentParser( description = '{}'.format( ProgramDescription ),
    #                                         usage = '{}'.format( ProgramUsage ) )
    # args = parser.parse_args()

    ###############################################################
    #   begin coding

    async def run_async():
        #   build mock server
        simple_websocket_server = SimpleWebSocketServer(MockServerHost, MockServerPort, StreamingRDPWebSocket)

        #   create asyncio task for run mock server
        task = asyncio.create_task(simple_websocket_server.serveforever())
        await asyncio.gather(task)

    #   run with asyncio
    asyncio.get_event_loop().run_until_complete(run_async())


if __name__ == '__main__':
    #   call main function
    main()
