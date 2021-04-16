# coding: utf-8

###############################################################
#
#   STANDARD IMPORTS
#

import argparse

import asyncio

import logging

import tracemalloc

tracemalloc.start()

###############################################################
#
#   REFINITIV IMPORTS
#

###############################################################
#
#   LOCAL IMPORTS
#

from context import async_websocket_server
from async_websocket_server import SimpleAsyncWebsocketServer, RDPMessageHandler

###############################################################
#
#   GLOBAL VARIABLES
#

WebsocketServerHost = '127.0.0.1'
WebsocketServerPort = 9001

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

    #   build generic RDP websocket server
    rdp_websocket_server = SimpleAsyncWebsocketServer(WebsocketServerHost, WebsocketServerPort,
                                                      RDPMessageHandler)
    rdp_websocket_server.set_log_level(logging.DEBUG)
    rdp_websocket_server.run()

    #   run forever
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    #   call main function
    main()
