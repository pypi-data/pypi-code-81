# pylint: disable=useless-super-delegation

from joinnector.service.base_sdk_service import BaseSDKService


class CurrencyService(BaseSDKService):
    def __init__(self, name):
        super().__init__(name)

    def get_by_currency_code(self, currency_code):
        return super().get_by("currency_code", currency_code)


currency_service = CurrencyService("currency")
