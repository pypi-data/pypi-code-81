from abc import ABC, abstractmethod
from typing import Any

from chosco.annotation.domain.aggregate_roots.media_item import MediaItem


class MediaRepository(ABC):
    @abstractmethod
    def retrieve(self, media_item: MediaItem, width: int = None, height: int = None) -> Any:
        raise NotImplementedError
