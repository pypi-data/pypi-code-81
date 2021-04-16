import time

from notecoin.huobi.connection import RestApiSyncClient, WebSocketReqClient, SubscribeClient
from notecoin.huobi.constant import HttpMethod
from notecoin.huobi.utils import request_order_detail_channel, orders_update_channel, trade_clearing_channel, \
    request_order_list_channel


class TradeService(RestApiSyncClient):

    def __init__(self, *args, **kwargs):
        super(TradeService, self).__init__(*args, **kwargs)

    def get_fee_rate_service(self, params):
        channel = "/v1/fee/fee-rate/get"

        return self.request_process(HttpMethod.GET_SIGN, channel, params)

    def get_history_orders_service(self, params):
        channel = "/v1/order/history"

        return self.request_process(HttpMethod.GET_SIGN, channel, params)

    def get_match_results_by_order_id_service(self, params):
        order_id = params["order_id"]

        def get_channel():
            path = "/v1/order/orders/{}/matchresults"
            return path.format(order_id)

        return self.request_process(HttpMethod.GET_SIGN, get_channel(), params)

    def get_match_results_service(self, params):
        channel = "/v1/order/matchresults"

        return self.request_process(HttpMethod.GET_SIGN, channel, params)

    def get_open_orders_service(self, params):
        channel = "/v1/order/openOrders"

        return self.request_process(HttpMethod.GET_SIGN, channel, params)

    def get_order_by_client_order_id_service(self, params):
        channel = "/v1/order/orders/getClientOrder"
        return self.request_process(HttpMethod.GET_SIGN, channel, params)

    def get_order_by_id_service(self, params):
        order_id = params["order_id"]

        def get_channel():
            path = "/v1/order/orders/{}"
            return path.format(order_id)

        return self.request_process(HttpMethod.GET_SIGN, get_channel(), params)

    def get_orders_service(self, params):
        channel = "/v1/order/orders"

        return self.request_process(HttpMethod.GET_SIGN, channel, params)

    def get_transact_fee_rate_service(self, params):
        channel = "/v2/reference/transact-fee-rate"

        return self.request_process(HttpMethod.GET_SIGN, channel, params)

    def post_batch_cancel_open_order_service(self, params):
        channel = "/v1/order/orders/batchCancelOpenOrders"

        return self.request_process(HttpMethod.POST_SIGN, channel, params)

    def post_batch_cancel_order_service(self, params):
        channel = "/v1/order/orders/batchcancel"
        return self.request_process(HttpMethod.POST_SIGN, channel, params)

    def post_batch_create_order_service(self, params):
        channel = "/v1/order/batch-orders"

        return self.request_process_post_batch(HttpMethod.POST_SIGN, channel, params)

    def post_cancel_client_order_service(self, params):
        channel = "/v1/order/orders/submitCancelClientOrder"

        return self.request_process(HttpMethod.POST_SIGN, channel, params)

    def post_cancel_order_service(self, params):
        order_id = params["order_id"]

        def get_channel():
            path = "/v1/order/orders/{}/submitcancel"
            return path.format(order_id)

        return self.request_process(HttpMethod.POST_SIGN, get_channel(), params)

    def post_create_order_service(self, params):
        channel = "/v1/order/orders/place"

        return self.request_process(HttpMethod.POST_SIGN, channel, params)

    def post_transfer_futures_pro_service(self, params):
        channel = "/v1/futures/transfer"

        return self.request_process(HttpMethod.POST_SIGN, channel, params)


class TRadeServiceSocket(WebSocketReqClient):

    def __init__(self, *args, **kwargs):
        super(TRadeServiceSocket, self).__init__(*args, **kwargs)

    def req_order_detail_service(self, callback, error_handler, params):
        order_id = params["order-id"]
        client_req_id = params["cid"]

        def subscription(connection):
            connection.send(request_order_detail_channel(order_id, client_req_id))

        self.execute_subscribe_v1(subscription,
                                  callback,
                                  error_handler,
                                  is_trade=True)

    def req_order_list_service(self, callback, error_handler, params):
        symbol = params["symbol"]
        account_id = params["account-id"]
        order_states = params["states"]
        client_req_id = params["client-req-id"]

        def subscription(connection):
            connection.send(request_order_list_channel(symbol=symbol, account_id=account_id,
                                                       states_str=order_states, client_req_id=client_req_id,
                                                       more_key=params))

        self.execute_subscribe_v1(subscription, callback, error_handler, is_trade=True)


class TRadeServiceSocketSub(SubscribeClient):
    def __init__(self, *args, **kwargs):
        super(TRadeServiceSocketSub, self).__init__(*args, **kwargs)

    def sub_order_update_v2_service(self, callback, error_handler, params):
        symbol_list = params["symbol_list"]

        def subscription(connection):
            for val in symbol_list:
                connection.send(orders_update_channel(val))
                time.sleep(0.01)

        self.execute_subscribe_v2(subscription, callback, error_handler, is_trade=True)

    def sub_trade_clearing_v2_service(self, callback, error_handler, params):
        symbol_list = params["symbol_list"]

        def subscription(connection):
            for symbol in symbol_list:
                connection.send(trade_clearing_channel(symbol))
                time.sleep(0.01)

        self.execute_subscribe_v2(subscription, callback, error_handler, is_trade=True)
