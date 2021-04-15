"""Module for annealing"""

from dataclasses import dataclass
from typing import Any


@dataclass
class AnnealingResult:
    """Result for annealing."""
    solutions: list[list[int]]
    solutionCounts: list[int]
    values: list[float]
    variableCount: int
    taskMetadata: dict[str, Any]
    additionalMetadata: dict[str, Any]


class AnnealingTask:
    """Annealing task."""
    def __init__(self, api, **kwargs) -> None:
        self.api = api
        self.data = kwargs

    def detail(self) -> AnnealingResult:
        """This method may be changed."""
        path = "v1/quantum-tasks/get"
        body = {
            "id": self.data['id'],
        }
        return AnnealingResult(**self.api.post_request(path, body))
