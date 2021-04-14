from notecoin.huobi.connection.restapi_sync_client import RestApiSyncClient
from notecoin.huobi.constant.system import HttpMethod
from notecoin.huobi.model.etf import *
from notecoin.huobi.utils import *


class GetEtfSwapConfigService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/etf/swap/config"

        def parse(dict_data):
            data_info = dict_data.get("data", {})
            return default_parse(data_info, EtfSwapConfig, UnitPrice)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET, channel, self.params, parse)


class GetEtfSwapListService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/etf/swap/list"

        def parse(dict_data):
            return EtfSwapList.json_parse_list(dict_data.get("data", []))

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET_SIGN, channel, self.params, parse)


class PostEftSwapInService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/etf/swap/in"

        def parse(dict_data):
            return default_parse_fill_directly(dict_data, EtfSwapInOut)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_SIGN, channel, self.params, parse)


class PostEtfSwapOutService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/etf/swap/out"

        def parse(dict_data):
            return default_parse_fill_directly(dict_data, EtfSwapInOut)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_SIGN, channel, self.params, parse)
