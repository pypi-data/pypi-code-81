from typing import Optional

from ..project_status import Ready
from ..project_status.status import ProjectStatus


class DashboardProject:
    def __init__(
        self,
        name: str,
        uuid: str,
        status: Optional[ProjectStatus] = None,
    ):
        self.__name = name
        self.__status = status or Ready()
        self.__uuid = uuid

    def get_name(self) -> str:
        return self.__name

    def get_id(self) -> str:
        return self.__uuid

    def get_status(self) -> ProjectStatus:
        return self.__status
