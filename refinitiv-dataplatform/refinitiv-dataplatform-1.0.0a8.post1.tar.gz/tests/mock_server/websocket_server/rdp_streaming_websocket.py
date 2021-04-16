# coding: utf-8

###############################################################
#
#   STANDARD IMPORTS
#

import json

import logging

import asyncio

###############################################################
#
#   REFINITIV IMPORTS
#

###############################################################
#
#   LOCAL IMPORTS
#

from .websocket_server import WebSocket, SimpleWebSocketServer


###############################################################
#
#   CLASSE DEFINITIONS
#

class StreamingRDPWebSocket(WebSocket):

    @staticmethod
    def call_every(loop, seconds, func, *args, now=True):
        def repeat(now=True, times=frange(loop.time() + seconds, None, seconds)):
            if now:
                func(*args)
            loop.call_at(next(times), repeat)

        repeat(now=now)

    def __init__(self, server, sock, address):
        super().__init__(server, sock, address)

    #   override methods
    def handleMessage(self):
        """
            Called when websocket frame is received.
            To access the frame data call self.data.

            If the frame is Text then self.data is a unicode object.
            If the frame is Binary then self.data is a bytearray object.
        """
        #   process the response to client by type of message

        #   extract the response into json
        request = json.loads(self.data)
        # print(f'request message ----> {request}')

        #   check method of request from client
        message_method = request.get('method')
        assert message_method is not None

        #   process by message method
        if message_method == 'Auth':
            #   do a process authentication
            self._process_auth(request)

        elif message_method == 'Subscribe':
            #   do a process subscribe
            self._process_subscribe(request)

    def _process_auth(self, request):
        """ process login request """

        #   construct the login response
        login_response = {
            "streamID": request.get('streamID'),
            "type": "Ack",
            "state": {
                "code": 200,
                "message": "OK"
                }
            }

        #   send response to client
        login_response_str = json.dumps([login_response])
        self.sendMessage(login_response_str)

    def _process_subscribe(self, request):
        """ process subscribe request """

        assert 'service' in request or 'context' in request

        stream_id = request.get('streamID')
        assert stream_id is not None

        #   by service
        name = None
        if 'service' in request:
            request_service = request.get('service')
            assert request_service is not None

            #   build the response by service
            if request_service == 'analytics/bond/contract':
                #   bond/contract
                response = {
                    "streamID": stream_id,
                    "type": "Response",
                    "data": [
                        ["US10YT=RR",
                         "FixedRateBond",
                         "2020-08-17T00:00:00Z",
                         "2030-08-15T00:00:00Z",
                         0.625,
                         0.0169836956521739,
                         99.8203125,
                         99.8372961956522,
                         0.643628449265034,
                         "2030-08-15T00:00:00Z",
                         9.65094016496659,
                         9.68199826322822,
                         9.63523816980838,
                         9.97282608695652,
                         99.754587651723
                         ]
                        ]
                    }
                #   send response to client
                response_str = json.dumps([response])
                self.sendMessage(response_str)

                #   extract universe

            else:
                assert False

        #   by context
        elif 'context' in request:
            #   extract context
            request_context = request.get('context')
            assert request_context is not None

            #   extact universe
            request_universe = request.get('universe')
            assert request_universe is not None
            assert isinstance(request_universe, list)
            assert len(request_universe) > 0

            #   extact name in universe
            # warning support only one universe
            request_universe_name = request_universe[0].get('name')
            assert request_universe_name is not None

            response = {
                "streamID": stream_id,
                "type": "Response",
                "fields": {
                    "ACVOL_1": 8719016,
                    "ADJUST_CLS": 392.8,
                    "ASK": 9000,
                    "ASKSIZE": 1,
                    "ASKXID": "BOS",
                    "ASK_MMID1": "BOS",
                    "BID": 0.01,
                    "BIDSIZE": 1,
                    "BIDXID": "BOS",
                    "BID_MMID1": "BOS",
                    "BID_NET_CH": null,
                    "BID_TICK_1": "⇩",
                    "BLKCOUNT": 5,
                    "BLKVOLUM": 116195,
                    "CLOSE_ASK": 398.1,
                    "CLOSE_BID": 398.01,
                    "CTS_QUAL": " ",
                    "CUM_EX_MKR": " ",
                    "CURRENCY": "USD",
                    "EXCHTIM": "21:00:01",
                    "EXDIVDATE": null,
                    "GV1_FLAG": null,
                    "GV1_TEXT": "-",
                    "HIGH_1": 398.85,
                    "HSTCLBDDAT": null,
                    "HSTCLSDATE": "2017-11-28",
                    "HST_CLOSE": 392.8,
                    "HST_CLSBID": null,
                    "INSCOND": " ",
                    "INSPRC": null,
                    "INSVOL": null,
                    "IRGCOND": "132",
                    "IRGPRC": 398.85,
                    "IRGVOL": 144,
                    "IRGXID": "CIN",
                    "LOW_1": 394.11,
                    "TRADE_DATE": "2017-11-29",
                    "TRDPRC_1": 398.15,
                    "TRDTIM_MS": 75601000,
                    "TRDVOL_1": 26506,
                    "TRDXID_1": "NAS",
                    "TRD_UNITS": "2DP ",
                    "TURNOVER": 392.8,
                    "VOL_X_PRC1": 397.9481
                    },
                "name": request_universe_name
                }
            #   send response to client
            response_str = json.dumps([response])
            self.sendMessage(response_str)

            #   done 
            return

        else:
            #   unknown subsription
            assert False

        #   set the timer to send the update message
        loop = asyncio.get_event_loop()
        self.call_every(loop, 1, self._send_update_message, stream_id, name, service, context)

    def _send_update_message(self, stream_id, name, service=None, context=None):

        #   generate update message
        update_message = self._generate_update_message(stream_id, name, service, context)

        #   convert update message to str
        update_message_str = json.dumps([update_message, ])
        self.sendMessage(update_message_str)

    def _generate_update_message(self, stream_id: int, name: str, service: str = None, context: str = None):
        """ generate the update message based on type of service or context """

        #   check the kind of update
        if service is not None:
            return {
                "streamID": stream_id,
                "type": "Response",
                "data": [
                    ["US10YT=RR",
                     "FixedRateBond",
                     "2020-08-17T00:00:00Z",
                     "2030-08-15T00:00:00Z",
                     0.625,
                     0.0169836956521739,
                     99.8203125,
                     99.8372961956522,
                     0.643628449265034,
                     "2030-08-15T00:00:00Z",
                     9.65094016496659,
                     9.68199826322822,
                     9.63523816980838,
                     9.97282608695652,
                     99.754587651723
                     ]
                    ]
                }

        elif context is not None:
            return {"streamID": stream_id,
                    "type": "Update",
                    "fields": {
                        "ASK": 401.55,
                        "ASKSIZE": 10,
                        "ASKXID": "NAS",
                        "ASK_MMID1": "NAS",
                        "BID": 401.51,
                        "BIDSIZE": 10,
                        "BIDXID": "NAS",
                        "BID_MMID1": "NAS",
                        "BID_NET_CH": 3.49,
                        "BID_TICK_1": "þ",
                        "GV1_TEXT": "-",
                        "QUOTIM": "14:40:32:001:000:000",
                        "QUOTIM_MS": 52832001
                        },
                    "name": name,
                    "updateType": "Quote"
                    }

        else:
            assert (False)
