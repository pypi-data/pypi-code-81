from revpayment.settings import api_settings
from revpayment.utils import round


class BaseCalculations:
    tax_rate = api_settings.TAX_RATE

    def __init__(self, items, profile, config):
        self.items = items
        self.profile = profile
        self.config = config

    def get_sales(self):
        raise NotImplementedError

    def get_items(self):
        raise NotImplementedError

    def get_amount(self):
        raise NotImplementedError

    def get_invoice_items(self):
        raise NotImplementedError

    def get_calc_dict(self):
        fee, fee_tax = self.get_fee()
        sales, tax = self.get_sales()
        items_amt, items_tax = self.get_items()
        return self.format_result(
            {
                "amount": sales + tax,
                "items_amount": items_amt,
                "items_tax": items_tax,
                "fee": fee,
                "fee_tax": fee_tax,
                "sales": sales,
                "tax": tax,
            }
        )

    def format_result(self, data):
        for k, v in data.items():
            if type(v) is float:
                data[k] = int(v)
        return data

    @staticmethod
    def get_empty_dict():
        return {
            "amount": 0,
            "items_amount": 0,
            "items_tax": 0,
            "fee": 0,
            "fee_tax": 0,
            "sales": 0,
            "tax": 0,
        }


class Calculations(BaseCalculations):
    extra_invoices = [{"amount": "fee", "tax": "fee_tax", "name": "運費"}]

    def get_fee(self):
        return 0, 0

    def get_sales(self):
        fee, fee_tax = self.get_fee()
        items = self.items
        amount = sum([item["price"] for item in items])
        result = round(amount / (1 + self.tax_rate))
        tax = amount - result
        return result + fee, tax + fee_tax

    def get_items(self):
        items = self.items
        amount = sum([item["price"] for item in items])
        result = round(amount / (1 + self.tax_rate))
        tax = amount - result
        return result, tax

    def get_amount(self):
        sales, tax = self.get_sales()
        return sales + tax

    def get_invoice_items(self, category="B2C", calc={}):
        if category == "B2C":
            items = [
                {
                    "name": item["name"],
                    "price": int(item["price"] / item["config"]["quantity"]),
                    "amount": item["price"],
                    "quantity": item["config"]["quantity"],
                }
                for item in self.items
            ]
            for field in self.extra_invoices:
                value = calc.get(field["amount"], 0)
                tax = calc.get(field["tax"], 0)
                if value:
                    items.append(
                        {
                            "name": field["name"],
                            "price": round(value + tax),
                            "amount": round(value + tax),
                            "quantity": 1,
                        }
                    )
            return items
        else:
            rate = 1 + self.tax_rate
            items = [
                {
                    "name": item["name"],
                    "price": round(item["price"] / (item["config"]["quantity"] * rate)),
                    "amount": round(item["price"] / rate),
                    "quantity": item["config"]["quantity"],
                }
                for item in self.items
            ]
            for field in self.extra_invoices:
                value = calc.get(field["amount"], 0)
                tax = calc.get(field["tax"], 0)
                if value:
                    items.append(
                        {
                            "name": field["name"],
                            "price": value,
                            "amount": value,
                            "quantity": 1,
                        }
                    )
            return items
