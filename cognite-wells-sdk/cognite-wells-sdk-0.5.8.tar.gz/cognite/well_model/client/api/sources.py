from typing import List

from requests import Response

from cognite.well_model.client._api_client import APIClient
from cognite.well_model.client.api.api_base import BaseAPI
from cognite.well_model.models import SourcesCreate


class SourcesAPI(BaseAPI):
    def __init__(self, wells_client: APIClient):
        super().__init__(wells_client)

    def ingest_sources(self, sources: List[str]) -> List[str]:
        path = self._get_path("/sources")
        json = SourcesCreate(items=sources).json()
        response: Response = self.wells_client.post(path, json)
        data: List[str] = response.json()
        return data

    def list_sources(self) -> List[str]:
        path = self._get_path("/sources")
        response: Response = self.wells_client.get(path)
        data: List[str] = response.json()
        return data
