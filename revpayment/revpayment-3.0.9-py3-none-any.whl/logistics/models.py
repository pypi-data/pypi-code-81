from django.conf import settings
from django.contrib import admin
from django.db import models

from revpayment.settings import api_settings

# Create your models here.


class Logistics(models.Model):
    PROVIDERS = (("ecpay", "ecpay"),)
    TYPES = (
        ("home", "home"),
        ("cvs", "cvs"),
    )
    SUBTYPES = (
        ("FAMI", "FAMI"),
        ("FAMIC2C", "FAMIC2C"),
        ("UNIMART", "UNIMART"),
        ("UNIMARTC2C", "UNIMARTC2C"),
        ("HILIFE", "HIFIFE"),
        ("HILIFEC2C", "HIFIFEC2C"),
        ("ECAN", "ECAN"),
        ("TCAT", "TCAT"),
    )
    STATUS = (
        ("processing", "processing"),
        ("uploading", "uploading"),
        ("transit", "transit"),
        ("delivered", "delivered"),
        ("store_arrived", "store_arrived"),
    )
    order = models.ForeignKey(api_settings.ORDER_CLASS, on_delete=models.CASCADE)
    logistic_provider = models.CharField(
        max_length=128, default="ecpay", choices=PROVIDERS
    )
    logistic_type = models.CharField(max_length=128, default="cvs", choices=TYPES)
    logistic_subtype = models.CharField(
        max_length=128, default="UNIMARTC2C", choices=SUBTYPES
    )
    logistic_status = models.CharField(
        max_length=128, default="processing", choices=STATUS
    )
    detail = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = "revpayment.logistics" not in settings.INSTALLED_APPS


if not Logistics._meta.abstract:
    admin.site.register(Logistics)
