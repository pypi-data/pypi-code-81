from typing import List, Optional, Tuple

from .. import optimization
from .sqlite_database import SQLiteDatabase
from .sqlite_persistence import SQLitePersistence
from .sqlite_persistence_project_loader import SQLitePersistenceProjectLoader


class SQLiteDashboardPersistence:
    def __init__(self, database: SQLiteDatabase):
        self.__project_loader = SQLitePersistenceProjectLoader(database=database)

    def get_projects(self) -> List[optimization.Project]:
        return self.__project_loader.load_projects()

    def load_project_data_by_id(
        self, project_id: str
    ) -> Tuple[Optional[optimization.Project], optimization.Evaluations]:
        return self.__project_loader.load_project_data_by_id(project_id=project_id)
