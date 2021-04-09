from django.shortcuts import redirect

from revpayment.settings import api_settings

default_app_config = "revpayment.logistics.apps.LogisticsConfig"


class LogisticsSDK:
    def __init__(self, order=None, logistic_provider="ecpay"):
        self.order = order
        self.logistic_provider = logistic_provider

    @property
    def provider_class(self):
        from revpayment.logistics.providers import EcpayLogistics

        if self.logistic_provider == "ecpay":
            return EcpayLogistics

    @property
    def provider(self):
        return self.provider_class(order=self.order)

    def create_logistics(self, **kwargs):
        return self.provider.create_logistics(**kwargs)

    def callback(self, *args, **kwargs):
        return self.provider.callback(*args, **kwargs)

    def cvs_map(self, logistic_subtype, state, collection=False):
        return self.provider.cvs_map(logistic_subtype, collection, state)

    def cvs_callback(self, result, profile):
        from revpayment.carts import Cart

        cart = Cart(profile)
        cart.edit_config(result)
        return redirect(f"{api_settings.WEB_HOST}/cart")
