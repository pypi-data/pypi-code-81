from notecoin.huobi.utils.json_parser import default_parse_fill_directly
from notecoin.huobi.connection.restapi_sync_client import RestApiSyncClient
from notecoin.huobi.constant import *
from notecoin.huobi.model.algo import *
from notecoin.huobi.utils.json_parser import *


class GetOpenOrdersService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v2/algo-orders/opening"

        # {
        #     "code": 200,
        #     "data": [
        #         {
        #             "accountId": 3684354,
        #             "clientOrderId": "test004",
        #             "lastActTime": 1600141535221,
        #             "orderOrigTime": 1600141535137,
        #             "orderPrice": "0.08",
        #             "orderSide": "buy",
        #             "orderSize": "65",
        #             "orderStatus": "created",
        #             "orderType": "limit",
        #             "source": "api",
        #             "stopPrice": "0.085",
        #             "symbol": "adausdt",
        #             "trailingRate": 0.001,
        #             "timeInForce": "gtc"
        #         }
        #     ]
        # }

        def parse(dict_data):
            data = dict_data.get("data", {})
            return default_parse_list_dict(data, OrderListItem)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, channel, self.params, parse)


class GetOrderByClientOrderIdService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v2/algo-orders/specific"

        def parse(dict_data):
            data = dict_data.get("data", {})
            return default_parse(data, OrderHistoryItem)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, channel, self.params, parse)


class GetOrderHistoryService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v2/algo-orders/history"

        def parse(dict_data):
            data = dict_data.get("data", {})
            return default_parse_list_dict(data, OrderHistoryItem)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, channel, self.params, parse)


class PostCancelOrderService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v2/algo-orders/cancellation"

        # {'code': 200, 'data': {'accepted': [], 'rejected': ['test001', 'test002']}}
        def parse(dict_data):
            data = dict_data.get("data", {})
            return default_parse_fill_directly(data, CancelOrderResult)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_SIGN, channel, self.params, parse)


class PostCreateOrderService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v2/algo-orders"

        # {'code': 200, 'data': {'clientOrderId': 'test001'}}
        def parse(dict_data):
            data = dict_data.get('data')
            return data.get('clientOrderId')

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_SIGN, channel, self.params, parse)
