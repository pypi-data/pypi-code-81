from IPython.core.display import Image
from google.cloud import storage
from google.cloud.exceptions import NotFound
from google.cloud.storage import Blob

from chosco.annotation.domain.aggregate_roots.media_item import MediaItem
from chosco.media.repository.domain.media_repository import MediaRepository


class GoogleCloudMediaRepository(MediaRepository):
    def __init__(self):
        self.storage_client = storage.Client()

    def retrieve(self, media_item: MediaItem, width: int = None, height: int = None) -> Image:
        try:
            blob = self._get_blob(media_item.media_id, media_item.media_bucket)
            data = blob.download_as_string(client=self.storage_client)
        except NotFound:
            raise Exception(
                f"Media {media_item.media_id} not found in Google Cloud repository"
            )

        return Image(data=data, format="jpg", unconfined=False, width=width, height=height)

    def _get_blob(self, media_id: str, bucket_name: str) -> Blob:
        bucket = self.storage_client.get_bucket(bucket_name)
        blob = bucket.blob(media_id)
        return blob
