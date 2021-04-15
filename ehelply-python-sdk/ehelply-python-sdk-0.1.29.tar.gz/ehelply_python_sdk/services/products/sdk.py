from .schemas import *
from ehelply_python_sdk.services.service_sdk_base import SDKBase


class ProductsSDK(SDKBase):
    def get_base_url(self) -> str:
        return super().get_base_url() + "/products"

    def get_docs_url(self) -> str:
        return super().get_docs_url()

    def get_service_version(self) -> str:
        return super().get_service_version()

    def process_payment(self, project_uuid: str, amount: int) -> Union[GenericHTTPResponse, ProcessPaymentResponse]:
        return transform_response_to_schema(
            self.requests_session.post(
                self.get_base_url() + "/products/billing/process_payment",
                json={"payment_schema": {
                    "project_uuid": project_uuid,
                    "amount": amount
                }}
            ),
            schema=ProcessPaymentResponse
        )