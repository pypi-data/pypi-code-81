# coding: utf-8

###############################################################
#
#   STANDARD IMPORTS
#

import sys

import asyncio
import websockets

import logging


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
#   CLASSE DEFINITIONS
#

class SimpleAsyncWebsocketServer(object):
    """ this class is desiged for a simple async websocket server.
    Developer don't need to change anythings in this class.
    This class only need a host and port for websocket and the websocket message handler clas.
    The websocket message handler class is a logical layer on how to process each kind of message from client.
    """

    #   logging format
    LoggingFormat = logging.Formatter(
        '[%(asctime)s] - [%(levelname)s] - [%(module)s] - [%(funcName)s] - Thread %(thread)d | %(threadName)s\n%(message)s')

    def __init__(self, host, port,
                 message_handler_cls,
                 scenario_file_name: str = None):
        self._host = host
        self._port = port

        ###############################################
        #   setup logger
        self._logger = logging.getLogger(self.__class__.__name__)

        #   for stdout logger stream handler
        self._stdout_stream_handler = logging.StreamHandler(sys.stdout)
        self._stdout_stream_handler.setFormatter(self.LoggingFormat)
        self._logger.addHandler(self._stdout_stream_handler)

        ###############################################
        #   setup handler

        #   create the message handler object
        self._message_handler = message_handler_cls(self._logger,
                                                    scenario_file_name=scenario_file_name)

    def set_log_level(self, log_level):
        self._logger.setLevel(log_level)

    def run(self):
        """ run websocket server """
        self._logger.debug('run()')

        #   build the task for websocket
        assert hasattr(self._message_handler, '_handle_messages')
        start_server = websockets.serve(self._message_handler._handle_messages, self._host, self._port, subprotocols=['tr_json2', ])

        #   run
        asyncio.get_event_loop().run_until_complete(start_server)
