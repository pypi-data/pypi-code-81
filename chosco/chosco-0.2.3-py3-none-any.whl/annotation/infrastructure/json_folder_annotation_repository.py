import json
import os

from chosco.annotation.domain.annotation import Annotation
from chosco.annotation.domain.annotation_repository import AnnotationRepository


class JsonFolderAnnotationRepository(AnnotationRepository):
    def __init__(self, output_folder: str):
        self.output_folder = output_folder
        os.makedirs(self.output_folder, exist_ok=True)
        self.username_filenames = {}
        self.user_annotations = {}

    def save(self, annotation: Annotation):
        if annotation.username not in self.username_filenames:
            filename = f"{self.output_folder}/{annotation.username}.json"
            self.username_filenames[annotation.username] = filename

        filename = self.username_filenames.get(annotation.username)
        if os.path.isfile(filename):
            with open(filename, "r") as infile:
                self.user_annotations = json.load(infile)

        self.user_annotations[annotation.id] = dict(
            internal_info=dict(annotator=annotation.username, media_id=annotation.id,
                               media_bucket=annotation.media_bucket), metadata=annotation.metadata)
        with open(filename, "w") as outfile:
            json.dump(self.user_annotations, outfile, indent=4)

    def retrieve(self, annotation_id: str, username: str) -> Annotation:
        if username not in self.username_filenames:
            raise ValueError(
                f"username {username} not exist in [{self.username_filenames.keys()}]"
            )

        filename = self.username_filenames.get(username)
        if not os.path.isfile(filename):
            raise ValueError(f"username filename {filename} not exist")

        with open(filename, "r") as infile:
            user_annotations = json.load(infile)
            if annotation_id not in user_annotations:
                raise ValueError(
                    f"annotation_id {annotation_id} not exist in [{user_annotations}]"
                )
            annotation_info = user_annotations.get(annotation_id)
            return Annotation(
                id=annotation_id,
                media_bucket=annotation_info['internal_info']['media_bucket'],
                username=username,
                metadata=annotation_info['metadata'],
            )

    def show(self):
        print(json.dumps(self.username_filenames, indent=4))
