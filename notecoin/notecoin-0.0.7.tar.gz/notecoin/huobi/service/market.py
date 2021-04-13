import time

from notecoin.huobi.connection.restapi_sync_client import RestApiSyncClient
from notecoin.huobi.connection.subscribe_client import SubscribeClient
from notecoin.huobi.connection.websocket_req_client import *
from notecoin.huobi.connection.websocket_req_client import WebSocketReqClient
from notecoin.huobi.constant.system import HttpMethod
from notecoin.huobi.model.market import *
from notecoin.huobi.model.market import PriceDepth
from notecoin.huobi.utils import *
from notecoin.huobi.utils.channels_request import *


class GetCandleStickService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/market/history/kline"

        def parse(dict_data):
            return default_parse_list_dict(dict_data.get("data", []), Candlestick)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET, channel, self.params, parse)


class GetHistoryTradeService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/market/history/trade"

        def parse(dict_data):
            trade_list_ret = []  # two level list, list item is list too
            data_list_outer = dict_data.get("data", [])
            if len(data_list_outer):
                for row in data_list_outer:
                    data_list_inner = row.get("data", [])
                    if len(data_list_inner):
                        for trade_info in data_list_inner:
                            trade_obj = default_parse_list_dict(trade_info, Trade, None)  # return a list
                            if trade_obj:
                                trade_list_ret.append(trade_obj)

            return trade_list_ret

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET, channel, self.params, parse)


class GetMarketDetailMergedService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/market/detail/merged"

        def parse(dict_data):
            tick = dict_data.get("tick", {})
            return default_parse_fill_directly(tick, MarketDetailMerged)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET, channel, self.params, parse)


class GetMarketDetailService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/market/detail"

        def parse(dict_data):
            tick = dict_data.get("tick", {})
            return default_parse(tick, MarketDetail)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET, channel, self.params, parse)


class GetMarketTickersService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/market/tickers"

        def parse(dict_data):
            return default_parse_list_dict(dict_data.get("data", []), MarketTicker)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET, channel, self.params, parse)


class GetMarketTradeService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/market/trade"

        def parse(dict_data):
            tick = dict_data.get("tick", {})
            data = tick.get("data", [])
            return default_parse_list_dict(data, Trade, [])

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET, channel, self.params, parse)


class GetPriceDepthService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/market/depth"

        def parse(dict_data):
            tick = dict_data.get("tick", {})
            return PriceDepth.json_parse(tick)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET, channel, self.params, parse)


class ReqCandleStickService:
    def __init__(self, params):
        self.params = params

    def subscribe(self, callback, error_handler, **kwargs):
        symbol_list = self.params["symbol_list"]
        interval = self.params["interval"]
        from_ts_second = self.params.get("from_ts_second", None)
        end_ts_second = self.params.get("end_ts_second", None)

        def subscription(connection):
            for symbol in symbol_list:
                connection.send(request_kline_channel(symbol, interval, from_ts_second, end_ts_second))
                time.sleep(0.01)

        def parse(dict_data):
            return default_parse(dict_data, CandlestickReq, Candlestick)

        WebSocketReqClient(**kwargs).execute_subscribe_v1(subscription,
                                                          parse,
                                                          callback,
                                                          error_handler)


class ReqMarketDetailService:
    def __init__(self, params):
        self.params = params

    def subscribe(self, callback, error_handler, **kwargs):
        symbol_list = self.params["symbol_list"]

        def subscription(connection):
            for symbol in symbol_list:
                connection.send(request_market_detail_channel(symbol))
                time.sleep(0.01)

        def parse(dict_data):
            return default_parse(dict_data, MarketDetailReq, MarketDetail)

        WebSocketReqClient(**kwargs).execute_subscribe_v1(subscription,
                                                          parse,
                                                          callback,
                                                          error_handler)


class ReqMbpService:
    def __init__(self, params):
        self.params = params

    def subscribe(self, callback, error_handler, **kwargs):
        symbol_list = self.params["symbol_list"]
        level = self.params["levels"]

        def subscription(connection):
            for symbol in symbol_list:
                connection.send(request_mbp_channel(symbol, level))
                time.sleep(0.01)

        def parse(dict_data):
            return MbpReq.json_parse(dict_data)

        WebSocketReqClient(**kwargs).execute_subscribe_mbp(subscription,
                                                           parse,
                                                           callback,
                                                           error_handler)


class ReqPriceDepthService:
    def __init__(self, params):
        self.params = params

    def subscribe(self, callback, error_handler, **kwargs):
        symbol_list = self.params["symbol_list"]
        step = self.params["step"]

        def subscription(connection):
            for symbol in symbol_list:
                connection.send(request_price_depth_channel(symbol, step))
                time.sleep(0.01)

        def parse(dict_data):
            price_depth_event = PriceDepthReq()
            price_depth_event.id = dict_data.get("id")
            price_depth_event.rep = dict_data.get("rep")
            data = dict_data.get("data", {})
            price_depth_obj = PriceDepth.json_parse(data)
            price_depth_event.data = price_depth_obj
            return price_depth_event

        WebSocketReqClient(**kwargs).execute_subscribe_v1(subscription,
                                                          parse,
                                                          callback,
                                                          error_handler)


class ReqTradeDetailService:
    def __init__(self, params):
        self.params = params

    def subscribe(self, callback, error_handler, **kwargs):
        symbol_list = self.params["symbol_list"]

        def subscription(connection):
            for symbol in symbol_list:
                connection.send(request_trade_detail_channel(symbol))
                time.sleep(0.01)

        def parse(dict_data):
            return default_parse(dict_data, TradeDetailReq, TradeDetail)

        WebSocketReqClient(**kwargs).execute_subscribe_v1(subscription,
                                                          parse,
                                                          callback,
                                                          error_handler)


class SubCandleStickService:
    def __init__(self, params):

        self.params = params

    def subscribe(self, callback, error_handler, **kwargs):
        symbol_list = self.params["symbol_list"]
        interval = self.params["interval"]

        def subscription(connection):
            for symbol in symbol_list:
                connection.send(kline_channel(symbol, interval))
                time.sleep(0.01)

        def parse(dict_data):
            return default_parse(dict_data, CandlestickEvent, Candlestick)

        SubscribeClient(**kwargs).execute_subscribe_v1(subscription,
                                                       parse,
                                                       callback,
                                                       error_handler)


class SubMarketDetailService:
    def __init__(self, params):
        self.params = params

    def subscribe(self, callback, error_handler, **kwargs):
        symbol_list = self.params["symbol_list"]

        def subscription(connection):
            for symbol in symbol_list:
                connection.send(market_detail_channel(symbol))
                time.sleep(0.01)

        def parse(dict_data):
            return default_parse(dict_data, MarketDetailEvent, MarketDetail)

        SubscribeClient(**kwargs).execute_subscribe_v1(subscription,
                                                       parse,
                                                       callback,
                                                       error_handler)


class SubMbpFullService:
    def __init__(self, params):
        self.params = params

    def subscribe(self, callback, error_handler, **kwargs):
        symbol_list = self.params["symbol_list"]
        level = self.params["levels"]

        def subscription(connection):
            for symbol in symbol_list:
                connection.send(mbp_full_channel(symbol, level))
                time.sleep(0.01)

        def parse(dict_data):
            return MbpFullEvent.json_parse(dict_data)

        SubscribeClient(**kwargs).execute_subscribe_v1(subscription,
                                                       parse,
                                                       callback,
                                                       error_handler)


class SubMbpIncreaseService:
    def __init__(self, params):
        self.params = params

    def subscribe(self, callback, error_handler, **kwargs):
        symbol_list = self.params["symbol_list"]
        level = self.params["levels"]

        def subscription(connection):
            for symbol in symbol_list:
                connection.send(mbp_increase_channel(symbol, level))
                time.sleep(0.01)

        def parse(dict_data):
            return MbpIncreaseEvent.json_parse(dict_data)

        SubscribeClient(**kwargs).execute_subscribe_mbp(subscription,
                                                        parse,
                                                        callback,
                                                        error_handler)


class SubPriceDepthBboService:
    def __init__(self, params):
        self.params = params

    def subscribe(self, callback, error_handler, **kwargs):
        symbol_list = self.params["symbol_list"]

        def subscription(connection):
            for symbol in symbol_list:
                connection.send(price_depth_bbo_channel(symbol))
                time.sleep(0.01)

        def parse(dict_data):
            return default_parse(dict_data, PriceDepthBboEvent, PriceDepthBbo)

        SubscribeClient(**kwargs).execute_subscribe_v1(subscription,
                                                       parse,
                                                       callback,
                                                       error_handler)


class SubPriceDepthService:
    def __init__(self, params):
        self.params = params

    def subscribe(self, callback, error_handler, **kwargs):
        symbol_list = self.params["symbol_list"]
        step = self.params["step"]

        def subscription(connection):
            for symbol in symbol_list:
                connection.send(price_depth_channel(symbol, step))
                time.sleep(0.01)

        def parse(dict_data):
            price_depth_event_obj = PriceDepthEvent()
            price_depth_event_obj.ch = dict_data.get("ch", "")
            tick = dict_data.get("tick", "")
            price_depth_event_obj.tick = PriceDepth.json_parse(tick)
            return price_depth_event_obj

        SubscribeClient(**kwargs).execute_subscribe_v1(subscription,
                                                       parse,
                                                       callback,
                                                       error_handler)


class SubTradeDetailService:
    def __init__(self, params):
        self.params = params

    def subscribe(self, callback, error_handler, **kwargs):
        symbol_list = self.params["symbol_list"]

        def subscription(connection):
            for symbol in symbol_list:
                connection.send(trade_detail_channel(symbol))
                time.sleep(0.01)

        def parse(dict_data):
            tick = dict_data.get("tick", {})
            trade_detail_event = default_parse(tick, TradeDetailEvent, TradeDetail)
            trade_detail_event.ch = dict_data.get("ch", "")
            return trade_detail_event

        SubscribeClient(**kwargs).execute_subscribe_v1(subscription,
                                                       parse,
                                                       callback,
                                                       error_handler)
