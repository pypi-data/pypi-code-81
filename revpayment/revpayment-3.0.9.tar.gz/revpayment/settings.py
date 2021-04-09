from django.conf import settings
from django.utils.module_loading import import_string

DEFAULTS = {
    # Base API policies
    "DEBUG": True,
    "PAYMENT_VERSION": "v3",
    "PAYMENT_HOST": "https://payment.revtel-api.com",
    "PAYMENT_DEBUG_HOST": "https://payment-stg.revtel-api.com",
    "TAX_RATE": 0.05,
    "LOGISTIC_SENDER_NAME": "",
    "LOGISTIC_SENDER_PHONE": "",
    "LOGISTIC_SENDER_CELLPHONE": "",
    "ORDER_CLASS": "revpayment.models.Order",
    "ITEM_CLASS": "revpayment.items.Item",
    "CALC_CLASS": "revpayment.calculations.Calculations",
    "CONFIG_CLASS": "revpayment.config.Config",
    "HANDLER_CLASS": "revpayment.handlers.Handler",
    "INVOICE_CLASS": "revpayment.invoice.models.Invoice",
    "DEFAULT_SDK_CLASS": "revpayment.checkout.CheckoutSDK",
    "DEFAULT_CART_CLASS": "revpayment.carts.Cart",
    "DEFAULT_NEWEB_CLASS": "revpayment.payments.NewebPayment",
    "DEFAULT_ECPAY_CLASS": "revpayment.payments.EcpayPayment",
    "DEFAULT_CREDIT_CLASS": "revpayment.payments.CreditPayment",
    "DEFAULT_REDIRECT_URL": f"{settings.WEB_HOST}/order",
    "DEFAULT_CHECKOUTFAIL_URL": f"{settings.WEB_HOST}/cart",
    "DEFAULT_REDIRECT_QUERY": "id",
}


# List of settings that may be in string import notation.
IMPORT_STRINGS = [
    "ORDER_CLASS",
    "ITEM_CLASS",
    "CALC_CLASS",
    "CONFIG_CLASS",
    "HANDLER_CLASS",
    "INVOICE_CLASS",
    "BUYER_CLASS",
    "PRODUCT_CLASS",
    "PRODUCT_SERIALIZER_CLASS",
    "VERIFY_METHOD",
    "DEFAULT_SDK_CLASS",
    "DEFAULT_CART_CLASS",
    "DEFAULT_NEWEB_CLASS",
    "DEFAULT_ECPAY_CLASS",
    "DEFAULT_CREDIT_CLASS",
]


def perform_import(val, setting_name):
    """
    If the given setting is a string import notation,
    then perform the necessary import or imports.
    """
    if val is None:
        return None
    elif isinstance(val, str):
        return import_from_string(val, setting_name)
    elif isinstance(val, (list, tuple)):
        return [import_from_string(item, setting_name) for item in val]
    return val


def import_from_string(val, setting_name):
    """
    Attempt to import a class from a string representation.
    """
    try:
        return import_string(val)
    except ImportError as e:
        msg = "Could not import '%s' for API setting '%s'. %s: %s." % (
            val,
            setting_name,
            e.__class__.__name__,
            e,
        )
        raise ImportError(msg)


class APISettings:
    def __init__(self, defaults=None, import_strings=None):
        self.defaults = defaults or DEFAULTS
        self.import_strings = import_strings or IMPORT_STRINGS

    @property
    def user_settings(self):
        return getattr(settings, "REVPAYMENT", {})

    def __getattr__(self, attr):
        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Coerce import strings into classes
        if attr in self.import_strings:
            val = perform_import(val, attr)

        # Cache the result
        setattr(self, attr, val)
        return val


api_settings = APISettings(DEFAULTS, IMPORT_STRINGS)
