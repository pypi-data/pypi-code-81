from media_platform.http_client.authenticated_http_client import AuthenticatedHTTPClient
from media_platform.service.media_platform_service import MediaPlatformService
from media_platform.service.visual_search_service.index_image_request import IndexImageRequest
from media_platform.service.visual_search_service.find_similar_images_request import FindSimilarImagesRequest


class VisualSearchService(MediaPlatformService):
    def __init__(self, domain: str, authenticated_http_client: AuthenticatedHTTPClient):
        super(VisualSearchService, self).__init__(domain, authenticated_http_client)

    def index_image_request(self) -> IndexImageRequest:
        return IndexImageRequest(self._authenticated_http_client, self._base_url)

    def find_similar_images_request(self) -> FindSimilarImagesRequest:
        return FindSimilarImagesRequest(self._authenticated_http_client, self._base_url)
