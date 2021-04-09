import json
from datetime import datetime

import requests
from django.conf import settings
from django.utils import timezone

from revpayment import exceptions
from revpayment.settings import api_settings


class BaseAction:
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def perform(self, *args, **kwargs):
        processed = self.process_data(*args, **kwargs)
        return self.do_action(processed)

    def process_data(self, *args, **kwargs):
        raise NotImplementedError

    def do_action(self, data):
        raise NotImplementedError


class HttpAction(BaseAction):
    api_key = settings.CLIENT_SECRET
    version = api_settings.PAYMENT_VERSION
    method = "post"
    path = None
    if settings.STAGE == "prod":
        api_host = api_settings.PAYMENT_HOST
    else:
        api_host = api_settings.PAYMENT_DEBUG_HOST

    @property
    def url(self):
        return f"{self.api_host}/{self.version}{self.path}?client_id={settings.CLIENT_ID}&client_secret={settings.CLIENT_SECRET}"

    def build_headers(self):
        return {"x-api-key": self.api_key, "Content-Type": "application/json"}

    def do_action(self, data):
        headers = self.build_headers()
        httpmethod = getattr(requests, self.method)
        try:
            resp = httpmethod(self.url, json=data, headers=headers)
            resp.raise_for_status()
            return resp.json()
        except requests.HTTPError:
            resp_json = resp.json()
            raise exceptions.HttpActionError(resp.status_code, resp_json["detail"])


class CheckoutAction(HttpAction):
    handler_class = api_settings.HANDLER_CLASS
    payment_type = None

    def before_checkout(self):
        handler = self.handler_class(order=None)
        handler.before_checkout(
            cart=self.cart,
            order_id=self.order_id,
            order_type=self.order_type,
            payment_type=self.payment_type,
            payment_subtype=self.payment_subtype,
        )

    def perform(self):
        self.before_checkout()
        resp = super().perform()
        self.after_checkout()
        return resp

    def after_checkout(self):
        handler = self.handler_class(order=None)
        handler.after_checkout(
            cart=self.cart,
            order_id=self.order_id,
            order_type=self.order_type,
            payment_type=self.payment_type,
            payment_subtype=self.payment_subtype,
        )


class NewebCheckout(CheckoutAction):
    payment_type = "neweb"
    path = "/neweb/request"

    class Meta:
        payment_table = {
            "default": {
                "CREDIT": 1,
                "CVSCOM": 0,
                "BARCODE": 1,
                "CVS": 1,
                "WEBATM": 1,
                "VACC": 1,
            },
            "credit": {
                "CREDIT": 1,
                "CVSCOM": 0,
                "BARCODE": 0,
                "CVS": 0,
                "WEBATM": 0,
            },
            "cvs_cod": {
                "CREDIT": 0,
                "CVSCOM": 2,
                "BARCODE": 0,
                "CVS": 0,
                "WEBATM": 0,
            },
            "web_atm": {
                "CREDIT": 0,
                "CVSCOM": 0,
                "BARCODE": 0,
                "CVS": 0,
                "WEBATM": 1,
            },
            "cvs": {
                "CREDIT": 0,
                "CVSCOM": 0,
                "BARCODE": 0,
                "CVS": 1,
                "WEBATM": 0,
            },
            "atm": {
                "VACC": 1,
                "CREDIT": 0,
                "CVSCOM": 0,
                "BARCODE": 0,
                "CVS": 0,
                "WEBATM": 0,
            },
        }

    def process_data(self):
        payment_subtype = self.Meta.payment_table[self.payment_subtype]
        cart = self.cart
        items = cart["items"]
        now = timezone.now()
        data = {
            "TimeStamp": str(int(now.timestamp())),
            "Amt": int(cart["calculations"]["amount"]),
            "Email": cart["config"]["email"],
            "ItemDesc": items[0]["name"],
            "MerchantOrderNo": self.order_id,
            "CREDIT": 1,
            "CVSCOM": cart["config"].get("CVSCOM", 0),
            "BARCODE": 1,
            "CVS": 1,
            "WEBATM": 1,
            **payment_subtype,
        }
        return data


class EcpayCheckout(CheckoutAction):
    payment_type = "ecpay"
    path = "/ecpay/request"

    class Meta:
        payment_table = {
            "default": {"ChoosePayment": "ALL"},
            "credit": {"ChoosePayment": "Credit"},
            "web_atm": {"ChoosePayment": "WebATM"},
            "atm": {"ChoosePayment": "ATM"},
            "cvs": {"ChoosePayment": "CVS"},
            "barcode": {"ChoosePayment": "BARCODE"},
        }

    def process_data(self):
        now = timezone.now()
        payment_subtype = self.Meta.payment_table[self.payment_subtype]
        datetime_str = now.strftime("%Y/%m/%d %H:%M:%S")
        trade_no = self.order_id
        cart = self.cart
        calc = cart["calculations"]
        items = cart["items"]
        data = {
            "MerchantTradeNo": trade_no,
            "MerchantTradeDate": datetime_str,
            "TotalAmount": int(calc["amount"]),
            "ItemName": "#".join([item["name"] for item in items]),
            "TradeDesc": "None",
            "ChoosePayment": "ALL",
            "InvoiceMark": "N",
            "BindingCard": 1,
            "MerchantMemberID": self.buyer.payment.uid,
            **payment_subtype,
        }

        return {**data}


class CreditCheckout(BaseAction):
    def process_data(self):
        return {}

    def do_action(self, processed):
        buyer = self.buyer
        cart = self.cart
        calc = cart["calculations"]
        if buyer.payment.credit < calc["amount"]:
            raise exceptions.CreditNotEnough(buyer.payment.credit, calc["amount"])

        return {"amount": calc["amount"], "payment_status": "success"}


class CallbackAction(BaseAction):
    order_class = api_settings.ORDER_CLASS
    handler_class = api_settings.HANDLER_CLASS
    payment_type = None

    def process_data(self, data):
        cart = self.cart
        payment_data = data
        payment_data["id"] = payment_data.pop("order_id")
        payment_data["amount"] = cart["calculations"]["amount"]
        payment_data.pop("client_id", None)
        payment_data.pop("total", None)
        return payment_data

    def payment_result(self, order, changed):
        handler = self.handler_class(order=order)
        handler.on_payment_result(changed)

    def perform(self, data):
        config = self.cart["config"]
        items = self.cart["items"]
        mapped = self.process_data(data)
        changed = {"__created": False}

        if "id" not in mapped:
            raise ValueError("id is required in mapped data")
        try:
            order = self.order_class.objects.get(id=mapped["id"])
            del mapped["id"]
            for k, v in mapped.items():
                if getattr(order, k) != v:
                    changed[k] = v
                    changed["_" + k] = getattr(order, k)
                setattr(order, k, v)
            order.save()
        except:
            order = self.order_class.objects.create(
                **mapped,
                cart=json.dumps(self.cart, ensure_ascii=False, indent=4),
                title=items[0]["name"],
                receiver_email=config["email"],
                receiver_name=config["name"],
                receiver_phone=config.get("email", ""),
                receiver_address=config.get("address", ""),
                payment_type=self.payment_type,
                buyer=self.buyer,
                order_type=self.order_type,
            )
            changed = mapped
            changed["__created"] = True

        self.payment_result(order, changed)
        return order


class NewebCallback(CallbackAction):
    payment_type = "neweb"


class EcpayCallback(CallbackAction):
    payment_type = "ecpay"


class CreditCallback(CallbackAction):
    handler_class = api_settings.HANDLER_CLASS
    payment_type = "credit"

    def process_data(self, data):
        return {"id": self.order_id, **data}

    def payment_result(self, order, changed):
        super().payment_result(order, changed)
        payment = self.buyer.payment
        payment.credit -= order.amount
        payment.save()


class CustomerRedirectAction(BaseAction):
    order_class = api_settings.ORDER_CLASS
    handler_class = api_settings.HANDLER_CLASS
    payment_type = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def process_data(self, data):
        raise NotImplementedError

    def payment_result(self, order, changed):
        handler = self.handler_class(order=order)
        handler.on_payment_result(changed)

    def perform(self, data):
        config = self.cart["config"]
        items = self.cart["items"]
        mapped = self.process_data(data)
        changed = {"__created": False}
        if "id" not in mapped:
            if not self.order_id:
                raise ValueError("state order_id is null")
            mapped["id"] = self.order_id
        try:
            order = self.order_class.objects.get(id=mapped["id"])
            del mapped["id"]
            for k, v in mapped.items():
                if getattr(order, k) != v:
                    changed[k] = v
                    changed["_" + k] = getattr(order, k)
                setattr(order, k, v)
            order.save()
        except:
            order = self.order_class.objects.create(
                **mapped,
                payment_type=self.payment_type,
                payment_redirect_detail=json.dumps(data, ensure_ascii=False),
                cart=self.cart,
                title=items[0]["name"],
                receiver_email=config["email"],
                receiver_name=config["name"],
                receiver_phone=config.get("email", ""),
                receiver_address=config.get("address", ""),
                buyer=self.buyer,
            )
            changed = mapped
            changed["__created"] = True

        self.payment_result(order, changed)
        return order


class NewebCusRedirect(CustomerRedirectAction):
    payment_type = "neweb"

    def process_data(self, data):
        payload = {}
        result = data.get("Result")
        if not result:
            return {}
        elif isinstance(result, str):
            result = json.loads(result)
        payment_type = result["PaymentType"]
        if data["Status"] == "SUCCESS":
            payload["id"] = self.order_id
            payload["amount"] = (
                result["Amt"]
                if type(result["Amt"]) in [float, int]
                else int(result["Amt"])
            )
            payload["payment_status"] = "code_generated"
            payload["pay_deadline"] = result["ExpireDate"] + "T" + result["ExpireTime"]
            if payment_type == "CVS":
                payload["payment_subtype"] = "cvs"
                payload["code_no"] = result["CodeNo"]
            elif payment_type == "BARCODE":
                payload["payment_subtype"] = "barcode"
                payload["barcode_1"] = result["Barcode_1"]
                payload["barcode_2"] = result["Barcode_2"]
                payload["barcode_3"] = result["Barcode_3"]
            elif payment_type == "VACC":
                payload["payment_subtype"] = "atm"
                payload["bank_code"] = result["BankCode"]
                payload["bank_account"] = result["CodeNo"]

        return payload


class EcpayCusRedirect(CustomerRedirectAction):
    payment_type = "ecpay"

    def process_data(self, data):
        payment_type = data["PaymentType"]
        code = data["RtnCode"]
        payload = {"amount": data["TradeAmt"]}
        if payment_type.startswith("CVS_") and code == "10100073":
            payload["payment_status"] = "code_generated"
            payload["payment_subtype"] = "cvs"
            payload["code_no"] = data["PaymentNo"]
            payload["pay_deadline"] = data["ExpireDate"]
        elif payment_type.startswith("BARCODE_") and code == "10100073":
            payload["payment_status"] = "code_generated"
            payload["payment_subtype"] = "barcode"
            payload["barcode_1"] = data["Barcode1"]
            payload["barcode_2"] = data["Barcode2"]
            payload["barcode_3"] = data["Barcode3"]
            payload["pay_deadline"] = data["ExpireDate"]
        elif payment_type.startswith("ATM_") and code == "2":
            payload["payment_status"] = "code_generated"
            payload["payment_subtype"] = "atm"
            payload["bank_code"] = data["BankCode"]
            payload["bank_account"] = data["vAccount"]
            payload["pay_deadline"] = datetime.strptime(data["ExpireDate"], "%Y/%m/%d")
        return payload


class NewebRefund(HttpAction):
    path = "/neweb/refund"

    def process_data(self, order):
        now = timezone.now()
        data = {
            "Amt": order.amount,
            "MerchantOrderNo": order.id,
            "TimeStamp": str(int(now.timestamp())),
            "IndexType": 1,
            "CloseType": 1,
        }
        return data

    def perform(self, order):
        data = self.process_data(order)
        resp = self.do_action(data)
        data["CloseType"] = 2
        resp = self.do_action(data)
        return resp
