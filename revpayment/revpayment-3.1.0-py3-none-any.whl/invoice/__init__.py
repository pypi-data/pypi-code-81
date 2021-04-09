default_app_config = "revpayment.invoice.apps.RevpaymentInvoiceConfig"


class InvoiceSDK:
    def __init__(self, order=None, invoice_type="neweb"):
        self.order = order
        self.invoice_type = invoice_type

    def get_provider_class(self):
        from .providers import EcpayProvider, NewebProvider

        if self.invoice_type == "ecpay":
            return EcpayProvider
        elif self.invoice_type == "neweb":
            return NewebProvider

    def get_provider(self, **kwargs):
        provider_class = self.get_provider_class()
        return provider_class(order=self.order, **kwargs)

    def issue_invoice(self, **kwargs):
        invoice = self.get_provider(**kwargs)
        resp = invoice.issue_invoice()
        return resp
