from IPython.core.display import Image

from chosco.annotation.domain.aggregate_roots.media_item import MediaItem
from chosco.media.repository.domain.media_repository import MediaRepository


class HardcodedWebMediaRepository(MediaRepository):
    def retrieve(self, media_item: MediaItem, width: int = None, height: int = None) -> Image:
        try:
            return Image(media_item.media_id, unconfined=True, width=width, height=height)
        except:  # noqa
            raise IndexError(
                f"media_id {media_item.media_id} cannot be loaded on HardcodedWebMediaRepository"
            )
