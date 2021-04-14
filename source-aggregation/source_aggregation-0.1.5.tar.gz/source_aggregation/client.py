import logging
import typing
import uuid
from os.path import join

import requests

from .utils import to_json

ArtifactId = typing.Union[int, str]


class ApiClient:
    resources = {}

    def __init__(self, endpoint, token):
        self._endpoint = endpoint
        self._token = token

    def __getattr__(self, name):
        return self.__class__.resources[name](self._endpoint, self._token)


class _BaseClient:
    """
    Client that exposes required source aggregation service endpoints

    Adds logging and tracing of requests and responses in debug mode. Raises on errors during request.
    """

    def __init__(self, endpoint, token):
        self._endpoint = endpoint
        self._token = token

    def __init_subclass__(cls, /, resource_name=None, **kwargs):
        super().__init_subclass__(**kwargs)
        ApiClient.resources[resource_name] = cls

    def exec_request(self, method, url, **kwargs):
        """ Executes a request, assigning a unique id beforehand and throwing on 4xx / 5xx """
        reqid = str(uuid.uuid4())

        logging.debug(
            f"{self.__class__.__qualname__} -> {method.upper()} {url} {reqid=}"
        )

        # requests.post / requests.get / ...
        method_exec = getattr(requests, method.lower())

        headers = self._build_headers()
        response = method_exec(url, headers=headers, **kwargs)

        status_code = response.status_code
        content_length = len(response.content or "")
        logging.debug(
            f"{self.__class__.__qualname__} <- {status_code} {content_length} {reqid=}"
        )

        # raise by default to halt further exec and bubble
        response.raise_for_status()

        return to_json(response)

    def build_url(self, *paths):
        return join(self._endpoint, *paths)

    def _build_headers(self):
        return {
            "Accept": "application/json",
            "User-Agent": "SAS-Python/0.0.1",
            "Authorization": f"Bearer {self._token}",
        }


class Artifact(_BaseClient, resource_name="artifacts"):
    def list(self, params: dict = None) -> dict:
        response = self.exec_request(
            method="GET",
            url=self.build_url("artifact"),
            params=(params or {}),
        )
        return response or {}

    def get(self, artifact_id: str) -> dict:
        response = self.exec_request(
            method="GET",
            url=self.build_url(f"artifact/{artifact_id}"),
        )
        return response or {}

    def export(self, artifacts) -> list:
        ids = ",".join(str(artifact.get("id")) for artifact in artifacts)
        response = self.exec_request(
            method="POST",
            url=self.build_url(f"artifact/{ids}/export"),
        )
        return response.get("id") or []

    def ignore(self, artifacts) -> list:
        ids = ",".join(str(artifact.get("id")) for artifact in artifacts)
        response = self.exec_request(
            method="POST",
            url=self.build_url(f"artifact/{ids}/ignore"),
        )
        return response.get("id") or []
