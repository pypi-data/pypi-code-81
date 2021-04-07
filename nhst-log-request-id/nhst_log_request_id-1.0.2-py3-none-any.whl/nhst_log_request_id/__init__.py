import threading

__version__ = "1.0.2"


local = threading.local()


REQUEST_ID_HEADER_SETTING = 'LOG_REQUEST_ID_HEADER'
LOG_REQUESTS_SETTING = 'LOG_REQUESTS'
LOG_REQUESTS_NO_SETTING = 'NO_REQUEST_ID'
LOG_USER_ATTRIBUTE_SETTING = 'LOG_USER_ATTRIBUTE'
DEFAULT_NO_REQUEST_ID = "none"  # Used if no request ID is available
REQUEST_ID_RESPONSE_HEADER_SETTING = 'REQUEST_ID_RESPONSE_HEADER'
OUTGOING_REQUEST_ID_HEADER_SETTING = 'OUTGOING_REQUEST_ID_HEADER'
GENERATE_REQUEST_ID_IF_NOT_IN_HEADER_SETTING = 'GENERATE_REQUEST_ID_IF_NOT_IN_HEADER'
REQUEST_ID_PROPERTY_NAME_SETTING = 'REQUEST_ID_PROPERTY_NAME'
DEFAULT_REQUEST_ID_PROPERTY_NAME = 'request_id'