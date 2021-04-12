import json
from uuid import uuid4

import numpy as np
from datetime import datetime
from typing import List, Dict

from chosco.annotation.domain.aggregate_roots.media_item import MediaItem


class AnnotationSession:
    @staticmethod
    def create(
        media_items: List[MediaItem],
        users: List[str],
        number_of_annotations_per_media: int,
    ):
        created_at = datetime.utcnow().strftime("%B %d %Y - %H:%M:%S")
        users = users
        number_of_media_items = len(media_items)
        number_of_users = len(users)
        number_of_annotations_per_media = number_of_annotations_per_media

        media_items_indexes = np.repeat(
            np.arange(number_of_media_items), number_of_annotations_per_media
        )
        tasks_list = [[] for i in range(number_of_users)]
        for i, idx in enumerate(media_items_indexes):
            row_id = i % number_of_users
            tasks_list[row_id].append(media_items[idx])

        tasks = {}
        for i, user in enumerate(users):
            tasks[user] = tasks_list[i]

        return AnnotationSession(
            str(uuid4()),
            created_at,
            number_of_media_items,
            number_of_users,
            number_of_annotations_per_media,
            tasks,
        )

    def __init__(
        self,
        id: str,
        created_at: str,
        number_of_ids: int,
        number_of_users: int,
        number_of_annotations_per_media: int,
        tasks: Dict[str, List[MediaItem]],
    ):
        self.id = id
        self.created_at = created_at
        self.number_of_ids = number_of_ids
        self.number_of_users = number_of_users
        self.number_of_annotations_per_media = number_of_annotations_per_media
        self.tasks = tasks

    def to_dict(self):
        tasks_dict = {}
        for username, tasks in self.tasks.items():
            tasks_dict[username] = []
            for media_item in tasks:
                tasks_dict[username].append(media_item.to_dict())

        return {
            "id": self.id,
            "created_at": self.created_at,
            "number_of_ids": self.number_of_ids,
            "number_of_users": self.number_of_users,
            "number_of_annotations_per_media": self.number_of_annotations_per_media,
            "tasks": tasks_dict,
        }

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4)

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def save(self, filename):
        with open(filename, "w") as outfile:
            json.dump(self.to_dict(), outfile, indent=4)

    @staticmethod
    def from_filename(filename):
        with open(filename, "r") as infile:
            kdict = json.load(infile)
            tasks = kdict.get("tasks")
            if tasks:
                tasks_dict = {}
                for username, tasks_list in tasks.items():
                    tasks_dict[username] = []
                    for media_item in tasks_list:
                        tasks_dict[username].append(MediaItem.from_dict(media_item))
            else:
                tasks_dict = tasks
            return AnnotationSession(
                kdict.get("id"),
                kdict.get("created_at"),
                kdict.get("number_of_ids"),
                kdict.get("number_of_users"),
                kdict.get("number_of_annotations_per_media"),
                tasks_dict,
            )

    def get_tasks_by_user(self, username: str) -> List[MediaItem]:
        return self.tasks.get(username)
