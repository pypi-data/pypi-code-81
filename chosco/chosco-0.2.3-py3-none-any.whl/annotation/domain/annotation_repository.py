from abc import ABC, abstractmethod

from chosco.annotation.domain.annotation import Annotation


class AnnotationRepository(ABC):
    @abstractmethod
    def save(self, annotation: Annotation):
        raise NotImplementedError

    @abstractmethod
    def retrieve(self, annotation_id: str, username: str) -> Annotation:
        raise NotImplementedError

    @abstractmethod
    def show(self):
        raise NotImplementedError
