#
# This class was auto-generated from the API references found at
# https://support.direct.ingenico.com/documentation/api/reference/
#
from ingenico.direct.sdk.api_resource import ApiResource
from ingenico.direct.sdk.call_context import CallContext
from ingenico.direct.sdk.response_exception import ResponseException
from ingenico.direct.sdk.domain.create_hosted_checkout_request import CreateHostedCheckoutRequest
from ingenico.direct.sdk.domain.create_hosted_checkout_response import CreateHostedCheckoutResponse
from ingenico.direct.sdk.domain.error_response import ErrorResponse
from ingenico.direct.sdk.domain.get_hosted_checkout_response import GetHostedCheckoutResponse
from ingenico.direct.sdk.merchant.hostedcheckout.i_hosted_checkout_client import IHostedCheckoutClient


class HostedCheckoutClient(ApiResource, IHostedCheckoutClient):
    """
    HostedCheckout client. Thread-safe.
    """

    def __init__(self, parent, path_context):
        """
        :param parent:       :class:`ingenico.direct.sdk.api_resource.ApiResource`
        :param path_context: dict[str, str]
        """
        super(HostedCheckoutClient, self).__init__(parent, path_context)

    def create_hosted_checkout(self, body: CreateHostedCheckoutRequest, context: CallContext = None) -> CreateHostedCheckoutResponse:
        """
        Resource /v2/{merchantId}/hostedcheckouts - Create hosted checkout

        See also https://support.direct.ingenico.com/documentation/api/reference#operation/CreateHostedCheckoutApi

        :param body: :class:`ingenico.direct.sdk.domain.create_hosted_checkout_request.CreateHostedCheckoutRequest`
        :param context: :class:`ingenico.direct.sdk.call_context.CallContext`
        :return: :class:`ingenico.direct.sdk.domain.create_hosted_checkout_response.CreateHostedCheckoutResponse`
        :raise: ValidationException if the request was not correct and couldn't be processed (HTTP status code 400)
        :raise: AuthorizationException if the request was not allowed (HTTP status code 403)
        :raise: ReferenceException if an object was attempted to be referenced that doesn't exist or has been removed,
                   or there was a conflict (HTTP status code 404, 409 or 410)
        :raise: DirectException if something went wrong at the Ingenico ePayments platform,
                   the Ingenico ePayments platform was unable to process a message from a downstream partner/acquirer,
                   or the service that you're trying to reach is temporary unavailable (HTTP status code 500, 502 or 503)
        :raise: ApiException if the Ingenico ePayments platform returned any other error
        """
        uri = self._instantiate_uri("/v2/{merchantId}/hostedcheckouts", None)
        try:
            return self._communicator.post(
                    uri,
                    self._client_headers,
                    None,
                    body,
                    CreateHostedCheckoutResponse,
                    context)

        except ResponseException as e:
            error_type = ErrorResponse
            error_object = self._communicator.marshaller.unmarshal(e.body, error_type)
            raise self._create_exception(e.status_code, e.body, error_object, context)

    def get_hosted_checkout(self, hosted_checkout_id: str, context: CallContext = None) -> GetHostedCheckoutResponse:
        """
        Resource /v2/{merchantId}/hostedcheckouts/{hostedCheckoutId} - Get hosted checkout status

        See also https://support.direct.ingenico.com/documentation/api/reference#operation/GetHostedCheckoutApi

        :param hosted_checkout_id: str
        :param context: :class:`ingenico.direct.sdk.call_context.CallContext`
        :return: :class:`ingenico.direct.sdk.domain.get_hosted_checkout_response.GetHostedCheckoutResponse`
        :raise: ValidationException if the request was not correct and couldn't be processed (HTTP status code 400)
        :raise: AuthorizationException if the request was not allowed (HTTP status code 403)
        :raise: ReferenceException if an object was attempted to be referenced that doesn't exist or has been removed,
                   or there was a conflict (HTTP status code 404, 409 or 410)
        :raise: DirectException if something went wrong at the Ingenico ePayments platform,
                   the Ingenico ePayments platform was unable to process a message from a downstream partner/acquirer,
                   or the service that you're trying to reach is temporary unavailable (HTTP status code 500, 502 or 503)
        :raise: ApiException if the Ingenico ePayments platform returned any other error
        """
        path_context = {
            "hostedCheckoutId": hosted_checkout_id,
        }
        uri = self._instantiate_uri("/v2/{merchantId}/hostedcheckouts/{hostedCheckoutId}", path_context)
        try:
            return self._communicator.get(
                    uri,
                    self._client_headers,
                    None,
                    GetHostedCheckoutResponse,
                    context)

        except ResponseException as e:
            error_type = ErrorResponse
            error_object = self._communicator.marshaller.unmarshal(e.body, error_type)
            raise self._create_exception(e.status_code, e.body, error_object, context)
