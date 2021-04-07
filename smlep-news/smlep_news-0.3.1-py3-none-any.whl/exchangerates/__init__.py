import requests

from .rates import Rates

url = "http://api.exchangeratesapi.io/v1/latest"


def get_exchange_rates(key):
    full_url = f"{url}?access_key={key}"
    r = requests.get(full_url)
    r.raise_for_status()

    return Rates(r.json())
