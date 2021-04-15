from notecoin.huobi.connection.restapi_sync_client import RestApiSyncClient
from notecoin.huobi.constant import *
from notecoin.huobi.model.trade import *
from notecoin.huobi.model.wallet import *
from notecoin.huobi.utils import *
from notecoin.huobi.utils.json_parser import default_parse_data_as_long


class GetAccountDepositAddressService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v2/account/deposit/address"

        def parse(dict_data):
            data_list = dict_data.get("data", [])
            return default_parse_list_dict(data_list, ChainDepositAddress)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, channel, self.params, parse)


class GetAccountWithdrawAddressService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v2/account/withdraw/address"

        def parse(dict_data):
            data_list = dict_data.get("data", [])
            return default_parse_list_dict(data_list, ChainWithdrawAddress)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, channel, self.params, parse)


class GetAccountWithdrawQuotaService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v2/account/withdraw/quota"

        def parse(dict_data):
            data = dict_data.get("data", {})
            chains = data.get("chains", [])
            return default_parse_list_dict(chains, WithdrawQuota)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, channel, self.params, parse)


class GetDepositWithdrawService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/query/deposit-withdraw"

        def parse(dict_data):
            op_type = self.params["type"]
            data_list = dict_data.get("data", [])
            if op_type == DepositWithdraw.DEPOSIT:
                return default_parse_list_dict(data_list, Deposit)
            elif op_type == DepositWithdraw.WITHDRAW:
                return default_parse_list_dict(data_list, Withdraw)
            return []

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, channel, self.params, parse)


class GetSubUserDepositAddressService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v2/sub-user/deposit-address"

        def parse(dict_data):
            json_data_list = dict_data.get("data", [])
            return default_parse_list_dict(json_data_list, ChainDepositAddress, [])

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, channel, self.params, parse)


class GetSubUserDepositHistoryService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v2/sub-user/query-deposit"

        def parse(dict_data):
            deposit_history = DepositHistory()
            deposit_history.nextId = dict_data.get("nextId", 0)
            json_data_list = dict_data.get("data", [])
            deposit_history_item_list = default_parse_list_dict(json_data_list, DepositHistoryItem)
            deposit_history.data = deposit_history_item_list
            return deposit_history

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, channel, self.params, parse)


class PostCancelWithdrawService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        withdraw_id_params = self.params["withdraw-id"]

        def get_channel():
            path = "/v1/dw/withdraw-virtual/{}/cancel"
            return path.format(withdraw_id_params)

        def parse(dict_data):
            return default_parse_data_as_long(dict_data, None)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_SIGN, get_channel(), self.params, parse)


class PostCreateWithdrawService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/dw/withdraw/api/create"

        def parse(dict_data):
            # return dict_data.get("data", 0)
            return default_parse_data_as_long(dict_data, None)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_SIGN, channel, self.params, parse)
