# coding: utf-8

###############################################################
#
#   STANDARD IMPORTS
#

import pytest

from unittest.mock import MagicMock

import asyncio

import httpx

import datetime

###############################################################
#
#   REFINITIV IMPORTS
#

import refinitiv.dataplatform as rdp

from refinitiv.dataplatform.errors import EnvError

###############################################################
#
#   LOCAL IMPORTS
#

###############################################################
#
#   TEST CASES
#

def test_trade_data_stream_constructor():
    ############################################
    #   prepare things

    session = MagicMock()

    ############################################
    #   test

    trade_data_stream = rdp.TradeDataStream(session=session, 
                                                universe=[])

    assert isinstance(trade_data_stream, rdp.TradeDataStream)

def test_trade_data_stream_constructor_with_cache_size():
    ############################################
    #   prepare things

    session = MagicMock()

    ############################################
    #   test

    trade_data_stream = rdp.TradeDataStream(session=session, 
                                                universe=[],
                                            max_order_summary_cache=0,
                                            max_order_events_cache=0)

    assert isinstance(trade_data_stream, rdp.TradeDataStream)
    assert trade_data_stream._max_order_events_cache == 0
    assert trade_data_stream._max_order_summary_cache == 0

def test_trade_data_stream_parameters_case_1():
    ############################################
    #   prepare things

    session = MagicMock()

    ############################################
    #   test

    trade_data_stream = rdp.TradeDataStream(session=session, 
                                                universe=['foo'],
                                                universe_type=rdp.TradeDataStream.UniverseTypes.UserID,
                                                events=rdp.TradeDataStream.Events.Full,
                                                finalized_orders=rdp.TradeDataStream.FinalizedOrders.No,
                                                views=[rdp.TradeDataStream.Views.OrderKey,
                                                        rdp.TradeDataStream.Views.OrderTime,
                                                ],
                                                filters=['foo']
                                                )

    assert isinstance(trade_data_stream, rdp.TradeDataStream)
    assert trade_data_stream._parameters == {'universeType':rdp.TradeDataStream.UniverseTypes.UserID.value,
                                                    'events': rdp.TradeDataStream.Events.Full.value,
                                                    'finalizedOrders': rdp.TradeDataStream.FinalizedOrders.No.value,
                                                    'filters': ['foo']
                                                }

def test_trade_data_stream_parameters_case_2():
    ############################################
    #   prepare things

    session = MagicMock()

    ############################################
    #   test

    trade_data_stream = rdp.TradeDataStream(session=session, 
                                                universe=['foo'],
                                                universe_type=rdp.TradeDataStream.UniverseTypes.UserID,
                                                events=rdp.TradeDataStream.Events.No,
                                                finalized_orders=None,
                                                views=[rdp.TradeDataStream.Views.OrderKey,
                                                        rdp.TradeDataStream.Views.OrderTime,
                                                ],
                                                filters=['foo']
                                                )

    assert isinstance(trade_data_stream, rdp.TradeDataStream)
    assert trade_data_stream._parameters == {'universeType':rdp.TradeDataStream.UniverseTypes.UserID.value,
                                                    'events': rdp.TradeDataStream.Events.No.value,
                                                    'finalizedOrders': rdp.TradeDataStream.FinalizedOrders.P1D.value,
                                                    'filters': ['foo']
                                                }

def test_trade_data_stream_parameters_case_3():
    ############################################
    #   prepare things

    session = MagicMock()

    ############################################
    #   test

    trade_data_stream = rdp.TradeDataStream(session=session, 
                                                universe=['foo'],
                                                universe_type=None,
                                                events=None,
                                                finalized_orders=None,
                                                views=[rdp.TradeDataStream.Views.OrderKey,
                                                        rdp.TradeDataStream.Views.OrderTime,
                                                ],
                                                filters=None
                                                )

    assert isinstance(trade_data_stream, rdp.TradeDataStream)
    assert trade_data_stream._parameters == {'universeType':rdp.TradeDataStream.UniverseTypes.RIC.value,
                                                    'events': rdp.TradeDataStream.Events.Full.value,
                                                    'finalizedOrders': rdp.TradeDataStream.FinalizedOrders.P1D.value,
                                                }

@pytest.mark.asyncio
async def test_trade_data_stream_open_async():
    ############################################
    #   prepare things

    async def mock_open_async(*args, **kwargs):
        return rdp.delivery.StreamState.Open

    session = MagicMock()

    ############################################
    #   test

    trade_data_stream = rdp.TradeDataStream(session=session, 
                                                universe=['foo'] )
    
    trade_data_stream._stream._stream_id = 12345
    trade_data_stream._stream.open_async = mock_open_async

    await trade_data_stream.open_async()

    assert trade_data_stream.state == rdp.delivery.StreamState.Open
    assert len(trade_data_stream._order_summary_dict) == 0
    assert len(trade_data_stream._order_key_to_event_list) == 0

@pytest.mark.asyncio
async def test_trade_data_stream_close_async():
    ############################################
    #   prepare things

    async def mock_open_async(*args, **kwargs):
        return rdp.delivery.StreamState.Open

    async def mock_close_async(*args, **kwargs):
        return rdp.delivery.StreamState.Closed

    session = MagicMock()

    ############################################
    #   test

    trade_data_stream = rdp.TradeDataStream(session=session, 
                                                universe=['foo'] )
    
    trade_data_stream._stream._stream_id = 12345
    trade_data_stream._stream.open_async = mock_open_async
    trade_data_stream._stream.close_async = mock_close_async

    assert trade_data_stream.state == rdp.delivery.StreamState.Closed
    
    await trade_data_stream.open_async()

    assert trade_data_stream.state == rdp.delivery.StreamState.Open

    await trade_data_stream.close_async()

    assert trade_data_stream.state == rdp.delivery.StreamState.Closed


def test_trade_data_stream_on_response_message_case_1():
    ############################################
    #   prepare things

    session = MagicMock()
    #   callback
    on_add_func = MagicMock()
    on_update_func = MagicMock()
    on_remove_func = MagicMock()
    on_event_func = MagicMock()
    on_state_func = MagicMock()
    on_complete_func = MagicMock()

    mock_response = {"streamID":"1",
                        "type":"Response",
                        "headers":[
                                    {"id":"OrderKey","type":"String","format":"","description":""},
                                    {"id":"OrderTime","type":"String","format":"datetime","description":""},
                                    {"id":"RIC","type":"String","format":"","description":""},
                                    {"id":"Side","type":"String","format":"","description":""},
                                    {"id":"AveragePrice","type":"Decimal","format":"0.0000","description":""},
                                    {"id":"OrderStatus","type":"String","format":"","description":""},
                                    {"id":"OrderQuantity","type":"Integer","format":"","description":""}
                                ],
                        "state":{
                                "code":200,"status":"Ok","stream":"Open","message":"queueSize=5089"
                            }
                    }

    ############################################
    #   test

    trade_data_stream = rdp.TradeDataStream(session=session, 
                                                universe=['foo'],
                                                on_add=on_add_func,
                                                on_update=on_update_func,
                                                on_remove=on_remove_func,
                                                on_event=on_event_func,
                                                on_state=on_state_func,
                                                on_complete=on_complete_func,
                                            )

    trade_data_stream._TradeDataStream__on_response('bar', mock_response)

    assert len(trade_data_stream._order_summary_header_names) != 0

    on_add_func.assert_not_called()
    on_update_func.assert_not_called()
    on_remove_func.assert_not_called()
    on_event_func.assert_not_called()
    on_state_func.assert_called_once()
    on_complete_func.assert_not_called()
    
def test_trade_data_stream_on_response_message_case_2():
    ############################################
    #   prepare things

    session = MagicMock()
    #   callback
    on_add_func = MagicMock()
    on_update_func = MagicMock()
    on_remove_func = MagicMock()
    on_event_func = MagicMock()
    on_state_func = MagicMock()
    on_complete_func = MagicMock()

    mock_response = {"streamID":"1",
                        "type":"Response",
                        "headers":[
                                    {"id":"OrderKey","type":"String","format":"","description":""},
                                    {"id":"OrderTime","type":"String","format":"datetime","description":""},
                                    {"id":"RIC","type":"String","format":"","description":""},
                                    {"id":"Side","type":"String","format":"","description":""},
                                    {"id":"AveragePrice","type":"Decimal","format":"0.0000","description":""},
                                    {"id":"OrderStatus","type":"String","format":"","description":""},
                                    {"id":"OrderQuantity","type":"Integer","format":"","description":""}
                                ],
                        "data":[
                                    ["REDI_1600992048000-4949545555-117-55-83202102110|2761.T","2021-02-11T01:05:03.413","2761.T","Buy",None,"Cxl",100],
                                ],
                        "state":{
                                "code":200,"status":"Ok","stream":"Open","message":"queueSize=5089"
                            }
                    }

    ############################################
    #   test

    trade_data_stream = rdp.TradeDataStream(session=session, 
                                                universe=['foo'],
                                                on_add=on_add_func,
                                                on_update=on_update_func,
                                                on_remove=on_remove_func,
                                                on_event=on_event_func,
                                                on_state=on_state_func,
                                                on_complete=on_complete_func,
                                            )

    trade_data_stream._TradeDataStream__on_response('bar', mock_response)

    assert len(trade_data_stream._order_summary_header_names) != 0

    on_add_func.assert_called_once()
    on_update_func.assert_not_called()
    on_remove_func.assert_not_called()
    on_event_func.assert_not_called()
    on_state_func.assert_called_once()
    on_complete_func.assert_not_called()
    
    
def test_trade_data_stream_on_response_message_case_3():
    ############################################
    #   prepare things

    session = MagicMock()
    #   callback
    on_add_func = MagicMock()
    on_update_func = MagicMock()
    on_remove_func = MagicMock()
    on_event_func = MagicMock()
    on_state_func = MagicMock()
    on_complete_func = MagicMock()

    mock_response = {"streamID":"1",
                        "type":"Response",
                        "headers":[
                                    {"id":"OrderKey","type":"String","format":"","description":""},
                                    {"id":"OrderTime","type":"String","format":"datetime","description":""},
                                    {"id":"RIC","type":"String","format":"","description":""},
                                    {"id":"Side","type":"String","format":"","description":""},
                                    {"id":"AveragePrice","type":"Decimal","format":"0.0000","description":""},
                                    {"id":"OrderStatus","type":"String","format":"","description":""},
                                    {"id":"OrderQuantity","type":"Integer","format":"","description":""}
                                ],
                        "data":[
                                    ["REDI_1600992048000-4949545555-117-55-83202102110|2761.T","2021-02-11T01:05:03.413","2761.T","Buy",None,"Cxl",100],
                                ],
                        "messages":[
                            {"key":"REDI_1600992048000-4949545555-117-55-83202102110|2761.T",
                                "events":[
                                            {
                                                "EventTime":"2021-02-11T00:39:07.667","OrderId":"REDI-1600992048-S7u-11677202102110","EventType":"Accepted",
                                                "EventData":{
                                                    "OrderQuantity":100,"LimitPrice":6180.0000,"StopPrice":0.0000,"DestinationType":"Dma","AlgoId":0,"TimeInForce":"Day","LastCapacity":"Agency_A"
                                                }
                                            }, 
                                            {
                                                "EventTime":"2021-02-11T00:39:07.667","OrderId":"REDI-1600992048-S7u-11677202102110","EventType":"Accepted",
                                                "EventData":{
                                                    "OrderQuantity":100,"LimitPrice":6180.0000,"StopPrice":0.0000,"DestinationType":"Dma","AlgoId":0,"TimeInForce":"Day","LastCapacity":"Agency_A"
                                                }
                                            }, 
                                ]
                            }
                        ],
                        "state":{
                                "code":200,"status":"Ok","stream":"Open","message":"queueSize=5089"
                            }
                    }

    ############################################
    #   test

    trade_data_stream = rdp.TradeDataStream(session=session, 
                                                universe=['foo'],
                                                on_add=on_add_func,
                                                on_update=on_update_func,
                                                on_remove=on_remove_func,
                                                on_event=on_event_func,
                                                on_state=on_state_func,
                                                on_complete=on_complete_func,
                                            )

    trade_data_stream._TradeDataStream__on_response('bar', mock_response)

    assert len(trade_data_stream._order_summary_header_names) == 7

    assert len(trade_data_stream._order_summary_dict) == 1

    on_add_func.assert_called_once()
    on_update_func.assert_not_called()
    on_remove_func.assert_not_called()
    on_event_func.assert_called()
    on_state_func.assert_called_with(trade_data_stream,
                                    {"code":200,"status":"Ok","stream":"Open","message":"queueSize=5089"})
    on_complete_func.assert_not_called()


def test_trade_data_stream_on_response_message_case_4():
    ############################################
    #   prepare things

    session = MagicMock()
    #   callback
    on_add_func = MagicMock()
    on_update_func = MagicMock()
    on_remove_func = MagicMock()
    on_event_func = MagicMock()
    on_state_func = MagicMock()
    on_complete_func = MagicMock()

    mock_response = {"streamID":"1",
                        "type":"Response",
                        "headers":[
                                    {"id":"OrderKey","type":"String","format":"","description":""},
                                    {"id":"OrderTime","type":"String","format":"datetime","description":""},
                                    {"id":"RIC","type":"String","format":"","description":""},
                                    {"id":"Side","type":"String","format":"","description":""},
                                    {"id":"AveragePrice","type":"Decimal","format":"0.0000","description":""},
                                    {"id":"OrderStatus","type":"String","format":"","description":""},
                                    {"id":"OrderQuantity","type":"Integer","format":"","description":""}
                                ],
                        "data":[
                                    ["REDI_1600992048000-4949545555-117-55-83202102110|2761.T","2021-02-11T01:05:03.413","2761.T","Buy",None,"Cxl",100],
                                ],
                        "messages":[
                            {"key":"REDI_1600992048000-4949545555-117-55-83202102110|2761.T",
                                "events":[
                                            {
                                                "EventTime":"2021-02-11T00:39:07.667","OrderId":"REDI-1600992048-S7u-11677202102110","EventType":"Accepted",
                                                "EventData":{
                                                    "OrderQuantity":100,"LimitPrice":6180.0000,"StopPrice":0.0000,"DestinationType":"Dma","AlgoId":0,"TimeInForce":"Day","LastCapacity":"Agency_A"
                                                }
                                            }, 
                                            {
                                                "EventTime":"2021-02-11T00:39:07.667","OrderId":"REDI-1600992048-S7u-11677202102110","EventType":"Accepted",
                                                "EventData":{
                                                    "OrderQuantity":100,"LimitPrice":6180.0000,"StopPrice":0.0000,"DestinationType":"Dma","AlgoId":0,"TimeInForce":"Day","LastCapacity":"Agency_A"
                                                }
                                            }, 
                                ]
                            }
                        ],
                        "state":{
                                "code":200,"status":"Ok","stream":"Open","message":"queueSize=0"
                            }
                    }

    ############################################
    #   test

    trade_data_stream = rdp.TradeDataStream(session=session, 
                                                universe=['foo'],
                                                on_add=on_add_func,
                                                on_update=on_update_func,
                                                on_remove=on_remove_func,
                                                on_event=on_event_func,
                                                on_state=on_state_func,
                                                on_complete=on_complete_func,
                                            )

    trade_data_stream._TradeDataStream__on_response('bar', mock_response)

    assert len(trade_data_stream._order_summary_header_names) == 7

    assert len(trade_data_stream._order_summary_dict) == 1

    on_add_func.assert_called_once()
    on_update_func.assert_not_called()
    on_remove_func.assert_not_called()
    on_event_func.assert_called()
    on_state_func.assert_called_with(trade_data_stream,
                                    {"code":200,"status":"Ok","stream":"Open","message":"queueSize=0"})
    on_complete_func.assert_called_once()


def test_trade_data_stream_on_ack_message():
    ############################################
    #   prepare things

    session = MagicMock()
    #   callback
    on_add_func = MagicMock()
    on_update_func = MagicMock()
    on_remove_func = MagicMock()
    on_event_func = MagicMock()
    on_state_func = MagicMock()
    on_complete_func = MagicMock()

    mock_ack = {"streamID":"2","type":"Ack","state":{"code":200,"status":"Ok","message":"Set token successfully"}}

    ############################################
    #   test

    trade_data_stream = rdp.TradeDataStream(session=session, 
                                                universe=['foo'],
                                                on_add=on_add_func,
                                                on_update=on_update_func,
                                                on_remove=on_remove_func,
                                                on_event=on_event_func,
                                                on_state=on_state_func,
                                                on_complete=on_complete_func,
                                            )

    trade_data_stream._TradeDataStream__on_ack('bar', mock_ack)

    assert trade_data_stream._order_summary_header_names is None

    assert len(trade_data_stream._order_summary_dict) == 0

    on_add_func.assert_not_called()
    on_update_func.assert_not_called()
    on_remove_func.assert_not_called()
    on_event_func.assert_not_called()
    on_state_func.assert_not_called()
    on_complete_func.assert_not_called()


def test_trade_data_stream_on_update_message_case_1():
    ############################################
    #   prepare things

    session = MagicMock()
    #   callback
    on_add_func = MagicMock()
    on_update_func = MagicMock()
    on_remove_func = MagicMock()
    on_event_func = MagicMock()
    on_state_func = MagicMock()
    on_complete_func = MagicMock()

    mock_response = {"streamID":"1",
                        "type":"Response",
                        "headers":[
                                    {"id":"OrderKey","type":"String","format":"","description":""},
                                    {"id":"OrderTime","type":"String","format":"datetime","description":""},
                                    {"id":"RIC","type":"String","format":"","description":""},
                                    {"id":"Side","type":"String","format":"","description":""},
                                    {"id":"AveragePrice","type":"Decimal","format":"0.0000","description":""},
                                    {"id":"OrderStatus","type":"String","format":"","description":""},
                                    {"id":"OrderQuantity","type":"Integer","format":"","description":""}
                                ],
                        "state":{
                                "code":200,"status":"Ok","stream":"Open","message":"queueSize=0"
                            }
                    }

    mock_update = {
                        "streamID":"1",
                        "type":"Update",
                        "data":[
                                ["REDI_1601023761000-4948485052-48-50-83202102100|SBUX.OQ","2021-02-10T08:21:28.199","SBUX.OQ","Sell",None,"Pend",100]
                            ],
                        "update":[
                                    {"key":"REDI_1601023761000-4948485052-48-50-83202102100|SBUX.OQ","Side":"Buy"}
                                ],
                        "messages":[
                                    {"key":"REDI_1601023761000-4948485052-48-50-83202102100|SBUX.OQ",
                                    "events":[
                                            {"EventTime":"2021-02-10T08:21:28.199","OrderId":"REDI-1601023791-S20-10028202102100","EventType":"Replaced",
                                                "EventData":{"OrderQuantity":100,"LimitPrice":83.2000,"StopPrice":0.0000,"DestinationType":"Dma","AlgoId":0,"TimeInForce":"Day","LastCapacity":"Agency_A"
                                            }
                                        }
                                    ]
                                }
                            ]
                        }

    ############################################
    #   test

    trade_data_stream = rdp.TradeDataStream(session=session, 
                                                universe=['foo'],
                                                on_add=on_add_func,
                                                on_update=on_update_func,
                                                on_remove=on_remove_func,
                                                on_event=on_event_func,
                                                on_state=on_state_func,
                                                on_complete=on_complete_func,
                                            )

    trade_data_stream._TradeDataStream__on_response('bar', mock_response)
    assert len(trade_data_stream._order_summary_header_names) == 7
    assert len(trade_data_stream._order_summary_dict) == 0

    trade_data_stream._TradeDataStream__on_update('bar', mock_update)
    assert len(trade_data_stream._order_summary_header_names) == 7
    assert len(trade_data_stream._order_summary_dict) == 1
    assert len(trade_data_stream._order_key_to_event_list) == 1

    on_add_func.assert_called_once()
    on_update_func.assert_called_once()
    on_remove_func.assert_not_called()
    on_event_func.assert_called_once()
    on_complete_func.assert_called_once()


def test_trade_data_stream_on_update_message_case_2_no_subscribed_field_in_update():
    ############################################
    #   prepare things

    session = MagicMock()
    #   callback
    on_add_func = MagicMock()
    on_update_func = MagicMock()
    on_remove_func = MagicMock()
    on_event_func = MagicMock()
    on_state_func = MagicMock()
    on_complete_func = MagicMock()

    mock_response = {'streamID': '1', 'type': 'Response', 'headers': [{'id': 'OrderKey', 'type': 'String', 'format': '', 'description': ''}, {'id': 'OrderTime', 'type': 'String', 'format': 'datetime', 'description': ''}, {'id': 'RIC', 'type': 'String', 'format': '', 'description': ''}, {'id': 'Side', 'type': 'String', 'format': '', 'description': ''}, {'id': 'AveragePrice', 'type': 'Decimal', 'format': '0.0000', 'description': ''}, {'id': 'OrderStatus', 'type': 'String', 'format': '', 'description': ''}, {'id': 'OrderQuantity', 'type': 'Integer', 'format': '', 'description': ''}], 'state': {'code': 200, 'status': 'Ok', 'stream': 'Open', 'message': 'queueSize=10701'}}
    mock_update = {"streamID":"1",
                        "type":"Update",
                        "data":[["REDI_1600696813000-5053565255-48-103-83202102110|STIM.OQ","2021-02-11T14:55:20.353","STIM.OQ","Buy",4.1968,"Comp",2500]],
                        "update":[{"key":"REDI_1600696813000-5053565255-48-103-83202102110|STIM.OQ","AnalyticStartDateTimeSource":"MarketOpen","AnalyticEndDateTimeEventType":"LastExecution","AnalyticEndDateTime":"2021-02-11T14:55:20.353000000"}],
                        "messages":[{"key":"REDI_1600696813000-5053565255-48-103-83202102110|STIM.OQ","events":[{"EventTime":"2021-02-11T14:55:20.353","OrderId":"REDI-1600696813-Sg0-25847202102110","EventType":"Executed",
                                        "EventData":{"ExecutionId":"REDI-1600696813-Rg0-52853","ExecutionQuantity":2000,"ExecutionPrice":4.2000,"ExecutionValue":8400.0000,"LastMarketMIC":"XNAS"}}]}]
                    }


    ############################################
    #   test

    trade_data_stream = rdp.TradeDataStream(session=session, 
                                                universe=['foo'],
                                                on_add=on_add_func,
                                                on_update=on_update_func,
                                                on_remove=on_remove_func,
                                                on_event=on_event_func,
                                                on_state=on_state_func,
                                                on_complete=on_complete_func,
                                            )

    trade_data_stream._TradeDataStream__on_response('bar', mock_response)
    assert len(trade_data_stream._order_summary_header_names) == 7
    assert len(trade_data_stream._order_summary_dict) == 0

    trade_data_stream._TradeDataStream__on_update('bar', mock_update)
    assert len(trade_data_stream._order_summary_header_names) == 7
    assert len(trade_data_stream._order_summary_dict) == 1
    assert len(trade_data_stream._order_key_to_event_list) == 1

    on_add_func.assert_called_once()
    on_update_func.assert_called_once()
    on_remove_func.assert_not_called()
    on_event_func.assert_called_once()
    on_complete_func.assert_not_called()


def test_trade_data_stream_on_update_message_case_3():
    ############################################
    #   prepare things

    session = MagicMock()
    #   callback
    on_add_func = MagicMock()
    on_update_func = MagicMock()
    on_remove_func = MagicMock()
    on_event_func = MagicMock()
    on_state_func = MagicMock()
    on_complete_func = MagicMock()

    mock_response = {"streamID":"1",
                        "type":"Response",
                        "headers":[
                                    {"id":"OrderKey","type":"String","format":"","description":""},
                                    {"id":"OrderTime","type":"String","format":"datetime","description":""},
                                    {"id":"RIC","type":"String","format":"","description":""},
                                    {"id":"Side","type":"String","format":"","description":""},
                                    {"id":"AveragePrice","type":"Decimal","format":"0.0000","description":""},
                                    {"id":"OrderStatus","type":"String","format":"","description":""},
                                    {"id":"OrderQuantity","type":"Integer","format":"","description":""}
                                ],
                        "state":{
                                "code":200,"status":"Ok","stream":"Open","message":"queueSize=4000"
                            }
                    }

    mock_update = {
                        "streamID":"1",
                        "type":"Update",
                        "data":[
                                ["REDI_1601023761000-4948485052-48-50-83202102100|SBUX.OQ","2021-02-10T08:21:28.199","SBUX.OQ","Sell",None,"Pend",100]
                            ],
                        "update":[
                                    {"key":"REDI_1601023761000-4948485052-48-50-83202102100|SBUX.OQ","Side":"Buy"}
                                ],
                        "messages":[
                                    {"key":"REDI_1601023761000-4948485052-48-50-83202102100|SBUX.OQ",
                                    "events":[
                                            {"EventTime":"2021-02-10T08:21:28.199","OrderId":"REDI-1601023791-S20-10028202102100","EventType":"Replaced",
                                                "EventData":{"OrderQuantity":100,"LimitPrice":83.2000,"StopPrice":0.0000,"DestinationType":"Dma","AlgoId":0,"TimeInForce":"Day","LastCapacity":"Agency_A"
                                            }
                                        }
                                    ]
                                }
                            ],
                        "state":{
                                "code":200,"status":"Ok","stream":"Open","message":"queueSize=0"
                            }
                        }

    ############################################
    #   test

    trade_data_stream = rdp.TradeDataStream(session=session, 
                                                universe=['foo'],
                                                on_add=on_add_func,
                                                on_update=on_update_func,
                                                on_remove=on_remove_func,
                                                on_event=on_event_func,
                                                on_state=on_state_func,
                                                on_complete=on_complete_func,
                                            )

    trade_data_stream._TradeDataStream__on_response('bar', mock_response)
    assert len(trade_data_stream._order_summary_header_names) == 7
    assert len(trade_data_stream._order_summary_dict) == 0

    trade_data_stream._TradeDataStream__on_update('bar', mock_update)
    assert len(trade_data_stream._order_summary_header_names) == 7
    assert len(trade_data_stream._order_summary_dict) == 1
    assert len(trade_data_stream._order_key_to_event_list) == 1

    on_add_func.assert_called_once()
    on_update_func.assert_called_once()
    on_remove_func.assert_not_called()
    on_event_func.assert_called_once()
    on_complete_func.assert_called_once()


def test_trade_data_stream_on_update_message_case_4():
    ############################################
    #   prepare things

    session = MagicMock()
    #   callback
    on_add_func = MagicMock()
    on_update_func = MagicMock()
    on_remove_func = MagicMock()
    on_event_func = MagicMock()
    on_state_func = MagicMock()
    on_complete_func = MagicMock()

    mock_response = {"streamID":"1",
                        "type":"Response",
                        "headers":[
                                    {"id":"OrderKey","type":"String","format":"","description":""},
                                    {"id":"OrderTime","type":"String","format":"datetime","description":""},
                                    {"id":"RIC","type":"String","format":"","description":""},
                                    {"id":"Side","type":"String","format":"","description":""},
                                    {"id":"AveragePrice","type":"Decimal","format":"0.0000","description":""},
                                    {"id":"OrderStatus","type":"String","format":"","description":""},
                                    {"id":"OrderQuantity","type":"Integer","format":"","description":""}
                                ],
                        "state":{
                                "code":200,"status":"Ok","stream":"Open","message":"queueSize=4000"
                            }
                    }

    mock_update = {
                        "streamID":"1",
                        "type":"Update",
                        "data":[
                                ["REDI_1601023761000-4948485052-48-50-83202102100|SBUX.OQ","2021-02-10T08:21:28.199","SBUX.OQ","Sell",None,"Pend",100]
                            ],
                        "update":[
                                    {"key":"REDI_1601023761000-4948485052-48-50-83202102100|SBUX.OQ","Side":"Buy"}
                                ],
                        "messages":[
                                    {"key":"REDI_1601023761000-4948485052-48-50-83202102100|SBUX.OQ",
                                    "events":[
                                            {"EventTime":"2021-02-10T08:21:28.199","OrderId":"REDI-1601023791-S20-10028202102100","EventType":"Replaced",
                                                "EventData":{"OrderQuantity":100,"LimitPrice":83.2000,"StopPrice":0.0000,"DestinationType":"Dma","AlgoId":0,"TimeInForce":"Day","LastCapacity":"Agency_A"
                                            }
                                        }
                                    ]
                                }
                            ],
                        "state":{
                                "code":200,"status":"Ok","stream":"Open","message":"queueSize=10"
                            }
                        }

    ############################################
    #   test

    trade_data_stream = rdp.TradeDataStream(session=session, 
                                                universe=['foo'],
                                                on_add=on_add_func,
                                                on_update=on_update_func,
                                                on_remove=on_remove_func,
                                                on_event=on_event_func,
                                                on_state=on_state_func,
                                                on_complete=on_complete_func,
                                            )

    trade_data_stream._TradeDataStream__on_response('bar', mock_response)
    assert len(trade_data_stream._order_summary_header_names) == 7
    assert len(trade_data_stream._order_summary_dict) == 0

    trade_data_stream._TradeDataStream__on_update('bar', mock_update)
    assert len(trade_data_stream._order_summary_header_names) == 7
    assert len(trade_data_stream._order_summary_dict) == 1
    assert len(trade_data_stream._order_key_to_event_list) == 1

    on_add_func.assert_called_once()
    on_update_func.assert_called_once()
    on_remove_func.assert_not_called()
    on_event_func.assert_called_once()
    on_complete_func.assert_not_called()

def test_trade_data_stream_get_order_summary():
    ############################################
    #   prepare things

    session = MagicMock()

    mock_response = {"streamID":"1",
                        "type":"Response",
                        "headers":[
                                    {"id":"OrderKey","type":"String","format":"","description":""},
                                    {"id":"OrderTime","type":"String","format":"datetime","description":""},
                                    {"id":"RIC","type":"String","format":"","description":""},
                                    {"id":"Side","type":"String","format":"","description":""},
                                    {"id":"AveragePrice","type":"Decimal","format":"0.0000","description":""},
                                    {"id":"OrderStatus","type":"String","format":"","description":""},
                                    {"id":"OrderQuantity","type":"Integer","format":"","description":""}
                                ],
                        "state":{
                                "code":200,"status":"Ok","stream":"Open","message":"queueSize=0"
                            }
                    }

    mock_update = {
                        "streamID":"1",
                        "type":"Update",
                        "data":[
                                ["REDI_1601023761000-4948485052-48-50-83202102100|SBUX.OQ","2021-02-10T08:21:28.199","SBUX.OQ","Sell",None,"Pend",100]
                            ],
                        "update":[
                                    {"key":"REDI_1601023761000-4948485052-48-50-83202102100|SBUX.OQ","Side":"Buy",'OrderQuantity':1150}
                                ],
                        "messages":[
                                    {"key":"REDI_1601023761000-4948485052-48-50-83202102100|SBUX.OQ",
                                    "events":[
                                            {"EventTime":"2021-02-10T08:21:28.199","OrderId":"REDI-1601023791-S20-10028202102100","EventType":"Replaced",
                                                "EventData":{"OrderQuantity":100,"LimitPrice":83.2000,"StopPrice":0.0000,"DestinationType":"Dma","AlgoId":0,"TimeInForce":"Day","LastCapacity":"Agency_A"
                                            }
                                        }
                                    ]
                                }
                            ]
                        }

    ############################################
    #   test

    trade_data_stream = rdp.TradeDataStream(session=session, 
                                                universe=['foo'],
                                            )

    trade_data_stream._TradeDataStream__on_response('bar', mock_response)
    trade_data_stream._TradeDataStream__on_update('bar', mock_update)

    df = trade_data_stream.get_order_summary()
    assert df is not None
    assert df.shape[0] == 1

    df = trade_data_stream.get_order_summary(['SBUX.OQ',])
    assert df is not None
    assert df.shape[0] == 1
    assert df.iloc[0]['Side'] == 'Buy'
    assert df.iloc[0]['OrderQuantity'] == 1150
    
    df = trade_data_stream.get_order_summary(['foo',])
    assert df is not None
    assert df.shape[0] == 0

    df = trade_data_stream.get_order_summary(['foo',],
                                                end_datetime=datetime.datetime.now())
    assert df is not None
    assert df.shape[0] == 0

    df = trade_data_stream.get_order_summary(start_datetime=datetime.datetime.now())
    assert df is not None
    assert df.shape[0] == 0

    df = trade_data_stream.get_order_summary(end_datetime=datetime.datetime.now())
    assert df is not None
    assert df.shape[0] == 1

    df = trade_data_stream.get_order_summary(start_datetime=datetime.datetime.strptime('2021-02-10T08:21:28.199', '%Y-%m-%dT%H:%M:%S.%f'))
    assert df is not None
    assert df.shape[0] == 1

    df = trade_data_stream.get_order_summary(start_datetime=datetime.datetime.strptime('2021-02-10T08:21:28.199', '%Y-%m-%dT%H:%M:%S.%f'),
                                                end_datetime=datetime.datetime.now())
    assert df is not None
    assert df.shape[0] == 1

    df = trade_data_stream.get_order_summary(end_datetime=datetime.datetime.strptime('2021-02-10T08:21:28.199', '%Y-%m-%dT%H:%M:%S.%f'))
    assert df is not None
    assert df.shape[0] == 1

def test_trade_data_stream_get_order_events():
    ############################################
    #   prepare things

    session = MagicMock()

    mock_response = {"streamID":"1",
                        "type":"Response",
                        "headers":[
                                    {"id":"OrderKey","type":"String","format":"","description":""},
                                    {"id":"OrderTime","type":"String","format":"datetime","description":""},
                                    {"id":"RIC","type":"String","format":"","description":""},
                                    {"id":"Side","type":"String","format":"","description":""},
                                    {"id":"AveragePrice","type":"Decimal","format":"0.0000","description":""},
                                    {"id":"OrderStatus","type":"String","format":"","description":""},
                                    {"id":"OrderQuantity","type":"Integer","format":"","description":""}
                                ],
                        "state":{
                                "code":200,"status":"Ok","stream":"Open","message":"queueSize=0"
                            }
                    }

    mock_update = {
                        "streamID":"1",
                        "type":"Update",
                        "data":[
                                ["REDI_1601023761000-4948485052-48-50-83202102100|SBUX.OQ","2021-02-10T08:21:28.199","SBUX.OQ","Sell",None,"Pend",100]
                            ],
                        "update":[
                                    {"key":"REDI_1601023761000-4948485052-48-50-83202102100|SBUX.OQ","Side":"Buy",'OrderQuantity':1150}
                                ],
                        "messages":[
                                    {"key":"REDI_1601023761000-4948485052-48-50-83202102100|SBUX.OQ",
                                    "events":[
                                            {"EventTime":"2021-02-10T08:21:28.199","OrderId":"REDI-1601023791-S20-10028202102100","EventType":"Replaced",
                                                "EventData":{"OrderQuantity":100,"LimitPrice":83.2000,"StopPrice":0.0000,"DestinationType":"Dma","AlgoId":0,"TimeInForce":"Day","LastCapacity":"Agency_A"
                                            }
                                        }
                                    ]
                                }
                            ]
                        }

    ############################################
    #   test

    trade_data_stream = rdp.TradeDataStream(session=session, 
                                                universe=['foo'],
                                            )

    trade_data_stream._TradeDataStream__on_response('bar', mock_response)
    trade_data_stream._TradeDataStream__on_update('bar', mock_update)

    df = trade_data_stream.get_order_events()
    assert df is not None
    assert df.shape[0] == 1

    df = trade_data_stream.get_order_events(universe=['SBUX.OQ'])
    assert df is not None
    assert df.shape[0] == 1

    df = trade_data_stream.get_order_events(universe=['foo'])
    assert df is not None
    assert df.shape[0] == 0

    df = trade_data_stream.get_order_events(universe=['foo'],
                                               end_datetime=datetime.datetime.now() )
    assert df is not None
    assert df.shape[0] == 0

    df = trade_data_stream.get_order_events(end_datetime=datetime.datetime.now())
    assert df is not None
    assert df.shape[0] == 1

    df = trade_data_stream.get_order_events(start_datetime=datetime.datetime.strptime('2021-02-10T08:21:28.199', '%Y-%m-%dT%H:%M:%S.%f'))
    assert df is not None
    assert df.shape[0] == 1

    df = trade_data_stream.get_order_events(start_datetime=datetime.datetime.strptime('2021-02-10T08:21:28.199', '%Y-%m-%dT%H:%M:%S.%f'),
                                                end_datetime=datetime.datetime.now())
    assert df is not None
    assert df.shape[0] == 1




    

