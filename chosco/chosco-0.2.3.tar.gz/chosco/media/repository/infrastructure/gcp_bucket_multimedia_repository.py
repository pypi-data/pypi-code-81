import os
from typing import Union

from IPython.core.display import Image, Video, HTML
from google.cloud import storage
from google.cloud.exceptions import NotFound
from google.cloud.storage import Blob
import base64
from chosco.annotation.domain.aggregate_roots.media_item import MediaItem
from chosco.media.repository.domain.media_repository import MediaRepository


class GoogleCloudMultimediaRepository(MediaRepository):
    def __init__(self):
        self.storage_client = storage.Client()

    def retrieve(self, media_item: MediaItem, width: int = None, height: int = None) -> Union[Image, Video]:
        try:
            blob = self._get_blob(media_item.media_id, media_item.media_bucket)
            data = blob.download_as_string(client=self.storage_client)
        except NotFound:
            raise Exception(
                f"Media {media_item.media_id} not found in Google Cloud repository"
            )
        extension = os.path.splitext(media_item.media_id)[-1].lower().replace(".", "")
        if extension in ["mp4", "avi", "mov"]:
            if extension == "mov":
                extension = "ogg" # "quicktime" It seems to work only with ogg mime
            elif extension == "avi":
                extension = "x-msvideo"
            return Video(data=base64.b64encode(data).decode(), embed=True,
                         width=width, height=height,
                         mimetype="video/{}".format(extension),
                         html_attributes="controls autoplay=autoplay")
        else:
            return Image(data=data, format="jpg", unconfined=False, width=width, height=height)

    def _get_blob(self, media_id: str, bucket_name: str) -> Blob:
        bucket = self.storage_client.get_bucket(bucket_name)
        blob = bucket.blob(media_id)
        return blob
