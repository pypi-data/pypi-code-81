from notecoin.huobi.connection.restapi_sync_client import RestApiSyncClient
from notecoin.huobi.constant.system import HttpMethod
from notecoin.huobi.model.subuser import *
from notecoin.huobi.model.subuser import TradeMarket
from notecoin.huobi.utils import *
from notecoin.huobi.utils.json_parser import default_parse_data_as_long


class GetUidService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v2/user/uid"

        def parse(dict_data):
            return default_parse_data_as_long(dict_data, None)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, channel, self.params, parse)


class GetUserApikeyInfoService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v2/user/api-key"

        def parse(dict_data):
            return default_parse_list_dict(dict_data.get("data", {}), UserApikeyInfo)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, channel, self.params, parse)


class PostSubuserCreationService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v2/sub-user/creation"

        def parse(dict_data):
            return default_parse_list_dict(dict_data.get("data", {}), SubuserCreation)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_SIGN, channel, self.params, parse)


class PostSetSubuserTransferability:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v2/sub-user/transferability"

        def parse(dict_data):
            return default_parse_list_dict(dict_data.get("data", {}), SubuserTransferability)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_SIGN, channel, self.params, parse)


class PostSubuserApikeyDeletionService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v2/sub-user/api-key-deletion"

        # {'code': 200, 'data': None, 'ok': True}
        def parse(dict_data):
            return dict_data

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_SIGN, channel, self.params, parse)


class PostSubuserApikeyGenerationService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v2/sub-user/api-key-generation"

        def parse(dict_data):
            return default_parse(dict_data.get("data", {}), SubuserApikeyGeneration)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_SIGN, channel, self.params, parse)


class PostSubuserApikeyModificationService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v2/sub-user/api-key-modification"

        def parse(dict_data):
            return default_parse(dict_data.get("data", {}), SubuserApikeyModification)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_SIGN, channel, self.params, parse)


class PostTradableMarketService:
    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v2/sub-user/tradable-market"

        def parse(dict_data):
            return default_parse_list_dict(dict_data.get("data", {}), TradeMarket)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_SIGN, channel, self.params, parse)
