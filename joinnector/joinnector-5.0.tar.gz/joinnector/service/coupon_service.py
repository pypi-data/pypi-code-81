# pylint: disable=useless-super-delegation

from joinnector.service.base_sdk_service import BaseSDKService


class CouponService(BaseSDKService):
    def __init__(self, name):
        super().__init__(name)


coupon_service = CouponService("coupon")
