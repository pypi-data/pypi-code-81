# pylint: disable=useless-super-delegation

from joinnector.service.base_sdk_service import BaseSDKService


class ReviewService(BaseSDKService):
    def __init__(self, name):
        super().__init__(name)


review_service = ReviewService("review")
