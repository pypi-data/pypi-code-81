# pylint: disable=useless-super-delegation

from joinnector.service.base_sdk_service import BaseSDKService


class SettingService(BaseSDKService):
    def __init__(self, name):
        super().__init__(name)


setting_service = SettingService("setting")
