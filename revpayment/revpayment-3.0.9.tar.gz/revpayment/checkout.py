import json
import urllib.request
from base64 import b64decode

import requests
from cryptography import x509
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from django.conf import settings
from django.shortcuts import redirect
from rest_framework import response

from revpayment.exceptions import (HttpActionError, InvalidCallback,
                                   PaymentException)
from revpayment.settings import api_settings

SNS_MESSAGE_TYPE_SUB_NOTIFICATION = "SubscriptionConfirmation"
SNS_MESSAGE_TYPE_NOTIFICATION = "Notification"
SNS_MESSAGE_TYPE_UNSUB_NOTIFICATION = "UnsubscribeConfirmation"


class CheckoutSDK:
    payment_classes = (
        ("neweb", api_settings.DEFAULT_NEWEB_CLASS),
        ("ecpay", api_settings.DEFAULT_ECPAY_CLASS),
        ("credit", api_settings.DEFAULT_CREDIT_CLASS),
    )
    handler_class = api_settings.HANDLER_CLASS
    fail_url = api_settings.DEFAULT_CHECKOUTFAIL_URL
    redirect_url = api_settings.DEFAULT_REDIRECT_URL
    redirect_query = api_settings.DEFAULT_REDIRECT_QUERY

    def __init__(self, state):
        self.state = state
        if type(state.cart) is str:
            self.cart = json.loads(state.cart)
        elif type(state.cart) is dict:
            self.cart = state.cart
        else:
            raise TypeError
        self.payment_type = state.payment_type
        self.payment_subtype = state.payment_subtype
        self.buyer = state.buyer

    def get_payment_class(self):
        try:
            payment_class = [
                c[1] for c in self.payment_classes if c[0] == self.payment_type
            ][0]
            return payment_class
        except IndexError:
            valids = [payment[0] for payment in self.payment_classes]
            raise exceptions.InvalidPaymentType(
                valids=valids, invalid=self.payment_type
            )

    def get_payment(self):
        payment_class = self.get_payment_class()
        return payment_class(
            buyer=self.buyer,
            payment_subtype=self.payment_subtype,
            cart=self.cart,
            order_id=self.state.order_id,
            order_type=self.state.order_type,
        )

    def checkout(self):
        try:
            payment = self.get_payment()
            result = payment.checkout()
            return redirect(result["url"])
        except PaymentException as e:
            return redirect(
                f"{self.fail_url}?error={e.error}&error_detail={e.error_detail}"
            )

    def callback(self, data):
        payment = self.get_payment()
        payment.callback(data)
        return response.Response({}, 200)

    def customer_redirect(self, data):
        payment = self.get_payment()
        order = payment.customer_redirect(data)
        return redirect(f"{self.redirect_url}?{self.redirect_query}={order.id}")


def canonical_message_builder(content, format):
    m = ""

    for field in sorted(format):
        try:
            m += field + "\n" + content[field] + "\n"
        except KeyError:
            # Build with what you have
            pass

    return m.encode()


def verify_sns_notification(request):
    cert = None
    pubkey = None
    canonical_message = None
    canonical_sub_unsub_format = [
        "Message",
        "MessageId",
        "SubscribeURL",
        "Timestamp",
        "Token",
        "TopicArn",
        "Type",
    ]
    canonical_notification_format = [
        "Message",
        "MessageId",
        "Subject",
        "Timestamp",
        "TopicArn",
        "Type",
    ]

    content = request.data
    decoded_signature = b64decode(content["Signature"])

    # Depending on the message type, canonical message format varies: http://goo.gl/oSrJl8
    if (
        request.META.get("HTTP_X_AMZ_SNS_MESSAGE_TYPE", None)
        == SNS_MESSAGE_TYPE_SUB_NOTIFICATION
        or request.META.get("HTTP_X_AMZ_SNS_MESSAGE_TYPE", None)
        == SNS_MESSAGE_TYPE_UNSUB_NOTIFICATION
    ):

        canonical_message = canonical_message_builder(
            content, canonical_sub_unsub_format
        )

    elif (
        request.META.get("HTTP_X_AMZ_SNS_MESSAGE_TYPE", None)
        == SNS_MESSAGE_TYPE_NOTIFICATION
    ):

        canonical_message = canonical_message_builder(
            content, canonical_notification_format
        )

    else:
        raise ValueError(
            "Message Type (%s) is not recognized"
            % request.META.get("HTTP_X_AMZ_SNS_MESSAGE_TYPE", None)
        )

    # Load the certificate and extract the public key
    cert_string = urllib.request.urlopen(content["SigningCertURL"]).read()

    cert = x509.load_pem_x509_certificate(cert_string, default_backend())
    pubkey: rsa.RSAPublicKey = cert.public_key()
    try:
        pubkey.verify(
            decoded_signature,
            canonical_message,
            PKCS1v15(),
            hashes.SHA1(),
        )
        return True
    except InvalidSignature:
        raise InvalidCallback()


def confirm_subcription(data):
    if settings.STAGE == "prod":
        host = api_settings.PAYMENT_HOST
    else:
        host = api_settings.PAYMENT_DEBUG_HOST

    full_url = f"{host}/{api_settings.PAYMENT_VERSION}/subscription/confirm?client_id={settings.CLIENT_ID}&client_secret={settings.CLIENT_SECRET}"

    try:
        resp = requests.post(full_url, json={"token": data["Token"]})
        resp.raise_for_status()
        return resp.json()
    except requests.HTTPError as exc:
        err_resp = exc.response
        if err_resp.status_code >= 500:
            detail = "internal server error"
        else:
            detail = err_resp.json()["detail"]
        raise HttpActionError(status_code=err_resp.status_code, detail=detail)
