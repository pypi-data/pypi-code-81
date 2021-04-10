# pylint: disable=useless-super-delegation

from joinnector.service.base_sdk_service import BaseSDKService


class LeadService(BaseSDKService):
    def __init__(self, name):
        super().__init__(name)

    def get_by_customer_id(self, customer_id, swap_id=None):
        return super().get_by("customer_id", customer_id, swap_id)

    def get_by_email(self, email, swap_id=None):
        return super().get_by("email", email, swap_id)

    def get_by_mobile(self, mobile, swap_id=None):
        return super().get_by("mobile", mobile, swap_id)


lead_service = LeadService("lead")
