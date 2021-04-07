import logging

from django.conf import settings
import json

from nhst_log_request_id import DEFAULT_NO_REQUEST_ID, LOG_REQUESTS_NO_SETTING, REQUEST_ID_PROPERTY_NAME_SETTING, DEFAULT_REQUEST_ID_PROPERTY_NAME, local


class RequestIDFilter(logging.Filter):

     def filter(self, record):
        default_request_id = getattr(settings, LOG_REQUESTS_NO_SETTING, DEFAULT_NO_REQUEST_ID)
        request_id_property_name = getattr(settings, REQUEST_ID_PROPERTY_NAME_SETTING, DEFAULT_REQUEST_ID_PROPERTY_NAME)
        request_id_property_value = getattr(local, request_id_property_name, default_request_id)
        setattr(record, request_id_property_name, request_id_property_value)
        return True
