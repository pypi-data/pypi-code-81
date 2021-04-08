import requests
from mlploy.config import api_base_url


def version():
    resp = requests.get(f"{api_base_url}/version").json()
    return resp
