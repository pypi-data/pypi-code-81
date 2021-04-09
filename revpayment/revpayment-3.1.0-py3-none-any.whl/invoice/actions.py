import json

from django.utils import timezone

from revpayment.actions import HttpAction
from revpayment.invoice.exceptions import MapResultError
from revpayment.settings import api_settings


class InvoiceAction(HttpAction):
    invoice_class = api_settings.INVOICE_CLASS
    calc_class = api_settings.CALC_CLASS
    invoice_type = None

    def __init__(
        self,
        order=None,
        category=None,
        carrier_type=None,
        carrier_num=None,
        uni_no=None,
        receiver_email=None,
        slang=None,
        company_title=None,
        cart=None,
    ):
        self.order = order
        self._category = category
        self._carrier_type = carrier_type
        self._carrier_num = carrier_num
        self._uni_no = uni_no
        self._company_title = company_title
        self._receiver_email = receiver_email
        self._slang = slang
        self._cart = cart

    @property
    def invoice_id(self):
        count = self.invoice_class.objects.filter(order=self.order).count() + 1
        return f"{self.order.id}_{count}"

    @property
    def receiver_email(self):
        if self._receiver_email:
            return self._receiver_email
        if self.order:
            return self.order.receiver_email
        return self.cart["config"]["email"]

    @property
    def slang(self):
        if self.order:
            return self.order.buyer.payment.trading_slang
        return self._slang

    @property
    def category(self):
        return (
            self._category
            if self._category
            else self.cart["config"].get("category", None)
        )

    @property
    def company_title(self):
        return (
            self._company_title
            if self._company_title
            else self.cart["config"].get("company_title", None)
        )

    @property
    def carrier_type(self):
        return (
            self._carrier_type
            if self._carrier_type
            else self.cart["config"].get("carrier_type", None)
        )

    @property
    def carrier_number(self):
        if self.carrier_type == "default":
            return self.receiver_email
        return (
            self._carrier_num
            if self._carrier_num
            else self.cart["config"].get("carrier_num", None)
        )

    @property
    def uni_no(self):
        return self._uni_no if self._uni_no else self.cart["config"].get("uni_no", None)

    @property
    def cart(self):
        if self._cart:
            return json.loads(self._cart)
        if self.order:
            return json.loads(self.order.cart)
        return None

    @property
    def items(self):
        if self.order:
            cart = self.cart
            calc = self.calc_class(
                items=cart["items"], config=cart["config"], profile=self.order.buyer
            )
            return calc.get_invoice_items(
                category=self.category, calc=cart["calculations"]
            )
        return None


class IssueAction(InvoiceAction):
    def map_result(self, result):
        raise NotImplementedError

    def perform(self, **kwargs):
        result = super().perform(**kwargs)
        invoice = self.on_result(result)
        return invoice

    def on_result(self, result):
        try:
            mapped = self.map_result(result)
        except Exception as e:
            msg = json.dumps(result, ensure_ascii=False)
            raise MapResultError(e)

        if not mapped:
            return None
        return self.invoice_class.objects.create(
            order=self.order,
            carrier_type=self.carrier_type,
            carrier_number=self.carrier_number,
            category=self.category,
            uni_no=self.uni_no,
            amount=self.cart["calculations"]["amount"],
            detail=json.dumps(result, ensure_ascii=False),
            invoice_type=self.invoice_type,
            **mapped,
        )


class EcpayIssue(IssueAction):
    invoice_type = "ecpay"

    @property
    def path(self):
        if self.category == "B2B":
            return "/ecpay/B2B/invoice/issue"
        return "/ecpay/B2C/invoice/issue"

    def map_result(self, data):
        payload = {}
        result = data["Data"]
        if result.get("RtnCode") == 1:
            payload["invoice_status"] = "success"
            no_str = "InvoiceNumber" if self.category == "B2B" else "InvoiceNo"
            payload["invoice_number"] = result[no_str]
        else:
            payload["invoice_status"] = "failure"

        return payload

    def process_data(self, **kwargs):
        calc = self.cart["calculations"]
        config = self.cart["config"]
        extra = {}
        if self.category == "B2B":
            extra["CustomerIdentifier"] = self.uni_no
            extra["Identifier"] = self.uni_no
            extra["SalesAmount"] = calc["sales"]
            extra["TaxAmount"] = calc["tax"]
            extra["TotalAmount"] = calc["amount"]
            extra["CompanyName"] = self.company_title
            extra["Address"] = config["address"]
            extra["EmailAddress"] = config["email"]
            extra["TelephoneNumber"] = config["phone"]
            extra["ExchangeMode"] = "1"
            extra["type"] = "1"
            extra["Action"] = "Add"
        else:
            extra["Donation"] = "1" if self.carrier_type == "donation" else "0"
            if extra["Donation"] == "1":
                extra["LoveCode"] = self.carrier_number
            else:
                types = {"default": "1", "npc": "2", "mobile": "3", "donation": ""}
                extra["CarrierType"] = types[self.carrier_type]
                extra["CarrierNum"] = (
                    self.carrier_number if extra["CarrierType"] != "1" else ""
                )
            extra["Print"] = "0"
            extra["SalesAmount"] = round(calc["amount"])

        return {
            "category": self.category,
            "TimeStamp": int(timezone.now().timestamp()),
            "RelateNumber": self.invoice_id,
            "CustomerEmail": config["email"],
            "TaxType": "1",  # 課稅類別
            "InvType": "07",
            "Items": self.build_items(),
            "vat": "1",
            **extra,
            **kwargs,
        }

    def build_items(self):
        items = [
            {
                "ItemSeq": index + 1,
                "ItemName": item["name"],
                "ItemCount": item["quantity"],
                "ItemWord": "個",
                "ItemPrice": item["price"],
                "ItemAmount": item["amount"],
                "ItemTaxType": "1",
            }
            for index, item in enumerate(self.items)
        ]
        return items


class NewebIssue(IssueAction):
    invoice_type = "neweb"
    path = "/neweb/invoice/issue"

    class Meta:
        mapping = {"mobile": "0", "npc": "1", "default": "2", "donation": ""}

    def map_result(self, data):
        result = data["Result"]
        result = result if type(result) in [dict, list] else json.loads(result)
        payload = {}
        if data["Status"] == "SUCCESS":
            payload["invoice_status"] = "success"
            payload["invoice_number"] = result["InvoiceNumber"]
        else:
            payload["invoice_status"] = "failure"
        return payload

    def build_items(self):
        return self.items

    def process_data(self, **kwargs):
        resp_data = {
            **self.build_general_data(),
            **self.build_detail_data(),
        }
        return {**resp_data, "items": self.build_items()}

    def build_detail_data(self):
        data = {}
        if self.category == "B2C":
            data = {
                "Category": "B2C",
                "PrintFlag": "N",
                "CarrierType": self.Meta.mapping[self.carrier_type],
                "CarrierNum": self.carrier_number,
            }

        elif self.category == "B2B":
            data = {
                "Category": "B2B",
                "PrintFlag": "Y",
                "BuyerUBN": self.uni_no,
                "BuyerName": self.company_title,
            }

        if self.carrier_type == "donation":
            data = {"PrintFlag": "N", "LoveCode": self.carrier_number}

        return data

    def build_general_data(self):
        now = timezone.now()
        config = self.cart["config"]
        tax = self.cart["calculations"]["tax"]
        return {
            "RespondType": "JSON",
            "Version": "1.4",
            "TimeStamp": str(int(now.timestamp())),
            "MerchantOrderNo": self.invoice_id,
            "Status": "1",
            "Category": self.category,
            "BuyerName": config.get("name"),
            "BuyerEmail": self.receiver_email,
            "PrintFlag": "Y",
            "TaxType": "1",
            "TaxRate": float(5),
            "Amt": self.cart["calculations"]["sales"],
            "TaxAmt": tax,
            "TotalAmt": self.cart["calculations"]["amount"],
        }


class NewebVoid(HttpAction):
    path = "/neweb/invoice/void"

    def process_data(self, invoice_num, reason):
        return {"InvoiceNumber": invoice_num, "InvalidReason": reason}
