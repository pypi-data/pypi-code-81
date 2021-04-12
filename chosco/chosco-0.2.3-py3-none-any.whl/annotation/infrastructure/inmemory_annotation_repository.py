import json

from chosco.annotation.domain.annotation import Annotation
from chosco.annotation.domain.annotation_repository import AnnotationRepository


class InMemoryAnnotationRepository(AnnotationRepository):
    def __init__(self):
        self.items = {}

    def save(self, annotation: Annotation):
        if annotation.username not in self.items:
            self.items[annotation.username] = {}
        self.items[annotation.username][annotation.id] = dict(
            internal_info=dict(annotator=annotation.username, media_id=annotation.id,
                               media_bucket=annotation.media_bucket),
            metadata=annotation.metadata
        )

    def retrieve(self, annotation_id: str, username: str) -> Annotation:
        if username not in self.items:
            raise ValueError(f"username {username} not exist in [{self.items.keys()}]")

        username_items = self.items.get(username)

        if annotation_id not in username_items:
            raise ValueError(
                f"annotation_id {username} not exist in [{username_items}]"
            )

        return username_items.get(annotation_id)['metadata']

    def show(self):
        print(json.dumps(self.items, indent=4))
