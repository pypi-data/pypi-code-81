# client

from joinnector.wrapper.security_wrapper import sucurity_wrapper
from joinnector.wrapper.logging_wrapper import logging_wrapper
from joinnector.wrapper.request_wrapper import request_wrapper

# service
from joinnector.service.coupon_service import coupon_service
from joinnector.service.currency_service import currency_service
from joinnector.service.deal_service import deal_service
from joinnector.service.lead_service import lead_service
from joinnector.service.notification_service import notification_service
from joinnector.service.review_service import review_service
from joinnector.service.setting_service import setting_service
from joinnector.service.swap_service import swap_service
from joinnector.service.task_service import task_service
from joinnector.service.taskactivity_service import taskactivity_service
from joinnector.service.wallet_service import wallet_service
from joinnector.service.wallettransaction_service import wallettransaction_service

class SDK(object):
    def __init__(self, key, secret, mode="prod"):
        self.init_wrappers(key=key, secret=secret, mode=mode)

    def init_wrappers(self, key, secret, mode):
        sucurity_wrapper.init()
        logging_wrapper.init()
        request_wrapper.init(key=key, secret=secret, mode=mode)

    def get_coupon_service(self):
        return coupon_service

    def get_currency_service(self):
        return currency_service

    def get_deal_service(self):
        return deal_service

    def get_lead_service(self):
        return lead_service

    def get_notification_service(self):
        return notification_service

    def get_review_service(self):
        return review_service

    def get_setting_service(self):
        return setting_service

    def get_swap_service(self):
        return swap_service

    def get_task_service(self):
        return task_service

    def get_taskactivity_service(self):
        return taskactivity_service

    def get_wallet_service(self):
        return wallet_service

    def get_wallettransaction_service(self):
        return wallettransaction_service
