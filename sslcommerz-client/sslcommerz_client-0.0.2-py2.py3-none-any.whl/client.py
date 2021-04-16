from .dataclasses import (
    Credential,
    PaymentInitPostData,
    APIResponse,
    PaymentInitResponse,
)
from typing import Union
from pprint import pprint
import requests


class SSLCommerzClient:
    def __init__(self, credential: Credential):
        self.credential = credential

    @property
    def sandbox(self):
        return self.credential.sandbox

    @property
    def baseURL(self):
        if self.sandbox:
            return "https://sandbox.sslcommerz.com"
        else:
            return "https://securepay.sslcommerz.com"

    @property
    def usable_credential(self):
        return {
            "store_id": self.credential.store_id,
            "store_passwd": self.credential.store_passwd,
        }

    def initiateSession(self, postData: Union[PaymentInitPostData, dict]):
        if not isinstance(postData, PaymentInitPostData):
            postData = PaymentInitPostData(**postData)
        url = self.baseURL + "/gwprocess/v4/api.php"
        request_data = postData.dict(exclude_none=True)
        request_data.update(self.usable_credential)
        resp = requests.post(url, request_data)
        if resp:
            pprint(resp.json())
            return APIResponse(
                raw_data=resp,
                status_code=resp.status_code,
                response=PaymentInitResponse(**resp.json()),
            )
        else:
            return APIResponse(raw_data=resp, status_code=resp.status_code)
