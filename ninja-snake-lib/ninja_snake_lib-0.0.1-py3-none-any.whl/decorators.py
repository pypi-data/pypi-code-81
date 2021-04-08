import json
import logging
import os
import requests
from django.http import HttpResponse

logger = logging.getLogger(__name__)


def validate_external_api_key(function):
    def wrap(request, *args, **kwargs):

        if os.getenv("VALIDATE_EXTERNAL_ACCESS_API_KEY") == "false":
            return function(request, *args, **kwargs)

        api_key = request.META.get("HTTP_AUTHORIZATION")

        if not api_key:
            logger.warning("Request sem header HTTP_AUTHORIZATION")
            raise GNPermissionDenied()

        if api_key == f"Bearer {os.getenv('EXTERNAL_ACCESS_API_KEY')}":
            return function(request, *args, **kwargs)
        else:
            logger.warning("Request com header HTTP_AUTHORIZATION errado")
            raise GNPermissionDenied()

    return wrap


def validate_sns_subscription(function):

    def wrap(request, *args, **kwargs):

        payload = json.loads(request.body.decode('utf-8'))
        message_type = request.META.get('HTTP_X_AMZ_SNS_MESSAGE_TYPE')

        if message_type == 'SubscriptionConfirmation':
            subscribe_url = payload.get('SubscribeURL')
            res = requests.get(subscribe_url)
            if res.status_code != 200:
                return HttpResponse(
                    'Invalid verification:\n{res.content}', status=400)
            else:
                return HttpResponse('OK')
        return function(request, *args, **kwargs)

    return wrap


class GNPermissionDenied(Exception):
    pass
