import requests

import src
from src.client.base import FlowfusicHttpClient
from src.exceptions import AuthenticationException
from src.log import logger
from src.model.user import User


class AuthClient(FlowfusicHttpClient):
    """
    Auth/User specific client
    """

    def __init__(self):
        self.base_url = f"{src.FLOWFUSIC_HOST}/api/v1/user/"

    def get_user(self, access_token, is_apikey=False):
        # This is a special case client, because auth_token is not set yet
        # (this is how we verify it)
        # So do not use the shared base client for this!
        logger.info("Logging to %s", self.base_url)

        if is_apikey:
            auth = f"apikey {access_token}"
        else:
            auth = f"Bearer {access_token}"
        response = requests.get(self.base_url, headers={"Authorization": auth})
        try:
            user_dict = response.json()
            response.raise_for_status()
        except Exception:
            if response.status_code == 401:
                raise AuthenticationException(
                    "Invalid Token.\nSee http://flowfusic.com/ for help"
                )  # noqa
            raise AuthenticationException(
                "Login failed.\nSee http://flowfusic.com/ for help"
            )

        return User.from_dict(user_dict)

    def login(self, credentials):
        # This is another special case client, because auth_token is not set yet
        # (this is how we get the token)
        # So do not use the shared base client for this!
        response = requests.post("%slogin" % self.base_url, json=credentials.to_dict())
        try:
            token_dict = response.json()
            response.raise_for_status()
        except Exception:
            if response.status_code == 401:
                raise AuthenticationException("Invalid credentials")
            raise AuthenticationException(
                "Login failed. Please try logging in using the token. "
                "Run login command without username and password parameters."
            )

        return token_dict.get("access_token")
