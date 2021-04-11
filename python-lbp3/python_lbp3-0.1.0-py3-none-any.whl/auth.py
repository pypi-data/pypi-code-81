import backoff
import httpx

from .endpoints import Endpoints
from .exceptions import AuthError


class BearerAuth(httpx.Auth):
    """Adds bearer authentication when token known."""

    def __init__(
        self,
        host_url: str,
        token: str = None,
        username: str = None,
        password: str = None,
    ):
        self.host_url = host_url

        if token is not None:
            self.token = token

        elif username is not None and password is not None:
            self.username = username
            self.password = password
            self.refresh_token()

        else:
            raise AuthError(f"Must pass either token or username/password combination.")

        self._auth_header = self._build_auth_header()

    def _build_auth_header(self):
        return f"Bearer " + self.token

    def auth_flow(self, request):
        request.headers["Authorization"] = self._auth_header
        yield request

    @backoff.on_exception(backoff.expo, AuthError, max_tries=3)
    def refresh_token(self):
        if self.username is None or self.password is None:
            raise AuthError(f"Must pass either token or username/password combination.")

        try:
            r = httpx.post(
                self.host_url + Endpoints.ACCESS_TOKEN,
                data={"username": self.username, "password": self.password},
            )
            self.token = r.json()["access_token"]

        except:
            raise AuthError(f"Unable to refresh token - {r.text if r else None}")

    def _test_token(self):
        try:
            r = httpx.post(self.host_url + Endpoints.TEST_TOKEN, auth=self)
            if r.status_code != 200:
                raise AuthError(f"Invalid token - {r.text}")

        except Exception as e:
            raise AuthError(f"Unable to test token - {e}")
