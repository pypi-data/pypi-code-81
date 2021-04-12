import json
import time

import requests
from yarl import URL

ONE_THOUSAND_YEARS_IN_SECONDS = 1000 * 365 * 24 * 3600


class PostRequestError(Exception):
    def __init__(self, response):
        self.message = f"Error status code: {response.status_code}"
        super().__init__(self.message)


class RefreshTokenExpirationError(Exception):
    def __init__(self, response):
        self.message = "The refresh token expired. We need to re-authentificate."
        super().__init__(self.message)


class AuthentificationError(Exception):
    def __init__(self, response):
        self.message = "You are not authentificate. Please run `Authentification.create(scope)` or load tokens using `Authentification.from_json(filename)`."
        super().__init__(self.message)


class Authentification(object):

    base_url = "{}/auth/realms/ELG/protocol/openid-connect/auth"
    token_url = "{}/auth/realms/ELG/protocol/openid-connect/token"
    client = "python-sdk"
    redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
    live_domain = "https://live.european-language-grid.eu"
    dev_domain = "https://dev.european-language-grid.eu"

    def __init__(self):
        self.access_token = None
        self.expires_in = None
        self.expires_time = time.gmtime(0)
        self.refresh_expires_in = None
        self.refresh_expires_time = time.gmtime(0)
        self.refresh_token = None
        self.token_type = None
        self.id_token = None
        self.not_before_policy = None
        self.session_state = None
        self.scope = None
        self.domain = None

    def __str__(self):
        return f"Authentification(valid_until: {time.strftime('%Y-%m-%dT%H:%M:%SZ', self.expires_time)})"

    def __repr__(self):
        obj = self.__dict__.copy()
        obj["access_token"] = "*****"
        obj["refresh_token"] = "*****"
        obj["id_token"] = "*****"
        return str(obj)

    def create(self, scope="openid"):
        auth_url = URL(self.base_url.format(self.domain)).with_query(
            client_id=self.client, redirect_uri=self.redirect_uri, response_type="code", scope=scope
        )
        print("Please go to this URL in your browser: {}".format(auth_url.human_repr()))
        print("")
        auth_code = input('Paste the "success code": ')
        data = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client,
        }
        self._requesting_oauth_token(data)

    def refresh(self):
        if self.refresh_token == None:
            raise AuthentificationError()
        data = {"grant_type": "refresh_token", "client_id": self.client, "refresh_token": self.refresh_token}
        self._requesting_oauth_token(data)

    def refresh_if_needed(self):
        # refresh if the token will expire in less than 60 seconds
        # idea from: https://stackoverflow.com/questions/30826726/how-to-identify-if-the-oauth-token-has-expired
        if time.gmtime(time.time() + 60) > self.expires_time:
            if time.gmtime() > self.refresh_expires_time:
                raise RefreshTokenExpirationError()
            if time.gmtime(time.time() + 3600) > self.refresh_expires_time:
                print(
                    f"Warning: the refresh token will expired in {time.mktime(time.gmtime()) - time.mktime(self.refresh_expires_time)} seconds"
                )
            self.refresh()

    def _requesting_oauth_token(self, data):
        response = requests.post(self.token_url.format(self.domain), data=data)
        if not response.ok:
            raise PostRequestError(response)
        tokens = response.json()
        self.access_token = tokens["access_token"]
        self.expires_in = tokens["expires_in"]
        self.expires_time = time.gmtime(time.time() + self.expires_in)
        self.refresh_expires_in = tokens["refresh_expires_in"]
        self.refresh_expires_time = time.gmtime(
            time.time() + (self.refresh_expires_in if self.refresh_expires_in != 0 else ONE_THOUSAND_YEARS_IN_SECONDS)
        )
        self.refresh_token = tokens["refresh_token"]
        self.token_type = tokens["token_type"]
        self.id_token = tokens.get(
            "id_token"
        )  # use get to not raise an error if there is no id_token (for offline_access)
        self.not_before_policy = tokens["not-before-policy"]
        self.session_state = tokens["session_state"]
        self.scope = tokens["scope"]

    def to_json(self, filemame):
        with open(filemame, "w") as f:
            json.dump(self.__dict__, f, indent="\t")

    @classmethod
    def init(cls, scope="openid", domain="live"):
        authentification = cls()
        if domain == "live":
            authentification.domain = cls.live_domain
        elif domain == "dev":
            authentification.domain = cls.dev_domain
        elif isinstance(domain, str):
            authentification.domain = domain
        else:
            raise ValueError(
                "domain argument must be a string. 'live' to use the live cluster, 'dev' to use the dev cluster or 'custum.domain.name' to use a local cluster."
            )
        authentification.create(scope)
        return authentification

    @classmethod
    def from_json(cls, filename):
        with open(filename, "r") as f:
            tokens = json.load(f)
        authentification = cls()
        authentification.access_token = tokens["access_token"]
        authentification.expires_in = tokens["expires_in"]
        authentification.expires_time = time.struct_time(tokens["expires_time"])
        authentification.refresh_expires_in = tokens["refresh_expires_in"]
        authentification.refresh_expires_time = time.struct_time(tokens["refresh_expires_time"])
        authentification.refresh_token = tokens["refresh_token"]
        authentification.token_type = tokens["token_type"]
        authentification.id_token = tokens["id_token"]
        authentification.not_before_policy = tokens["not_before_policy"]
        authentification.session_state = tokens["session_state"]
        authentification.scope = tokens["scope"]
        authentification.domain = tokens["domain"]
        return authentification
