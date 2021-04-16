from notecoin.huobi.connection import (RestApiSyncClient, SubscribeClient,
                                       WebSocketReqClient)
from notecoin.huobi.model.account import *
from notecoin.huobi.utils import *


class GetAccountAssetValuationService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v2/account/asset-valuation"

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, channel, self.params)


class GetAccountBalanceBySubUidService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        sub_uid = self.params["sub-uid"]

        def get_channel():
            path = "/v1/account/accounts/{}"
            return path.format(sub_uid)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, get_channel(), self.params)


class GetAccountHistoryService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/account/history"

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, channel, self.params)


class GetAccountLedgerService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v2/account/ledger"

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, channel, self.params)


class GetAccountPointService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v2/point/account"

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, channel, self.params)


class GetAccountsService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/account/accounts"

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, channel, self.params)


class GetAggregateSubUserBalanceService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/subuser/aggregate-balance"

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, channel, self.params)


class GetBalanceService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        account_id = self.params["account-id"]

        def get_channel():
            path = "/v1/account/accounts/{}/balance"
            return path.format(account_id)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, get_channel(), self.params)

    def get_request(self, **kwargs):
        account_id = self.params["account-id"]

        def get_channel():
            path = "/v1/account/accounts/{}/balance"
            return path.format(account_id)

        return RestApiSyncClient(**kwargs).create_request(HttpMethod.GET_SIGN, get_channel(), self.params)


class PostAccountTransferService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/account/transfer"

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_SIGN, channel, self.params)


class PostTransferBetweenFuturesAndProService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/futures/transfer"

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_SIGN, channel, self.params)


class PostPointTransferService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v2/point/transfer"

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_SIGN, channel, self.params)


class PostSubUidManagementService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v2/sub-user/management"

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_SIGN, channel, self.params)


class PostSubaccountTransferService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/subuser/transfer"

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_SIGN, channel, self.params)


class ReqAccountBalanceService:
    def __init__(self, params):
        self.params = params

    def subscribe(self, callback, error_handler, **kwargs):
        client_req_id = self.params["client_req_id"]

        def subscription(connection):
            connection.send(request_account_list_channel(client_req_id))

        WebSocketReqClient(**kwargs).execute_subscribe_v1(subscription, callback, error_handler, is_trade=True)


class SubAccountUpdateV2Service:
    def __init__(self, params):
        self.params = params

    def subscribe(self, callback, error_handler, **kwargs):
        mode = self.params["mode"]

        def subscription(connection):
            connection.send(accounts_update_channel(mode))

        SubscribeClient(**kwargs).execute_subscribe_v2(subscription, callback, error_handler, is_trade=True)
