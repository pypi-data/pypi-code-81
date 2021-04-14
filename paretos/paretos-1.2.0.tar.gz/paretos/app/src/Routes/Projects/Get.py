from typing import Union

from .....database.sqlite_dashboard_persistence import SQLiteDashboardPersistence
from ...CommandHandler.CommandHandler import CommandHandler
from ...CommandHandler.Outcome.Outcome import Outcome
from ...Service.Logger import Logger


class Get(CommandHandler):
    _methods = ["POST"]

    def __init__(self, logger: Logger, persistence: SQLiteDashboardPersistence):
        self.__logger = logger
        self.__persistence = persistence

    def process(self, request_data: dict) -> Union[dict, Outcome]:
        self.__logger.info("getting projects", projects_input={})
        projects = self.__persistence.get_projects()

        result_projects = []

        # TODO: Add Status
        for project in projects:
            result_projects.append(
                {
                    "id": project.get_id(),
                    # "status": project.get_status(),
                    "description": None,
                    "name": project.get_name(),
                }
            )

        return {"projects": result_projects}
