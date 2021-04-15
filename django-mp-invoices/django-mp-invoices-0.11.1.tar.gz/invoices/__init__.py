
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class InvoicesConfig(AppConfig):

    name = 'invoices'
    verbose_name = _("Invoices")

    is_online_sale_enabled = False


default_app_config = 'invoices.InvoicesConfig'
