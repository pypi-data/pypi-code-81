from typing import List
from .qradarmodel import QRadarModel


class SavedSearchGroup(QRadarModel):

    def __init__(self, *, id: int = None, parent_id: int = None, type: str = None, level: int = None, name: str = None, description: str = None,  owner: str = None, modified_time: int = None, child_group_ids: List[int] = None):
        """
        Args:
            id (int, optional): The ID of the group. Defaults to None.
            parent_id (int, optional): The ID of the parent group (default resources can have localized names). Defaults to None.
            type (str, optional): The type of the group. Defaults to None.
            level (int, optional): The depth of the group in the group hierarchy. Defaults to None.
            name (str, optional): The name of the group (default groups can have localized names). Defaults to None.
            description (str, optional): The description of the group (default groups can have localized names). Defaults to None.
            owner (str, optional): The owner of the group. Defaults to None.
            modified_time (int, optional): The time in milliseconds since epoch since the group was last modified. Defaults to None.
            child_group_ids (List[int], optional): List of the child group ids. Defaults to None.
        """
        self.id = id
        self.parent_id = parent_id
        self.type = type
        self.level = level
        self.name = name
        self.description = description
        self.owner = owner
        self.modified_time = modified_time
        self.child_group_ids = child_group_ids
