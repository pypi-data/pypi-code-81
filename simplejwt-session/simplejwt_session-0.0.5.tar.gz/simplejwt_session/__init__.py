import os

import requests
from requests_toolbelt import sessions
from dotenv import load_dotenv

load_dotenv()


def get_auth_session(email=None, password=None, base_url=None, endpoint="/auth/token/"):
    """Given an email and password, logs into a Django API authenticated w/ `django-rest-framework-simplejwt` and returns an authenticated `requests.Session` instance. POSTs credentials to {base_url}/auth/token/ and caputres access token from the response. Also adds `base_url` to all session requests.

    Parameters
    ----------
    email : `str`, optional
        if `None`, uses environment variable `API_EMAIL`

    password : `str`, optional
        if `None`, uses environment variable `API_PASSWORD`

    endpoint : `str`, optional
        endpoint to get tokens from; default to "/auth/token/"

    base_url : `str`, optional
        base URL of API; if `None`, uses environment variable `API_BASE_URL`; avoid the last slash (/) in URL

    Returns
    -------
    `requests.Session`
        authenticated session
    """
    if(password == None):
        password = os.environ["API_PASSWORD"]
    if(email == None):
        email = os.environ["API_EMAIL"]
    if(base_url == None):
        base_url = os.environ["API_BASE_URL"]

    # get tokens
    url = f"{base_url}{endpoint}"
    body = {"password": password, "email": email}
    res = requests.post(url, data=body)
    res.raise_for_status()
    tokens = res.json()

    # generate auth header
    auth_header = f"Bearer {tokens['access']}"
    headers = {
        "Authorization": auth_header
    }

    # generate session w/ auth header
    auth_session = sessions.BaseUrlSession(base_url=base_url)
    auth_session.headers.update(headers)
    return auth_session
