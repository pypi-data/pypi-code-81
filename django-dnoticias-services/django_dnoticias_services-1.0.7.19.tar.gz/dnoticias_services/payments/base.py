from django.conf import settings


class BasePaymentRequest:
    def __init__(self):
        self.api_key = getattr(settings, "PAYMENT_SERVICE_ACCOUNT_API_KEY", None)
        self.timeout = getattr(settings, "PAYMENT_SERVICE_REQUEST_TIMEOUT", 5)
