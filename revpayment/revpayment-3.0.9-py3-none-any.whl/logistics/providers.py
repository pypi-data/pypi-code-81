import json
from datetime import datetime

import requests
from django.http import HttpResponse

from revpayment.logistics.models import Logistics
from revpayment.models import RedirectState
from revpayment.settings import api_settings

API_HOST = "https://payment.revtel-api.com"
STG_HOST = "https://payment-stg.revtel-api.com"
STATE = {
    "FAMI": {
        "300": "processing",
        "310": "uploading",
        "3024": "transit",
        "3022": "delivered",
        "3018": "store_arrived",
    },
    "UNIMART": {
        "300": "processing",
        "310": "uploading",
        "2041": "transit",
        "2067": "delivered",
        "2063": "store_arrived",
    },
    "UNIMARTC2C": {
        "300": "processing",
        "310": "uploading",
        "2068": "transit",
        "2067": "delivered",
        "2073": "store_arrived",
    },
    "HILIFE": {
        "300": "processing",
        "310": "uploading",
        "3006": "transit",
        "2067": "delivered",
        "2063": "store_arrived",
        "2073": "store_arrived",
    },
    "ECAN": {
        "300": "processing",
        "310": "uploading",
        "3006": "transit",
        "3003": "delivered",
    },
    "TCAT": {
        "300": "processing",
        "310": "uploading",
        "3006": "transit",
        "3003": "delivered",
    },
}
STATE["FAMIC2C"] = STATE["FAMI"]
STATE["HILIFEC2C"] = STATE["HILIFE"]


class BaseLogistics:
    DEBUG = api_settings.DEBUG
    API_KEY = api_settings.CLIENT_SECRET
    VERSION = "v2"
    logistic_provider = "none"
    logistics_class = Logistics
    handler_class = api_settings.HANDLER_CLASS
    sender_name = api_settings.LOGISTIC_SENDER_NAME
    sender_phone = api_settings.LOGISTIC_SENDER_PHONE
    sender_cellphone = api_settings.LOGISTIC_SENDER_CELLPHONE
    callback_prefix = "payment"

    def __init__(self, order):
        self.order = order

    @property
    def state(self):
        return RedirectState.objects.get(order_id=self.order.id)

    @property
    def cart(self):
        return json.loads(self.order.cart)

    @property
    def logistic_type(self):
        config = self.cart["config"]
        return config["logistic_type"]

    @property
    def logistic_subtype(self):
        config = self.cart["config"]
        return config["logistic_subtype"]

    @property
    def url(self):
        if self.DEBUG:
            return f"{STG_HOST}/{self.VERSION}"
        return f"{API_HOST}/{self.VERSION}"

    def _post(self, url, data):
        return requests.post(
            url,
            json=data,
            headers={"x-api-key": self.API_KEY, "Content-Type": "application/json"},
        )

    def map_logistic_callback(self, data):
        raise NotImplementedError

    def build_logistic_data(self):
        raise NotImplementedError

    def on_logistic_result(self, data):
        mapped = self.map_logistic_callback(data)
        if not mapped:
            return
        fields = [f.name for f in self.logistics_class._meta.get_fields()]

        try:
            logistics = self.logistics_class.objects.get(order=self.order)
        except:
            logistics = self.logistics_class.objects.create(
                order=self.order,
                logistic_provider=self.logistic_provider,
                logistic_type=self.logistic_type,
                logistic_subtype=self.logistic_subtype,
            )
        for k, v in mapped.items():
            if k in fields:
                setattr(logistics, k, v)
        try:
            detail = json.loads(logistics.detail)
        except:
            detail = []
        detail.append(data)
        detail_str = json.dumps(detail, ensure_ascii=False)
        logistics.detail = detail_str
        logistics.save()

        changed = {"_payment_status": self.order.payment_status}
        if (
            self.order.payment_subtype == "cvs_cod"
            and mapped.get("logistic_status") == "delivered"
        ):
            self.order.payment_status = "success"
            self.order.save()
            changed["payment_status"] = self.order.payment_status
            handler = self.handler_class(order=self.order)
            handler.on_payment_result(changed)
        return logistics

    def create_logistics(self):
        data = self.build_logistic_data()
        url = f"{self.url}/{self.logistic_provider}/logistics/create"

        resp = self._post(url, data=data)
        resp_json = resp.json()
        resp.raise_for_status()
        logistics = self.on_logistic_result(resp_json)
        return logistics

    def callback(self, data):
        self.on_logistic_result(data)

    def build_cvs_data(self, **kwargs):
        raise NotImplementedError

    def cvs_map(self, logistic_subtype, collection, state):
        url = f"{self.url}/{self.logistic_provider}/cvs/map"
        data = self.build_cvs_data(logistic_subtype, collection, state)
        resp = self._post(url, data=data)
        resp.raise_for_status()
        resp_json = resp.json()
        return HttpResponse(resp_json["html"], charset="utf-8")


class EcpayLogistics(BaseLogistics):
    logistic_provider = "ecpay"

    def build_logistic_data(self):
        config = self.cart["config"]
        extra = {}
        if self.order.payment_subtype == "cvs_cod":
            extra["IsCollection"] = "Y"

        if self.logistic_type == "cvs":
            extra["LogisticsType"] = "CVS"
            extra["LogisticsSubType"] = config["logistic_subtype"]
            extra["ReceiverStoreID"] = config["CVSStoreID"]
            extra[
                "LogisticsC2CReplyURL"
            ] = f"{api_settings.WEB_HOST}/order?id={self.order.id}"

        if self.logistic_type == "home":
            extra["LogisticsType"] = "HOME"
            extra["LogisticsSubType"] = config.get("logistic_subtype", "TCAT")
            extra["ReceiverAddress"] = config["ReceiverAddress"]
            extra["ReceiverZipCode"] = config["zip_code"]
            extra["Temperature"] = "0001"
            extra["Distance"] = "00"
            extra["Specification"] = "0001"

        return {
            "MerchantTradeDate": datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
            "MerchantTradeNo": self.order.id,
            "SenderName": self.sender_name,
            "SenderPhone": self.sender_phone,
            "SenderCellPhone": self.sender_cellphone,
            "ReceiverName": config["name"],
            "ReceiverEmail": config["email"],
            "ReceiverPhone": config["phone"],
            "ReceiverCellPhone": config["phone"],
            "GoodsAmount": self.order.amount,
            "GoodsName": self.order.title,
            "ServerReplyURL": f"{api_settings.API_HOST}/{self.callback_prefix}/logistics/callback?state={self.state.state}",
            **extra,
        }

    def map_logistic_callback(self, data):
        code = data["RtnCode"]
        try:
            status = STATE[self.logistic_subtype][code]
        except:
            status = "exception"
        return {
            "logistic_status": status,
        }

    def build_cvs_data(self, logistic_subtype, collection, state, is_mobile=False):
        extra = {"IsCollection": "N"}
        if collection:
            extra["IsCollection"] = "Y"
        return {
            "LogisticsType": "CVS",
            "LogisticsSubType": logistic_subtype,
            "ServerReplyURL": f"{api_settings.API_HOST}/{self.callback_prefix}/logistics/cvs/callback?state={state.state}",
            "Device": 1 if is_mobile else 0,
            **extra,
        }
