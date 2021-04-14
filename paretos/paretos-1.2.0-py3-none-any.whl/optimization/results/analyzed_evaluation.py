from __future__ import annotations


class AnalyzedEvaluation:
    """
    Class inheriting one evaluation and the information about pareto optimality
    """

    def __init__(self, id: str, is_pareto_optimal: bool):
        self.__id = id
        self.__is_pareto_optimal = is_pareto_optimal

    def get_id(self) -> str:
        return self.__id

    def is_pareto_optimal(self) -> bool:
        return self.__is_pareto_optimal
