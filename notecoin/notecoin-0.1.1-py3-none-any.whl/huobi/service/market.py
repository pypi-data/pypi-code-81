import time

from notecoin.huobi.connection.restapi_sync_client import RestApiSyncClient
from notecoin.huobi.connection.subscribe_client import SubscribeClient
from notecoin.huobi.connection.websocket_req_client import WebSocketReqClient
from notecoin.huobi.constant.system import HttpMethod
from notecoin.huobi.model.market import PriceDepth, Trade, MarketDetail, MbpReq, PriceDepthReq, TradeDetailReq, \
    TradeDetail, CandlestickEvent, Candlestick, MarketDetailEvent, MbpFullEvent, CandlestickReq, MarketDetailReq, \
    MbpIncreaseEvent, MarketDetailMerged, MarketTicker, PriceDepthBboEvent, PriceDepthBbo, PriceDepthEvent, \
    TradeDetailEvent
from notecoin.huobi.utils.channels import request_mbp_channel, kline_channel, market_detail_channel, mbp_full_channel, \
    mbp_increase_channel, price_depth_bbo_channel, price_depth_channel, trade_detail_channel
from notecoin.huobi.utils.channels_request import request_kline_channel, request_market_detail_channel, \
    request_price_depth_channel, request_trade_detail_channel
from notecoin.huobi.utils.json_parser import default_parse_list_dict, default_parse, default_parse_fill_directly


class MarketService(RestApiSyncClient):
    def __init__(self, *args, **kwargs):

        super(MarketService, self).__init__(*args, **kwargs)

    def get_candle_stick_service(self, params):
        channel = "/market/history/kline"

        def parse(dict_data):
            return default_parse_list_dict(dict_data.get("data", []), Candlestick)

        return self.request_process(HttpMethod.GET, channel, params, parse)

    def get_history_trade_service(self, params):
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

        return self.request_process(HttpMethod.GET, channel, params, parse)

    def get_market_detail_merged_service(self, params):
        channel = "/market/detail/merged"

        def parse(dict_data):
            tick = dict_data.get("tick", {})
            return default_parse_fill_directly(tick, MarketDetailMerged)

        return self.request_process(HttpMethod.GET, channel, params, parse)

    def get_market_detail_service(self, params):
        channel = "/market/detail"

        def parse(dict_data):
            tick = dict_data.get("tick", {})
            return default_parse(tick, MarketDetail)

        return self.request_process(HttpMethod.GET, channel, params, parse)

    def GetMarketTickersService(self, params):
        channel = "/market/tickers"

        def parse(dict_data):
            return default_parse_list_dict(dict_data.get("data", []), MarketTicker)

        return self.request_process(HttpMethod.GET, channel, params, parse)

    def GetMarketTradeService(self, params):
        channel = "/market/trade"

        def parse(dict_data):
            tick = dict_data.get("tick", {})
            data = tick.get("data", [])
            return default_parse_list_dict(data, Trade, [])

        return self.request_process(HttpMethod.GET, channel, params, parse)

    def GetPriceDepthService(self, params):
        channel = "/market/depth"

        def parse(dict_data):
            tick = dict_data.get("tick", {})
            return PriceDepth.json_parse(tick)

        return self.request_process(HttpMethod.GET, channel, params, parse)


class MarketServiceSocket(WebSocketReqClient):
    def __init__(self, *args, **kwargs):
        super(MarketServiceSocket, self).__init__(*args, **kwargs)

    def ReqCandleStickService(self, callback, error_handler, params):
        symbol_list = params["symbol_list"]
        interval = params["interval"]
        from_ts_second = params.get("from_ts_second", None)
        end_ts_second = params.get("end_ts_second", None)

        def subscription(connection):
            for symbol in symbol_list:
                connection.send(request_kline_channel(symbol, interval, from_ts_second, end_ts_second))
                time.sleep(0.01)

        def parse(dict_data):
            return default_parse(dict_data, CandlestickReq, Candlestick)

        self.execute_subscribe_v1(subscription,
                                  parse,
                                  callback,
                                  error_handler)

    def ReqMarketDetailService(self, callback, error_handler, params):
        symbol_list = params["symbol_list"]

        def subscription(connection):
            for symbol in symbol_list:
                connection.send(request_market_detail_channel(symbol))
                time.sleep(0.01)

        def parse(dict_data):
            return default_parse(dict_data, MarketDetailReq, MarketDetail)

        self.execute_subscribe_v1(subscription,
                                  parse,
                                  callback,
                                  error_handler)

    def ReqMbpService(self, callback, error_handler, params):
        symbol_list = params["symbol_list"]
        level = params["levels"]

        def subscription(connection):
            for symbol in symbol_list:
                connection.send(request_mbp_channel(symbol, level))
                time.sleep(0.01)

        def parse(dict_data):
            return MbpReq.json_parse(dict_data)

        self.execute_subscribe_mbp(subscription,
                                   parse,
                                   callback,
                                   error_handler)

    def ReqPriceDepthService(self, callback, error_handler, params):
        symbol_list = params["symbol_list"]
        step = params["step"]

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

        self.execute_subscribe_v1(subscription,
                                  parse,
                                  callback,
                                  error_handler)

    def ReqTradeDetailService(self, callback, error_handler, params):
        symbol_list = params["symbol_list"]

        def subscription(connection):
            for symbol in symbol_list:
                connection.send(request_trade_detail_channel(symbol))
                time.sleep(0.01)

        def parse(dict_data):
            return default_parse(dict_data, TradeDetailReq, TradeDetail)

        self.execute_subscribe_v1(subscription,
                                  parse,
                                  callback,
                                  error_handler)


class MarketSeriveSub(SubscribeClient):
    def __init__(self, *args, **kwargs):
        super(MarketSeriveSub, self).__init__(*args, **kwargs)

    def SubCandleStickService(self, callback, error_handler, params):
        symbol_list = params["symbol_list"]
        interval = params["interval"]

        def subscription(connection):
            for symbol in symbol_list:
                connection.send(kline_channel(symbol, interval))
                time.sleep(0.01)

        def parse(dict_data):
            return default_parse(dict_data, CandlestickEvent, Candlestick)

        self.execute_subscribe_v1(subscription,
                                  parse,
                                  callback,
                                  error_handler)

    def SubMarketDetailService(self, callback, error_handler, params):
        symbol_list = params["symbol_list"]

        def subscription(connection):
            for symbol in symbol_list:
                connection.send(market_detail_channel(symbol))
                time.sleep(0.01)

        def parse(dict_data):
            return default_parse(dict_data, MarketDetailEvent, MarketDetail)

        self.execute_subscribe_v1(subscription,
                                  parse,
                                  callback,
                                  error_handler)

    def SubMbpFullService(self, callback, error_handler, params):
        symbol_list = params["symbol_list"]
        level = params["levels"]

        def subscription(connection):
            for symbol in symbol_list:
                connection.send(mbp_full_channel(symbol, level))
                time.sleep(0.01)

        def parse(dict_data):
            return MbpFullEvent.json_parse(dict_data)

        self.execute_subscribe_v1(subscription,
                                  parse,
                                  callback,
                                  error_handler)

    def SubMbpIncreaseService(self, callback, error_handler, params):
        symbol_list = params["symbol_list"]
        level = params["levels"]

        def subscription(connection):
            for symbol in symbol_list:
                connection.send(mbp_increase_channel(symbol, level))
                time.sleep(0.01)

        def parse(dict_data):
            return MbpIncreaseEvent.json_parse(dict_data)

        self.execute_subscribe_mbp(subscription,
                                   parse,
                                   callback,
                                   error_handler)

    def SubPriceDepthBboService(self, callback, error_handler, params):
        symbol_list = params["symbol_list"]

        def subscription(connection):
            for symbol in symbol_list:
                connection.send(price_depth_bbo_channel(symbol))
                time.sleep(0.01)

        def parse(dict_data):
            return default_parse(dict_data, PriceDepthBboEvent, PriceDepthBbo)

        self.execute_subscribe_v1(subscription,
                                  parse,
                                  callback,
                                  error_handler)

    def SubPriceDepthService(self, callback, error_handler, params):
        symbol_list = params["symbol_list"]
        step = params["step"]

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

        self.execute_subscribe_v1(subscription,
                                  parse,
                                  callback,
                                  error_handler)

    def SubTradeDetailService(self, callback, error_handler, params):
        symbol_list = params["symbol_list"]

        def subscription(connection):
            for symbol in symbol_list:
                connection.send(trade_detail_channel(symbol))
                time.sleep(0.01)

        def parse(dict_data):
            tick = dict_data.get("tick", {})
            trade_detail_event = default_parse(tick, TradeDetailEvent, TradeDetail)
            trade_detail_event.ch = dict_data.get("ch", "")
            return trade_detail_event

        self.execute_subscribe_v1(subscription,
                                  parse,
                                  callback,
                                  error_handler)
