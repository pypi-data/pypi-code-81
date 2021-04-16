import time

from notecoin.huobi.connection import (RestApiSyncClient, SubscribeClient,
                                       WebSocketReqClient)
from notecoin.huobi.constant.system import HttpMethod
from notecoin.huobi.model.market import (Candlestick, CandlestickEvent,
                                         CandlestickReq, MarketDetail,
                                         MarketDetailEvent, MarketDetailReq,
                                         MbpFullEvent, MbpIncreaseEvent,
                                         MbpReq, PriceDepth, PriceDepthBbo,
                                         PriceDepthBboEvent, PriceDepthEvent,
                                         PriceDepthReq, Trade, TradeDetail,
                                         TradeDetailEvent, TradeDetailReq)
from notecoin.huobi.utils.channels import (kline_channel,
                                           market_detail_channel,
                                           mbp_full_channel,
                                           mbp_increase_channel,
                                           price_depth_bbo_channel,
                                           price_depth_channel,
                                           request_mbp_channel,
                                           trade_detail_channel)
from notecoin.huobi.utils.channels_request import (
    request_kline_channel, request_market_detail_channel,
    request_price_depth_channel, request_trade_detail_channel)
from notecoin.huobi.utils.json_parser import (default_parse,
                                              default_parse_list_dict)


class MarketService(RestApiSyncClient):
    def __init__(self, *args, **kwargs):

        super(MarketService, self).__init__(*args, **kwargs)

    def get_candle_stick_service(self, params):
        channel = "/market/history/kline"
        return self.request_process(HttpMethod.GET, channel, params)

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

        return self.request_process(HttpMethod.GET, channel, params)

    def get_market_detail_merged_service(self, params):
        channel = "/market/detail/merged"
        return self.request_process(HttpMethod.GET, channel, params)

    def get_market_detail_service(self, params):
        channel = "/market/detail"
        return self.request_process(HttpMethod.GET, channel, params)

    def get_market_tickers_service(self, params):
        channel = "/market/tickers"
        return self.request_process(HttpMethod.GET, channel, params)

    def get_market_trade_service(self, params):
        channel = "/market/trade"
        return self.request_process(HttpMethod.GET, channel, params)

    def get_price_depth_service(self, params):
        channel = "/market/depth"
        return self.request_process(HttpMethod.GET, channel, params)


class MarketServiceSocket(WebSocketReqClient):
    def __init__(self, *args, **kwargs):
        super(MarketServiceSocket, self).__init__(*args, **kwargs)

    def req_candle_stick_service(self, callback, error_handler, params):
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

        self.execute_subscribe_v1(subscription, parse, callback, error_handler)

    def req_market_detail_service(self, callback, error_handler, params):
        symbol_list = params["symbol_list"]

        def subscription(connection):
            for symbol in symbol_list:
                connection.send(request_market_detail_channel(symbol))
                time.sleep(0.01)

        def parse(dict_data):
            return default_parse(dict_data, MarketDetailReq, MarketDetail)

        self.execute_subscribe_v1(subscription, parse, callback, error_handler)

    def req_mbp_service(self, callback, error_handler, params):
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

    def req_price_depth_service(self, callback, error_handler, params):
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

    def req_trade_detail_service(self, callback, error_handler, params):
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


class MarketServiceSub(SubscribeClient):
    def __init__(self, *args, **kwargs):
        super(MarketServiceSub, self).__init__(*args, **kwargs)

    def sub_candle_stick_service(self, callback, error_handler, params):
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

    def sub_market_detail_service(self, callback, error_handler, params):
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

    def sub_mbp_full_service(self, callback, error_handler, params):
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

    def sub_mbp_increase_service(self, callback, error_handler, params):
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

    def sub_price_depth_bbo_service(self, callback, error_handler, params):
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

    def sub_price_depth_service(self, callback, error_handler, params):
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

    def sub_trade_detail_service(self, callback, error_handler, params):
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
