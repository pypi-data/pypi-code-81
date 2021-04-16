# coding: utf-8

###############################################################
#
#   STANDARD IMPORTS
#

import abc

import json

import asyncio


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

class SimpleAsyncMessageHandler(abc.ABC):
    """ this class is desiged for handing the mssage from websocket client.
    this is an abstruct class for developer to define their own kind of websocket server that will response to client.
    developer must overide the process_messages method.
    """

    def __init__(self, logger, scenario_file_name: str = None):
        self._logger = logger
        self._scenario_file_name = scenario_file_name

    async def _handle_messages(self, websocket, path):
        """ handle the message from websocket client """
        self._logger.debug(f'_handle_messages(websocket={websocket}, path={path}')

        while True:

            #   loop over all received message from websocket
            async for message in websocket:
                self._logger.debug(f'received message = {message}')

                #   extract message into json format
                #       then call _process_messages
                message_json = json.loads(message)
                await self._process_message(websocket, message_json)

    @abc.abstractmethod
    def _process_message(self, websocket, message):
        """ this is an abstract function for process each kind of messages from client 
        note that messages is already in json format.
        """
        pass


class RDPMessageHandler(SimpleAsyncMessageHandler):
    """ this class is desinged for a RDP protocol. (define here https://confluence.refinitiv.com/display/EPA/Streaming+Standards)
    """

    @staticmethod
    async def call_every(loop, seconds, func, *args, **kwargs):
        async def periodic():
            while True:
                await func(*args, **kwargs)
                await asyncio.sleep(seconds)

        #   create periodic task
        task = loop.create_task(periodic())

        #   done
        return task

    async def send_message(self, websocket, messages):
        self._logger.debug(f'send_message(websocket={websocket}, messages={messages}')
        await websocket.send(json.dumps(messages))

    def __init__(self, logger, scenario_file_name: str = None):
        SimpleAsyncMessageHandler.__init__(self, logger, scenario_file_name)

        #   dict of stream id to all update reponse task
        self._update_message_tasks = {}

    async def _process_message(self, websocket, message):
        """ this is an abstract function for process each kind of messages from client 
        note that messages is already in json format.
        """
        self._logger.debug(f'_process_message(websocket={websocket}, message={message}')

        if message is None:
            #   do nothing
            return

        #   check method of request from client
        message_method = message.get('method')
        assert message_method is not None
        self._logger.debug(f'    method={message_method}')

        #   process by message method
        if message_method == 'Auth':
            #   do a process authentication
            await self._process_auth(websocket, message)

        elif message_method == 'Subscribe':
            #   do a process subscribe
            await self._process_subscribe(websocket, message)

        elif message_method == 'Close':
            #   do close subscription
            self._process_close(websocket, message)

    async def _process_auth(self, websocket, message):
        """ process login request """

        #   construct the login response
        login_response = {
            "streamID": message.get('streamID'),
            "type": "Ack",
            "state": {
                "code": 200,
                "message": "Ok"
                }
            }

        #   send response to client
        await self.send_message(websocket, [login_response])

    async def _process_subscribe(self, websocket, message):
        """ process subscribe request """
        self._logger.debug(f'_process_subscribe(message={message}')

        assert 'service' in message or 'context' in message

        stream_id = message.get('streamID')
        self._logger.debug(f'     stream_id={stream_id}')
        assert stream_id is not None

        #   initialize parameters
        name = None
        request_service = None
        request_context = None

        #   by service
        if 'service' in message:
            request_service = message.get('service')
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
                await self.send_message(websocket, [response])

            else:
                assert False

        #   by context
        if 'context' in message:
            #   extract context
            request_context = message.get('context')
            assert request_context is not None

            #   extact universe
            request_universe = message.get('universe')
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
            await self.send_message(websocket, [response])

        #   check for a subscribe message and setup a repeat update message
        if request_service is not None or request_context is not None:
            #   set the timer to send the update message
            loop = asyncio.get_event_loop()
            task = await self.call_every(loop, 1,
                                         self._send_update_message,
                                         websocket=websocket,
                                         stream_id=stream_id,
                                         name=name,
                                         service=request_service,
                                         context=request_context)

            #   store update message task

            #   cancel old task for this stream id
            if stream_id in self._update_message_tasks:
                #   cancel this task
                old_task = self._update_message_tasks[stream_id]
                old_task.cancel()

            #   store the update task of this stream id
            self._update_message_tasks[stream_id] = task

    def _process_close(self, websocket, message):
        """ process close request """

        #   stream id
        stream_id = message.get('streamID')
        self._logger.debug(f'     stream_id={stream_id}')
        assert stream_id is not None

        #   cancel old task for this stream id
        if stream_id in self._update_message_tasks:
            #   cancel this task
            task = self._update_message_tasks[stream_id]
            task.cancel()

    async def _send_update_message(self, websocket, stream_id: int, name: str,
                                   service: str = None, context: str = None):

        #   generate update message
        update_message = self._generate_update_message(stream_id, name,
                                                       service=service, context=context)

        #   convert update message to str
        await self.send_message(websocket, [update_message, ])

    def _generate_update_message(self, stream_id: int, name: str, service: str = None, context: str = None):
        """ generate the update message based on type of service or context """
        assert service is not None or context is not None

        #   check the kind of update
        if service is not None:
            return {
                "streamID": stream_id,
                "type": "Update",
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
