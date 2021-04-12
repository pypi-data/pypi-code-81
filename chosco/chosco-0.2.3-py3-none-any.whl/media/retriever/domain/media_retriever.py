from typing import Tuple

from chosco.annotation.domain.aggregate_roots.media_item import MediaItem
from chosco.annotation.domain.annotation_task_provider import AnnotationTaskProvider
from chosco.annotation.domain.annotation_task_status import AnnotationTaskStatus
from chosco.media.repository.domain.media_repository import MediaRepository

from IPython.core.display import Image


class MediaRetriever:
    def __init__(
        self,
        annotation_task_provider: AnnotationTaskProvider,
        repository: MediaRepository,
        image_width: int = 1200,
        image_height: int = None
    ):
        self.annotation_task_provider = annotation_task_provider
        self.repository = repository
        self.image_width = image_width
        self.image_height = image_height
        self.media_item = None

    def previous_media(self) -> Tuple[MediaItem, Image]:
        self.media_item = self.annotation_task_provider.previous()
        image = None
        if self.media_item:
            image = self.repository.retrieve(self.media_item, width=self.image_width, height=self.image_height)
        return self.media_item, image

    def next_media(self) -> Tuple[MediaItem, Image]:
        self.media_item = self.annotation_task_provider.next()
        image = None
        if self.media_item:
            image = self.repository.retrieve(self.media_item)

        return self.media_item, image

    def confirm(self, media_item):
        self.annotation_task_provider.confirm_current_task(media_item)

    def get_status(self) -> AnnotationTaskStatus:
        return self.annotation_task_provider.get_status()
