from typing import List
from .qradarmodel import QRadarModel


class LogsourceGroup(QRadarModel):

    def __init__(self, *, id: int = None, name: str = None, description: str = None, parent_id: int = None, owner: str = None, modification_date: str = None, child_groups: List = None):
        self.id = id
        self.name = name
        self.description = description
        self.parent_id = parent_id
        self.owner = owner
        self.modification_date = modification_date
        self.child_groups = child_groups
