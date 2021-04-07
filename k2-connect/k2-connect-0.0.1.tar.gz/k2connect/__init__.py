"""
This module handles the initialization of the k2connect library.
It takes a client id, secret and base url and initializes all k2connect
services as with appropriate required arguments.
"""
# TODO: Remember to remove http from validation
# TODO: David-dev branch is the one that is behind use the development branch which is the updated one
from k2connect import exceptions

import k2connect

from .authorization import TokenService
from .pay import PayService
from .result_processor import ResultProcessor
from .receive_payments import ReceivePaymentsService
from .transfers import TransferService
from . import validation
from .webhooks import WebhookService


Tokens = None
ReceivePayments = None
Pay = None
Transfers = None
Webhooks = None
ResultHandler = None


def initialize(client_id, client_secret, base_url, api_secret=None):
    """
    Initializes k2connect services
    :param base_url: The domain to use in the library.
    :type base_url: str
    :param client_id: Identifier for the k2 user.
    :type client_id: str
    :param client_secret: Secret key for k2 user.
    :type client_secret: str
    :param api_secret: API Secret key for processing webhook payloads.
    :type api_secret: str
    """
    validation.validate_string_arguments(client_id,
                                         client_secret,
                                         base_url)

    # initialize  token service
    globals()['Tokens'] = TokenService(client_id=client_id,
                                       client_secret=client_secret,
                                       base_url=base_url)

    # initialize stk service
    globals()['ReceivePayments'] = ReceivePaymentsService(base_url=base_url)

    # initialize Pay service
    globals()['Pay'] = PayService(base_url=base_url)

    # initialize transfers service
    globals()['Transfers'] = TransferService(base_url=base_url)

    # initialize webhook service
    globals()['Webhooks'] = WebhookService(base_url=base_url)

    # initialize response processor
    globals()['ResultHandler'] = ResultProcessor(base_url=base_url,
                                                 api_secret=api_secret)
