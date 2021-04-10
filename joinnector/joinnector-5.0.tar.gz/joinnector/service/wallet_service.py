# pylint: disable=useless-super-delegation

from joinnector.service.base_sdk_service import BaseSDKService


class WalletService(BaseSDKService):
    def __init__(self, name):
        super().__init__(name)


wallet_service = WalletService("wallet")
