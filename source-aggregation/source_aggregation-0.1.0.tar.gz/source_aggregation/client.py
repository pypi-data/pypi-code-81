import logging
import uuid
from os.path import join

import requests

from .utils import to_json


class ApiClient:
    """
    Client that exposes required source aggregation service endpoints

    Adds logging and tracing of requests and responses in debug mode. Raises on errors during request.
    """

    def __init__(self, endpoint, token):
        self._endpoint = endpoint
        self._token = token
        self.artifacts = Artifact(self)

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


class Artifact:
    def __init__(self, client):
        self.client = client

    def list(self, params: dict = None):
        response = self.client.exec_request(
            method="GET",
            url=self.client.build_url("artifact"),
            params=(params or {}),
        )
        return response or []

    def get(self, artifact_id: str):
        response = self.client.exec_request(
            method="GET",
            url=self.client.build_url(f"artifact/{artifact_id}"),
        )
        return response or {}

    def export(self, artifacts):
        ids = ",".join(str(artifact.get("id")) for artifact in artifacts)
        response = self.client.exec_request(
            method="POST",
            url=self.client.build_url(f"artifact/{ids}/export"),
        )
        return response.get("id") or []

    def ignore(self, artifacts):
        ids = ",".join(str(artifact.get("id")) for artifact in artifacts)
        response = self.client.exec_request(
            method="POST",
            url=self.client.build_url(f"artifact/{ids}/ignore"),
        )
        return response.get("id") or []
