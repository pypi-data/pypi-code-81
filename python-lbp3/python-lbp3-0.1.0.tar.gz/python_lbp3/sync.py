import httpx
from .auth import BearerAuth
from .endpoints import Endpoints
from . import exceptions as exc


class SyncClient:
    """Client for creating synchronous connections to the LBP3 Data api."""

    def __init__(self, auth: BearerAuth):
        self.auth = auth
        self.host_url = auth.host_url
        # Validate
        self.auth._test_token()

    def _validate_response(self, r: httpx.Response):
        if 200 <= r.status_code < 299:
            return r.json()
        else:
            try:
                error = dict(r.json())
                error["status"] = r.status_code
            except:
                error = dict(text=r.text, status=r.status_code)

        if r.status_code == 404:
            raise exc.NotFound(error)
        elif r.status_code == 403:
            raise exc.Forbidden(error)
        elif r.status_code == 400:
            raise exc.BadRequest(error)
        elif r.status_code == 401:
            raise exc.Unauthorized(error)
        elif r.status_code == 422:
            raise exc.UnprocessableEntity(error)
        elif r.status_code == 500:
            raise exc.ServerError(error)
        else:
            raise exc.OtherResponseError(error)

    def get(self, endpoint: str, params: dict = {}):
        r = httpx.get(self.host_url + endpoint, auth=self.auth, params=params)
        return self._validate_response(r)

    def post(self, endpoint: str, params: dict = {}, data: dict = {}):
        r = httpx.post(
            self.host_url + endpoint, auth=self.auth, params=params, json=data
        )
        return self._validate_response(r)

    def put(self, endpoint: str, params: dict = {}, data: dict = {}):
        r = httpx.put(
            self.host_url + endpoint, auth=self.auth, params=params, json=data
        )
        return self._validate_response(r)

    def delete(self, endpoint: str, params: dict = {}):
        r = httpx.delete(self.host_url + endpoint, auth=self.auth, params=params)
        return self._validate_response(r)

    def me(self):
        """Returns information out myself as user."""
        return self.get(endpoint=Endpoints.ME)

    def users(self, skip=0, limit=100):
        """Returns all users as a list."""
        return self.get(endpoint=Endpoints.USERS, params=dict(skip=skip, limit=limit))

    def assets(self, skip=0, limit=100):
        """Returns all assets as a list."""
        return self.get(endpoint=Endpoints.ASSETS, params=dict(skip=skip, limit=limit))

    def periodicities(self, skip=0, limit=100):
        """Returns all periodicities as a list."""
        return self.get(
            endpoint=Endpoints.PERIODICITIES, params=dict(skip=skip, limit=limit)
        )

    def patterns(self, skip=0, limit=100):
        """Returns all patterns as a list."""
        return self.get(
            endpoint=Endpoints.PATTERNS, params=dict(skip=skip, limit=limit)
        )
