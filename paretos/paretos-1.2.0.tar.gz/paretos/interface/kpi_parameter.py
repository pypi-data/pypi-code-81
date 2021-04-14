KpiGoalMinimum = "minimum"
KpiGoalMaximum = "maximum"


class KpiParameter:
    """
    Describes a single KPI Parameter which should be considered as an optimization goal
    """

    def __init__(
        self,
        name: str,
        goal: str = KpiGoalMinimum,
    ):
        if goal != KpiGoalMinimum and goal != KpiGoalMaximum:
            raise ValueError(
                f"KPI parameter goal has to be '{KpiGoalMinimum}' or '{KpiGoalMaximum}'"
            )

        self.__name = name
        self.__goal = goal

    def get_goal(self) -> str:
        return self.__goal

    def get_name(self) -> str:
        return self.__name
