from abc import ABC, abstractmethod

from chosco.annotation.domain.aggregate_roots.media_item import MediaItem


class AnnotationTaskProvider(ABC):
    @abstractmethod
    def get_number_of_annotations(self):
        raise NotImplementedError

    @abstractmethod
    def get_number_pending_annotations(self):
        raise NotImplementedError

    @abstractmethod
    def get_total_annotations(self):
        raise NotImplementedError

    @abstractmethod
    def get_status(self):
        raise NotImplementedError

    @abstractmethod
    def next(self) -> MediaItem:
        raise NotImplementedError

    @abstractmethod
    def previous(self) -> MediaItem:
        raise NotImplementedError

    @abstractmethod
    def confirm_current_task(self, task: MediaItem):
        raise NotImplementedError
