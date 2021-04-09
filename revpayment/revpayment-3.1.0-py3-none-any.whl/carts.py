import json

from rest_framework import exceptions

from revpayment.settings import api_settings


class Cart:
    tax_rate = api_settings.TAX_RATE
    item_class = api_settings.ITEM_CLASS
    calc_class = api_settings.CALC_CLASS
    config_class = api_settings.CONFIG_CLASS

    def __init__(self, profile):
        self.profile = profile
        self.payment = profile.payment
        self.cart = json.loads(self.payment.cart)

    def _save_cart(self):
        config = self.cart["config"]
        calc = self.calc_class(
            items=self.cart["items"], profile=self.profile, config=config
        )
        self.cart["calculations"] = calc.get_calc_dict()
        self.payment.cart = json.dumps(self.cart, ensure_ascii=False)
        self.payment.save()

    def add_item(self, item):
        logic = self.item_class(item=item, profile=self.profile)
        verified_item = logic.get_item()
        self.cart["items"].append(verified_item)
        self._save_cart()

    def delete_item(self, index):
        if index > len(self.cart["items"]) - 1:
            raise exceptions.ValidationError
        items = self.cart["items"]
        del items[index]
        self.cart["items"] = items
        self._save_cart()

    def edit_item(self, index, config):
        items = self.cart["items"]
        if index > len(self.cart["items"]) - 1:
            raise exceptions.ValidationError
        item = items[index]
        item = {
            **item,
            "config": {**item["config"], **config},
            "product": item["product"]["id"],
        }
        item = self.item_class(item=item, profile=self.profile)
        self.cart["items"][index] = item.get_item()
        self._save_cart()

    def edit_config(self, update_config):
        config = self.config_class(config=self.cart["config"])
        config_dict = config.update_config(**update_config)
        self.cart["config"] = config_dict
        self._save_cart()

    def clear_cart(self):
        self.cart = {
            **self.cart,
            "items": [],
            "calculations": self.calc_class.get_empty_dict(),
        }
        self._save_cart()

    def _build_order_title(self):
        return "REVTEL-ORDER"

    def get_order_data(self):
        return {
            "amount": self.cart["calculations"]["amount"],
            "cart": json.dumps(self.cart, ensure_ascii=False),
            "title": self._build_order_title(),
            "receiver_name": self.cart["config"].get("name", self.profile.name),
            "receiver_email": self.cart["config"].get("email", self.profile.email),
            "receiver_phone": self.cart["config"].get("phone", self.profile.phone),
            "receiver_address": self.cart["config"].get(
                "address", self.profile.address
            ),
        }

    def on_order_will_create(self, data):
        return self.get_order_data()

    @staticmethod
    def get_empty_cart(dumps=False, **kwargs):
        data = {
            "config": {**kwargs},
            "items": [],
            "calculations": Cart.calc_class.get_empty_dict(),
        }
        if dumps:
            return json.dumps(data)
        return data
