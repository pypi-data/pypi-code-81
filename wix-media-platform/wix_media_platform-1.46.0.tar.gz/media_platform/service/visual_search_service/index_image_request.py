from __future__ import annotations

from media_platform.http_client.authenticated_http_client import AuthenticatedHTTPClient
from media_platform.job.index_image_job import IndexImageJob
from media_platform.service.callback import Callback
from media_platform.service.media_platform_request import MediaPlatformRequest
from media_platform.service.source import Source


class IndexImageRequest(MediaPlatformRequest):
    def __init__(self, authenticated_http_client: AuthenticatedHTTPClient, base_url: str):
        super().__init__(authenticated_http_client, 'POST', f'{base_url}/visual_search', IndexImageJob)

        self.source = None
        self.callback = None
        self.collection_id = None

    def set_source(self, source: Source) -> IndexImageRequest:
        self.source = source
        return self

    def set_collection_id(self, collection_id: str) -> IndexImageRequest:
        self.collection_id = collection_id
        return self

    def set_callback(self, callback: Callback):
        self.callback = callback
        return self

    def execute(self):
        self.url = f'{self.url}/collections/{self.collection_id}/index'
        return super().execute()

    def _params(self) -> dict:
        return {
            'source': self.source.serialize(),
            'jobCallback': self.callback.serialize() if self.callback else None,
            'specification': None,
        }
