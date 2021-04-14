from typing import Union

from .....database.sqlite_dashboard_persistence import SQLiteDashboardPersistence
from ...CommandHandler.CommandHandler import CommandHandler
from ...CommandHandler.Outcome.NotFoundFailure import NotFoundFailure
from ...CommandHandler.Outcome.Outcome import Outcome
from ...Service.Logger import Logger
from ...Service.ResponseMapper import DataApiResponseMapper


class Get(CommandHandler):
    _methods = ["POST"]
    _schema = {
        "type": "object",
        "properties": {"project": {"type": "string"}},
        "required": ["project"],
    }

    def __init__(self, logger: Logger, persistence: SQLiteDashboardPersistence):
        self.__logger = logger
        self.__persistence = persistence

    def process(self, request_data: dict) -> Union[dict, Outcome]:
        self.__logger.info(
            "getting project meta",
            project_meta_input={"project": request_data["project"]},
        )

        project, evaluations = self.__persistence.load_project_data_by_id(
            request_data["project"]
        )

        if project is None:
            return NotFoundFailure()

        problem = project.get_optimization_problem()

        return DataApiResponseMapper.problem_to_request(problem)
