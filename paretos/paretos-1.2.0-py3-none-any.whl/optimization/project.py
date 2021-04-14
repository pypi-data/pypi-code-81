from typing import Optional
from uuid import uuid4

from .optimization_problem import OptimizationProblem
from .project_status.done import Done
from .project_status.ready import Ready
from .project_status.status import ProjectStatus


class Project:
    def __init__(
        self,
        name: str,
        problem: OptimizationProblem,
        status: Optional[ProjectStatus] = None,
        uuid: str = None,
    ):
        self.__name = name
        self.__optimization_problem = problem
        self.__status = status or Ready()
        self.__uuid = uuid or str(uuid4())

    def get_name(self) -> str:
        return self.__name

    def get_id(self) -> str:
        return self.__uuid

    def get_status(self) -> ProjectStatus:
        return self.__status

    def get_optimization_problem(self) -> OptimizationProblem:
        return self.__optimization_problem

    def finish(self) -> None:
        self.__status = Done()
