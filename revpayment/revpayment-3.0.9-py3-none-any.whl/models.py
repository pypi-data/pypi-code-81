import json
import random
import string
import uuid
from uuid import uuid4

from django.conf import settings
from django.contrib import admin
from django.db import models
from django.utils import timezone

from revpayment.settings import api_settings


def uuid_hex():
    return uuid.uuid4().hex[:-2]


def random_digits(stringLength=8):
    letters = string.digits
    return "".join(random.choice(letters) for i in range(stringLength))


def gen_order_id():
    now = timezone.now()
    return now.strftime("%Y%m%d%H%M%S") + random_digits(4)


def empty_cart():
    from revpayment.carts import Cart

    return json.dumps(Cart.get_empty_cart())


class PaymentInfo(models.Model):
    cart = models.TextField(blank=True, default=empty_cart)
    credit = models.IntegerField(default=0)
    trading_slang = models.CharField(max_length=20, default=random_digits)
    owner = models.OneToOneField(
        api_settings.BUYER_CLASS, on_delete=models.CASCADE, related_name="payment"
    )
    uid = models.CharField(max_length=30, default=uuid_hex)

    class Meta:
        abstract = "revpayment" not in settings.INSTALLED_APPS
        app_label = "revpayment"


class RedirectState(models.Model):
    PAYMENT_TYPES = (
        ("offline", "offline"),
        ("ecpay", "ecpay"),  # 綠界支付 #
        ("neweb", "neweb"),  # 藍新支付 #
    )

    PAYMENT_SUBTYPES = (
        ("default", "default"),  # 預設全開 #
        ("credit", "credit"),  # 信用卡 #
        ("cvs_cod", "cvs_cod"),  # 超商貨到付款 #
        ("cvs", "cvs"),  # 超商付款 #
        ("atm", "atm"),  # atm #
        ("web_atm", "web_atm"),  # web_atm #
        ("barcode", "barcode"),  # 條碼付款 #
    )

    state = models.UUIDField(default=uuid4)
    redirect_url = models.URLField(default=api_settings.WEB_HOST)
    payment_type = models.CharField(
        max_length=20, choices=PAYMENT_TYPES, default="neweb"
    )
    payment_subtype = models.CharField(
        max_length=20, choices=PAYMENT_SUBTYPES, default="default"
    )
    cart = models.TextField()
    order_id = models.CharField(max_length=128, default=gen_order_id)
    order_type = models.CharField(max_length=128, default="default")
    buyer = models.ForeignKey(
        api_settings.BUYER_CLASS, on_delete=models.CASCADE, null=True
    )

    class Meta:
        abstract = "revpayment" not in settings.INSTALLED_APPS
        app_label = "revpayment"


class BaseOrder(models.Model):
    CURRENCY_CHOICES = (
        ("TWD", "TWD"),
        ("USD", "USD"),
        ("JPY", "JPY"),
    )

    PAYMENT_TYPES = (
        ("offline", "offline"),
        ("ecpay", "ecpay"),  # 綠界支付 #
        ("neweb", "neweb"),  # 藍新支付 #
    )

    PAYMENT_SUBTYPES = (
        ("default", "default"),  # 預設全開 #
        ("credit", "credit"),  # 信用卡 #
        ("cvs_cod", "cvs_cod"),  # 超商貨到付款 #
        ("cvs", "cvs"),  # 超商付款 #
        ("atm", "atm"),  # atm #
        ("web_atm", "web_atm"),  # web_atm #
        ("barcode", "barcode"),  # 條碼付款 #
    )

    PAYMENT_STATUS = (
        ("success", "success"),
        ("failure", "failure"),
        ("refunded", "refunded"),
        ("logistics_created", "logistics_created"),
        ("form_created", "form_created"),
        ("code_generated", "code_generated"),
    )

    TYPES = (("default", "default"), ("credit", "credit"))

    id = models.CharField(max_length=128, primary_key=True, default=gen_order_id)
    buyer = models.ForeignKey(api_settings.BUYER_CLASS, on_delete=models.CASCADE)
    order_type = models.CharField(max_length=128, choices=TYPES, default="default")
    amount = models.FloatField(default=0)
    title = models.CharField(max_length=100, default="order")
    description = models.CharField(max_length=256, default="no description")
    currency = models.CharField(max_length=8, choices=CURRENCY_CHOICES, default="TWD")
    payment_type = models.CharField(
        max_length=20, choices=PAYMENT_TYPES, default="neweb"
    )
    payment_subtype = models.CharField(
        max_length=20, choices=PAYMENT_SUBTYPES, default="default"
    )
    payment_status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS, default="waiting"
    )
    data = models.TextField(null=True, blank=True)
    cart = models.TextField(null=True, blank=True)
    receiver_email = models.EmailField()
    receiver_name = models.CharField(max_length=20, blank=True)
    receiver_phone = models.CharField(max_length=20, blank=True)
    receiver_address = models.CharField(max_length=128, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    payment_transaction_detail = models.TextField(blank=True)
    payment_redirect_detail = models.TextField(blank=True)

    code_no = models.CharField(max_length=128, blank=True)
    bank_code = models.CharField(max_length=128, blank=True)
    bank_account = models.CharField(max_length=128, blank=True)
    barcode_1 = models.CharField(max_length=128, blank=True)
    barcode_2 = models.CharField(max_length=128, blank=True)
    barcode_3 = models.CharField(max_length=128, blank=True)
    pay_deadline = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.id


class Order(BaseOrder):
    class Meta:
        abstract = "revpayment" not in settings.INSTALLED_APPS
        app_label = "revpayment"


if (
    settings.REVPAYMENT.get("ORDER_CLASS", "revpayment.models.Order")
    == "revpayment.models.Order"
    and "revpayment" in settings.INSTALLED_APPS
):
    admin.site.register(Order)
