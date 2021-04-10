# pylint: disable=useless-super-delegation

from joinnector.service.base_sdk_service import BaseSDKService


class WalletTransactionService(BaseSDKService):
    def __init__(self, name):
        super().__init__(name)


wallettransaction_service = WalletTransactionService("wallettransaction")
