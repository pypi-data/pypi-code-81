# pylint: disable=useless-super-delegation

from joinnector.service.base_sdk_service import BaseSDKService


class NotificationService(BaseSDKService):
    def __init__(self, name):
        super().__init__(name)


notification_service = NotificationService("notification")
