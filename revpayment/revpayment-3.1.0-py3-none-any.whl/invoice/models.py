from django.conf import settings
from django.contrib import admin
from django.db import models

from revpayment.settings import api_settings


class Invoice(models.Model):
    INVOICE_TYPES = (("neweb", "neweb"), ("ecpay", "ecpay"))
    INVOICE_STATUS = (("success", "success"), ("failure", "failure"), ("void", "void"))

    CATEGORY = (("B2B", "B2B"), ("B2C", "B2C"))

    CARRIER_TYPE = (
        ("no_carrier", "no_carrier"),
        ("mobile", "mobile"),
        ("npc", "npc"),
        ("donation", "donation"),
        ("default", "default"),
    )

    category = models.CharField(max_length=10, choices=CATEGORY, default="B2C")
    order = models.ForeignKey(
        api_settings.ORDER_CLASS, null=True, on_delete=models.CASCADE
    )
    amount = models.IntegerField(default=0)
    invoice_type = models.CharField(
        max_length=64, choices=INVOICE_TYPES, default="neweb"
    )
    invoice_status = models.CharField(max_length=64, choices=INVOICE_STATUS)
    invoice_number = models.CharField(max_length=128, null=True)
    carrier_type = models.CharField(
        max_length=128, choices=CARRIER_TYPE, default="no_carrier", null=True
    )
    carrier_number = models.CharField(max_length=128, blank=True, null=True)
    uni_no = models.CharField(max_length=128, blank=True, null=True)
    print_flag = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    detail = models.TextField(blank=True)

    class Meta:
        abstract = "revpayment.invoice" not in settings.INSTALLED_APPS


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "invoice_type", "created")


if not Invoice._meta.abstract:
    admin.site.register(Invoice, InvoiceAdmin)
