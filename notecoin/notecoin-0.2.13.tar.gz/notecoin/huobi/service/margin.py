from notecoin.huobi.connection.restapi_sync_client import RestApiSyncClient
from notecoin.huobi.constant import *
from notecoin.huobi.constant.system import HttpMethod
from notecoin.huobi.model.account import Balance
from notecoin.huobi.model.margin import *
from notecoin.huobi.model.margin import (GeneralRepayLoanRecord,
                                         GeneralRepayLoanResult)
from notecoin.huobi.utils import *
from notecoin.huobi.utils.json_parser import (default_parse_data_as_long,
                                              default_parse_list_dict)


class GetCrossMarginAccountBalanceService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/cross-margin/accounts/balance"

        def parse(dict_data):
            return CrossMarginAccountBalance.json_parse(dict_data.get("data", {}))

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, channel, self.params, parse)


class GetCrossMarginLoanInfoService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/cross-margin/loan-info"

        def parse(dict_data):
            return default_parse_list_dict(dict_data.get("data", []), CrossMarginLoanInfo, [])

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, channel, self.params, parse)


class GetCrossMarginLoanOrdersService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/cross-margin/loan-orders"

        def parse(dict_data):
            data_list = dict_data.get("data", [])
            return default_parse_list_dict(data_list, LoanOrder, [])

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, channel, self.params, parse)


class GetGeneralRepaymentLoanRecordsService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):

        def get_channel():
            path = "/v2/account/repayment"
            return path

        def parse(dict_data):
            return default_parse_list_dict(dict_data.get("data", {}), GeneralRepayLoanRecord)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, get_channel(), self.params, parse)
        


class GetMarginAccountBalanceService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/margin/accounts/balance"

        def parse(dict_data):
            data_list = dict_data.get("data", [])
            account_balance_list = []
            if data_list and len(data_list):
                for row in data_list:
                    account_balance = default_parse(row, MarginAccountBalance, Balance)
                    account_balance_list.append(account_balance)
            return account_balance_list

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, channel, self.params, parse)


class GetMarginLoanInfoService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/margin/loan-info"

        def parse(dict_data):
            return MarginLoanInfo.json_parse(dict_data.get("data", []))

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, channel, self.params, parse)


class GetMarginLoanOrdersService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/margin/loan-orders"

        def parse(dict_data):
            data_list = dict_data.get("data", [])
            return default_parse_list_dict(data_list, LoanOrder, [])

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, channel, self.params, parse)


class PostCreateMarginOrderService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/margin/orders"

        def parse(dict_data):
            return default_parse_data_as_long(dict_data, None)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_SIGN, channel, self.params, parse)


class PostCrossMarginCreateLoanOrdersService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/cross-margin/orders"

        def parse(dict_data):
            return default_parse_data_as_long(dict_data, None)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_SIGN, channel, self.params, parse)


class PostCrossMarginLoanOrderRepayService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/cross-margin/orders/{order_id}/repay".format(order_id=self.params.get("order-id"))

        def parse(dict_data):
            return dict_data.get("status", None)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_SIGN, channel, self.params, parse)


class PostCrossMarginTransferInService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/cross-margin/transfer-in"

        def parse(dict_data):
            return default_parse_data_as_long(dict_data, None)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_SIGN, channel, self.params, parse)


class PostCrossMarginTransferOutService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/cross-margin/transfer-out"

        def parse(dict_data):
            transfer_id = default_parse_data_as_long(dict_data, None)
            return transfer_id

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_SIGN, channel, self.params, parse)


class PostGeneralRepayLoanService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):

        def get_channel():
            path = "/v2/account/repayment"
            return path

        def parse(dict_data):
            return default_parse_list_dict(dict_data.get("data", {}), GeneralRepayLoanResult)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_SIGN, get_channel(), self.params, parse)
        


class PostRepayMarginOrderService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        loan_id = self.params["loan_id"]

        def get_channel():
            path = "/v1/margin/orders/{}/repay"
            return path.format(loan_id)

        def parse(dict_data):
            return default_parse_data_as_long(dict_data, None)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_SIGN, get_channel(), self.params, parse)


class PostTransferInMarginService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/dw/transfer-in/margin"

        def parse(dict_data):
            return default_parse_data_as_long(dict_data, None)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_SIGN, channel, self.params, parse)


class PostTransferOutMarginService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/dw/transfer-out/margin"

        def parse(dict_data):
            return default_parse_data_as_long(dict_data, None)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_SIGN, channel, self.params, parse)
