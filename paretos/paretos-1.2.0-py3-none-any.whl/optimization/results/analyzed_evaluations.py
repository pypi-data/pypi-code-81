from __future__ import annotations

from typing import List

from .analyzed_evaluation import AnalyzedEvaluation


class AnalyzedEvaluations:
    """
    Class mapping all evaluations with the information from api about pareto optimality
    """

    def __init__(self, analyzed_evaluations: List[AnalyzedEvaluation] = None):
        if analyzed_evaluations is None:
            analyzed_evaluations = []

        self.__analyzed_evaluations = analyzed_evaluations
        self.__evaluation_ids = self.__get_evaluation_ids()
        self.__pareto_evaluation_ids = self.__get_evaluation_ids(True)

    def __get_evaluation_ids(self, only_pareto: bool = False):
        return [
            evaluation.get_id()
            for evaluation in self.__analyzed_evaluations
            if (evaluation.is_pareto_optimal() or not only_pareto)
        ]

    def get_evaluation_ids(self) -> List[str]:
        return self.__evaluation_ids

    def get_pareto_evaluation_ids(self) -> List[str]:
        return self.__pareto_evaluation_ids
