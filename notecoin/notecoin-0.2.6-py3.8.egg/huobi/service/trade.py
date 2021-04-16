import time

from notecoin.huobi.connection.restapi_sync_client import RestApiSyncClient
from notecoin.huobi.connection.subscribe_client import SubscribeClient
from notecoin.huobi.connection.websocket_req_client import *
from notecoin.huobi.constant import *
from notecoin.huobi.constant.system import HttpMethod
from notecoin.huobi.model.trade import *
from notecoin.huobi.model.trade.batch_create_order import BatchCreateOrder
from notecoin.huobi.utils import *
from notecoin.huobi.utils.json_parser import default_parse_data_as_long


class GetFeeRateService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/fee/fee-rate/get"

        def parse(dict_data):
            data_list = dict_data.get("data", [])
            return default_parse_list_dict(data_list, FeeRate, [])

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, channel, self.params, parse)


class GetHistoryOrdersService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/order/history"

        def parse(dict_data):
            data_list = dict_data.get("data", [])
            return Order.json_parse_list(data_list)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, channel, self.params, parse)


class GetMatchResultsByOrderIdService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        order_id = self.params["order_id"]

        def get_channel():
            path = "/v1/order/orders/{}/matchresults"
            return path.format(order_id)

        def parse(dict_data):
            data_list = dict_data.get("data", [])
            return default_parse_list_dict(data_list, MatchResult, [])

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, get_channel(), self.params, parse)


class GetMatchResultsService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/order/matchresults"

        def parse(dict_data):
            data_list = dict_data.get("data", [])
            return default_parse_list_dict(data_list, MatchResult, [])

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, channel, self.params, parse)


class GetOpenOrdersService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/order/openOrders"

        def parse(dict_data):
            data_list = dict_data.get("data", [])
            return Order.json_parse_list(data_list)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, channel, self.params, parse)


class GetOrderByClientOrderIdService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/order/orders/getClientOrder"

        def parse(dict_data):
            data_dict = dict_data.get("data", {})
            return Order.json_parse(data_dict)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, channel, self.params, parse)


class GetOrderByIdService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        order_id = self.params["order_id"]

        def get_channel():
            path = "/v1/order/orders/{}"
            return path.format(order_id)

        def parse(dict_data):
            data_dict = dict_data.get("data")
            return Order.json_parse(data_dict)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, get_channel(), self.params, parse)


class GetOrdersService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/order/orders"

        def parse(dict_data):
            data_list = dict_data.get("data", [])
            return Order.json_parse_list(data_list)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, channel, self.params, parse)


class GetTransactFeeRateService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v2/reference/transact-fee-rate"

        def parse(dict_data):
            data_list = dict_data.get("data", [])
            return default_parse_list_dict(data_list, TransactFeeRate, [])

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, channel, self.params, parse)


class PostBatchCancelOpenOrderService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/order/orders/batchCancelOpenOrders"

        def parse(dict_data):
            data = dict_data.get("data", {})
            return default_parse(data, BatchCancelCount)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_SIGN, channel, self.params, parse)


class PostBatchCancelOrderService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/order/orders/batchcancel"

        def parse(dict_data):
            data = dict_data.get("data", {})
            return default_parse_fill_directly(data, BatchCancelResult)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_SIGN, channel, self.params, parse)


class PostBatchCreateOrderService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/order/batch-orders"

        def parse(dict_data):
            data = dict_data.get("data", [])
            return default_parse_list_dict(data, BatchCreateOrder, [])

        return RestApiSyncClient(**kwargs).request_process_post_batch(HttpMethod.POST_SIGN, channel, self.params, parse)


class PostCancelClientOrderService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/order/orders/submitCancelClientOrder"

        def parse(dict_data):
            return default_parse_data_as_long(dict_data, None)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_SIGN, channel, self.params, parse)


class PostCancelOrderService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        order_id = self.params["order_id"]

        def get_channel():
            path = "/v1/order/orders/{}/submitcancel"
            return path.format(order_id)

        def parse(dict_data):
            return default_parse_data_as_long(dict_data, None)
        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_SIGN, get_channel(), self.params, parse)


class PostCreateOrderService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/order/orders/place"

        def parse(dict_data):
            return default_parse_data_as_long(dict_data, None)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_SIGN, channel, self.params, parse)


class PostTransferFuturesProService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/futures/transfer"

        def parse(dict_data):
            return default_parse_data_as_long(dict_data, None)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_SIGN, channel, self.params, parse)


class ReqOrderDetailService:
    def __init__(self, params):
        self.params = params

    def subscribe(self, callback, error_handler, **kwargs):
        order_id = self.params["order-id"]
        client_req_id = self.params["cid"]

        def subscription(connection):
            connection.send(request_order_detail_channel(order_id, client_req_id))

        def parse(dict_data):
            order_update_event = default_parse(dict_data, OrderDetailReq, OrderListItem)

            return order_update_event

        WebSocketReqClient(**kwargs).execute_subscribe_v1(subscription,
                                                          parse,
                                                          callback,
                                                          error_handler,
                                                          is_trade=True)


class ReqOrderListService:
    def __init__(self, params):
        self.params = params

    def subscribe(self, callback, error_handler, **kwargs):
        symbol = self.params["symbol"]
        account_id = self.params["account-id"]
        order_states = self.params["states"]
        client_req_id = self.params["client-req-id"]

        def subscription(connection):
            connection.send(request_order_list_channel(symbol=symbol, account_id=account_id,
                            states_str=order_states, client_req_id=client_req_id, more_key=self.params))

        def parse(dict_data):
            order_update_event = default_parse(dict_data, OrderListReq, OrderListItem)

            return order_update_event

        WebSocketReqClient(**kwargs).execute_subscribe_v1(subscription,
                                                          parse,
                                                          callback,
                                                          error_handler,
                                                          is_trade=True)


class SubOrderUpdateV2Service:
    def __init__(self, params):
        self.params = params

    def subscribe(self, callback, error_handler, **kwargs):
        symbol_list = self.params["symbol_list"]

        def subscription(connection):
            for val in symbol_list:
                connection.send(orders_update_channel(val))
                time.sleep(0.01)

        def parse(dict_data):
            return default_parse(dict_data, OrderUpdateEvent, OrderUpdate)

        SubscribeClient(**kwargs).execute_subscribe_v2(subscription,
                                                       parse,
                                                       callback,
                                                       error_handler,
                                                       is_trade=True)


class SubTradeClearingV2Service:
    def __init__(self, params):
        self.params = params

    def subscribe(self, callback, error_handler, **kwargs):
        symbol_list = self.params["symbol_list"]

        def subscription(connection):
            for symbol in symbol_list:
                connection.send(trade_clearing_channel(symbol))
                time.sleep(0.01)

        def parse(dict_data):
            return TradeClearingEvent.json_parse(dict_data)

        SubscribeClient(**kwargs).execute_subscribe_v2(subscription,
                                                       parse,
                                                       callback,
                                                       error_handler,
                                                       is_trade=True)
