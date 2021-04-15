"""
kerfed_api
----------

Python helper library for using the Kerfed Engine.
"""
import os

from .shop import _Shop
from .order import _Order
from .quote import _Quote


# set the default request timeout period in milliseconds
_TIMEOUT = 15000

# set the root URL of the Kerfed v1 REST API
# note that you can override the default by setting
# your preferred value as an environment variable.
_API_ROOT = os.environ.get(
    'KERFED_API_ROOT',
    'https://kerfed.com/api/v1')

# get API key if set as an environment variable
# if this isn't set you can live-patch the value
# in your script `kerfed_api.API_KEY = '.......'`
API_KEY = os.environ.get('KERFED_API_KEY', None)


# create simple parent classes for our main objects
# so that the API URL and key can be passed automatically
# from this top library level on object instantiation.
class Shop(_Shop):
    def __init__(self, *args, **kwargs):
        self._TIMEOUT = _TIMEOUT
        self._API_ROOT = _API_ROOT
        self._API_KEY = API_KEY
        super(Shop, self).__init__(*args, **kwargs)


class Order(_Order):
    def __init__(self, *args, **kwargs):
        self._TIMEOUT = _TIMEOUT
        self._API_ROOT = _API_ROOT
        self._API_KEY = API_KEY
        super(Order, self).__init__(*args, **kwargs)


class Quote(_Quote):
    def __init__(self, *args, **kwargs):
        self._TIMEOUT = _TIMEOUT
        self._API_ROOT = _API_ROOT
        self._API_KEY = API_KEY
        # save reference to Order object
        self._ORDER = Order
        super(Quote, self).__init__(*args, **kwargs)
