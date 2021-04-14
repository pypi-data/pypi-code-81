from notecoin.huobi.connection.restapi_sync_client import RestApiSyncClient
from notecoin.huobi.constant.system import HttpMethod
from notecoin.huobi.model.generic import *
from notecoin.huobi.utils import *
from notecoin.huobi.utils.json_parser import default_parse_data_as_long


class GetExchangeCurrenciesService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/common/currencys"

        def parse(dict_data):
            data_list = dict_data.get("data", [])
            return data_list if len(data_list) else []

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET, channel, self.params, parse)


class GetExchangeSymbolsService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/common/symbols"

        def parse(dict_data):
            data_list = dict_data.get("data", [])
            return default_parse_list_dict(data_list, Symbol, [])

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET, channel, self.params, parse)


class GetExchangeTimestampService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v1/common/timestamp"

        def parse(dict_data):
            return default_parse_data_as_long(dict_data, None)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET, channel, self.params, parse)


class GetMarketStatusService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v2/market-status"

        def parse(dict_data):
            return default_parse(dict_data.get("data", {}), MarketStatus)

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET, channel, self.params, parse)


class GetReferenceCurrenciesService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/v2/reference/currencies"

        def parse(dict_data):
            ret_list = []
            data_list = dict_data.get("data", [])
            if data_list and len(data_list):
                for reference_currency in data_list:
                    reference_currency_obj = default_parse(reference_currency, ReferenceCurrency, Chain)
                    ret_list.append(reference_currency_obj)
            return ret_list

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET, channel, self.params, parse)


class GetSystemStatusService:

    def __init__(self, params):
        self.params = params

    def request(self, **kwargs):
        channel = "/api/v2/summary.json"
        kwargs["url"] = "https://status.huobigroup.com"

        def parse(dict_data):
            return dict_data

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET, channel, self.params, parse)
