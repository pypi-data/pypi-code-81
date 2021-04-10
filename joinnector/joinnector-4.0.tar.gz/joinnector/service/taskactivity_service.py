# pylint: disable=useless-super-delegation

from joinnector.service.base_sdk_service import BaseSDKService


class TaskActivityService(BaseSDKService):
    def __init__(self, name):
        super().__init__(name)


taskactivity_service = TaskActivityService("taskactivity")
