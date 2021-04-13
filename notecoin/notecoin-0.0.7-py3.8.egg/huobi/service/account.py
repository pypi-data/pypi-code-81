from notecoin.huobi.connection.restapi_sync_client import RestApiSyncClient
from notecoin.huobi.connection.subscribe_client import SubscribeClient
from notecoin.huobi.connection.websocket_req_client import *
from notecoin.huobi.constant.system import HttpMethod
from notecoin.huobi.model.account import *
from notecoin.huobi.utils import *
from notecoin.huobi.utils.json_parser import default_parse_data_as_long


class GetAccountAssetValuationService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v2/account/asset-valuation"

        def parse(dict_data):
            data = dict_data.get("data", {})
            return default_parse(data, AccountAssetValuationResult, [])

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, channel, self.params, parse)


class GetAccountBalanceBySubUidService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        sub_uid = self.params["sub-uid"]

        def get_channel():
            path = "/v1/account/accounts/{}"
            return path.format(sub_uid)

        def parse(dict_data):
            data_list = dict_data.get("data", [])
            return AccountBalance.json_parse_list(data_list)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, get_channel(), self.params, parse)


class GetAccountHistoryService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/account/history"

        def parse(dict_data):
            response = dict()
            data_list = dict_data.get("data", [])
            response['data'] = default_parse_list_dict(data_list, AccountHistory, [])
            response['next_id'] = dict_data.get("next-id", 0)
            return response

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, channel, self.params, parse)


class GetAccountLedgerService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v2/account/ledger"

        def parse(dict_data):
            data_list = dict_data.get("data", [])
            return default_parse_list_dict(data_list, AccountLedger, [])

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, channel, self.params, parse)


class GetAccountPointService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v2/point/account"

        def parse(dict_data):
            data = dict_data.get("data", {})
            return default_parse(data, AccountPointResult, {})

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, channel, self.params, parse)


class GetAccountsService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/account/accounts"

        def parse(dict_data):
            data_list = dict_data.get("data", [])
            return default_parse_list_dict(data_list, Account, [])

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, channel, self.params, parse)


class GetAggregateSubUserBalanceService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/subuser/aggregate-balance"

        def parse(dict_data):
            data = dict_data.get("data", [])
            return default_parse_list_dict(data, Balance)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, channel, self.params, parse)


class GetBalanceService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        account_id = self.params["account-id"]

        def get_channel():
            path = "/v1/account/accounts/{}/balance"
            return path.format(account_id)

        def parse(dict_data):
            data = dict_data.get("data", {})
            balance_list = data.get("list", [])
            return default_parse_list_dict(balance_list, Balance, [])

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, get_channel(), self.params, parse)

    def get_request(self, **kwargs):
        account_id = self.params["account-id"]

        def get_channel():
            path = "/v1/account/accounts/{}/balance"
            return path.format(account_id)

        def parse(dict_data):
            data = dict_data.get("data", {})
            balance_list = data.get("list", [])
            return default_parse_list_dict(balance_list, Balance, [])

        return RestApiSyncClient(**kwargs).create_request(HttpMethod.GET_SIGN, get_channel(), self.params, parse)


class PostAccountTransferService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/account/transfer"

        def parse(dict_data):
            data = dict_data.get("data", {})
            return default_parse(data, AccountTransferResult, [])

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_SIGN, channel, self.params, parse)


class PostTransferBetweenFuturesAndProService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/futures/transfer"

        def parse(dict_data):
            return default_parse_data_as_long(dict_data, None)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_SIGN, channel, self.params, parse)


class PostPointTransferService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v2/point/transfer"

        def parse(dict_data):
            data = dict_data.get("data", {})
            return default_parse(data, AccountPointTransferResult, {})

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_SIGN, channel, self.params, parse)


class PostSubUidManagementService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v2/sub-user/management"

        def parse(dict_data):
            return default_parse_list_dict(dict_data.get("data", {}), SubUidManagement)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_SIGN, channel, self.params, parse)


class PostSubaccountTransferService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/subuser/transfer"

        def parse(dict_data):
            return default_parse_data_as_long(dict_data, None)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_SIGN, channel, self.params, parse)


class ReqAccountBalanceService:
    def __init__(self, params):
        self.params = params

    def subscribe(self, callback, error_handler, **kwargs):
        client_req_id = self.params["client_req_id"]

        def subscription(connection):
            connection.send(request_account_list_channel(client_req_id))

        def parse(dict_data):
            req_obj = AccountBalanceReq()
            req_obj.ts = dict_data.get("ts", 0)
            req_obj.topic = dict_data.get("topic", 0)
            req_obj.cid = dict_data.get("cid", 0)
            data_list = dict_data.get("data", [])
            req_obj.data = AccountBalance.json_parse_list(data_list)
            return req_obj

        WebSocketReqClient(**kwargs).execute_subscribe_v1(subscription,
                                                          parse,
                                                          callback,
                                                          error_handler,
                                                          is_trade=True)


class SubAccountUpdateV2Service:
    def __init__(self, params):
        self.params = params

    def subscribe(self, callback, error_handler, **kwargs):
        mode = self.params["mode"]

        def subscription(connection):
            connection.send(accounts_update_channel(mode))

        def parse(dict_data):
            account_change_event = AccountUpdateEvent()
            account_change_event.ch = dict_data.get("ch")
            data = dict_data.get("data", {})
            if data and len(data):
                account_change_event.data = default_parse_list_dict(data, AccountUpdate)

            return account_change_event

        SubscribeClient(**kwargs).execute_subscribe_v2(subscription,
                                                       parse,
                                                       callback,
                                                       error_handler,
                                                       is_trade=True)
