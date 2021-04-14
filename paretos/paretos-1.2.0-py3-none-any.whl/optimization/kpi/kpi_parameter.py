from typing import Optional

from ..goals import Goal, Minimum
from ..parameter import Parameter


class KpiParameter(Parameter):
    """
    Describes a single KPI Parameter which should be considered as an optimization goal
    """

    def __init__(
        self, name: str, goal: Optional[Goal] = None, uuid: Optional[str] = None
    ):
        super().__init__(
            name=name,
            uuid=uuid,
        )

        self.__goal = goal or Minimum()

    def get_goal(self) -> Goal:
        return self.__goal
