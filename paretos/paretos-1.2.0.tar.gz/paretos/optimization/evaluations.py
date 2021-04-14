from typing import List

from .evaluation import Evaluation


class Evaluations:
    """
    Class containing all evaluations
    """

    def __init__(self, evaluations: List[Evaluation] = None):
        if evaluations is None:
            self.__evaluations = []
        else:
            self.__evaluations = evaluations.copy()

    def get_evaluations(self) -> List[Evaluation]:
        return self.__evaluations.copy()

    def add_evaluation(self, evaluation: Evaluation):
        self.__evaluations.append(evaluation)

    def get_pareto_optimal_evaluations(self) -> List[Evaluation]:
        pareto_optima = []

        for evaluation in self.__evaluations:
            if evaluation.is_pareto_optimal():
                pareto_optima.append(evaluation)

        return pareto_optima
