class PaymentException(Exception):
    error = None
    error_detail = None


class HttpActionError(PaymentException):
    def __init__(self, status_code, detail):
        msg = f"status_code: {status_code}, detail: {detail}"
        self.error = "http_exception"
        self.error_detail = msg
        super().__init__(msg)


class CreditNotEnough(PaymentException):
    def __init__(self, current, paid):
        msg = f"current credit: {current} not enough for paid: {paid}"
        self.error = "credit_not_enough"
        self.error_detail = msg
        super().__init__(msg)


class InvalidPaymentType(PaymentException):
    def __init__(self, valids, invalid):
        msg = f"valid types: {valids}, invalid: {invalid}"
        self.error = "invalid_payment"
        self.error_detail = msg
        super().__init__(msg)


class InvalidCallback(PaymentException):
    def __init__(self):
        error_detail = "signature in valid"
        super().__init__(error_detail)
