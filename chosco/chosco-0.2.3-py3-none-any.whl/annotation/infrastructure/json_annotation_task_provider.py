import json
from datetime import datetime
from typing import List

from chosco.annotation.domain.aggregate_roots.media_item import MediaItem
from chosco.annotation.domain.annotation_task_provider import AnnotationTaskProvider
from chosco.annotation.domain.annotation_task_status import AnnotationTaskStatus


class JsonAnnotationTaskProvider(AnnotationTaskProvider):
    @staticmethod
    def from_filename(filename: str):
        with open(filename, "r") as infile:
            kdict = json.load(infile)
            done = kdict.get("done")
            done_media_items = (
                [MediaItem.from_dict(media_dict) for media_dict in done]
                if done
                else None
            )
            pending = kdict.get("pending")
            pending_media_items = (
                [MediaItem.from_dict(media_dict) for media_dict in pending]
                if pending
                else None
            )

            return JsonAnnotationTaskProvider(
                done_media_items,
                pending_media_items,
                kdict.get("session_id"),
                kdict.get("current_task_index"),
                filename,
            )

    @staticmethod
    def create(tasks: List[MediaItem], session_id: str):
        done = list()
        pending = tasks
        return JsonAnnotationTaskProvider(done, pending, session_id)

    def __init__(
        self,
        done: List[MediaItem],
        pending: List[MediaItem],
        session_id: str,
        current_task_index: int = None,
        filename: str = None,
    ):
        self.done = done if isinstance(done, list) else list()
        self.pending = pending if isinstance(pending, list) else list()
        self.total_tasks = self.done + self.pending
        self.current_task_index = current_task_index

        self.session_id = session_id
        self.updated_at = None
        if self.pending is None or len(self.pending) < 1:
            raise AttributeError(
                f"Pending documents must have at least a task. {self.to_dict()}"
            )
        self.current_task = None
        self.filename = filename

    def to_dict(self):
        return {
            "updated_at": self.updated_at,
            "number_of_annotations": self.get_number_of_annotations(),
            "number_pending_annotations": self.get_number_pending_annotations(),
            "done": [field_item.to_dict() for field_item in self.done],
            "pending": [field_item.to_dict() for field_item in self.pending],
            "session_id": self.session_id,
            "current_task_index": self.current_task_index,
        }

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4)

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def save(self, filename):
        self.filename = filename
        with open(filename, "w") as outfile:
            json.dump(self.to_dict(), outfile, indent=4)

    def save_snapshot(self):
        if self.filename:
            self.save(self.filename)

    def get_current_index(self):
        return self.current_task_index

    def get_number_of_annotations(self):
        return len(self.done) if self.done else 0

    def get_number_pending_annotations(self):
        return len(self.pending) if self.pending else 0

    def get_total_annotations(self):
        return len(self.total_tasks)

    def get_status(self):
        return AnnotationTaskStatus(
            index=self.get_current_index(),
            number_of_annotations=self.get_number_of_annotations(),
            total_annotations=self.get_total_annotations(),
            current_task=self.current_task,
        )

    def next(self) -> MediaItem:
        self.current_task_index = (
            -1 if self.current_task_index is None else self.current_task_index
        )
        try:
            if self.current_task_index >= len(self.total_tasks) - 1:
                self.current_task = None
            else:
                self.current_task_index += 1
                self.current_task = self.total_tasks[self.current_task_index]
        except IndexError:
            self.current_task = None
        return self.current_task

    def previous(self) -> MediaItem:
        if self.current_task_index is None or self.current_task_index < 1:
            self.current_task = None
        else:
            self.current_task_index -= 1
            self.current_task = self.total_tasks[self.current_task_index]

        return self.current_task

    def confirm_current_task(self, task: MediaItem):
        if len(self.pending) > 0:
            try:
                self.pending.remove(task)
                self.done.append(task)
                self.updated_at = datetime.utcnow().strftime("%B %d %Y - %H:%M:%S")
                self.save_snapshot()
            except ValueError:
                pass
