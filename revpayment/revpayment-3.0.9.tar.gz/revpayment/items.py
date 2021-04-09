from rest_framework import exceptions

from revpayment import TAX_RATE
from revpayment.settings import api_settings


class BaseItem:
    tax_rate = TAX_RATE
    product_class = api_settings.PRODUCT_CLASS
    serializer_class = api_settings.PRODUCT_SERIALIZER_CLASS

    def __init__(self, item, profile):
        self.item = item
        self.profile = profile
        try:
            self.product = self.product_class.objects.get(id=item["product"])
        except:
            raise exceptions.NotFound
        self.validate_config()

    def _get_serialized_product(self):
        return self.serializer_class(self.product).data

    def get_item(self):
        raise NotImplementedError

    def validate_config(self):
        raise NotImplementedError

    def get_price(self):
        raise NotImplementedError

    @classmethod
    def get_credit_item(cls, credit, naming_format="{} 點"):
        return {
            "name": naming_format.format(credit),
            "price": credit,
            "config": {"quantity": 1},
        }


class Item(BaseItem):
    def validate_config(self):
        if "config" not in self.item:
            raise exceptions.ValidationError

        config = self.item["config"]
        if "quantity" not in config:
            raise exceptions.ValidationError

    def get_item(self):
        extra = {}
        price = self.get_price()
        return {
            "product": self._get_serialized_product(),
            "price": price,
            "config": self.item["config"],
            "name": self.product.name,
            **extra,
        }

    def get_price(self):
        amount = self.product.price * self.item["config"]["quantity"]
        return amount
