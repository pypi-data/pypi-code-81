from typing import Dict, List

from .evaluation_result_interface import EvaluationResultInterface


class OptimizationResultInterface:
    def get_evaluations(self) -> List[EvaluationResultInterface]:
        raise NotImplementedError()

    def get_pareto_optimal_evaluations(self) -> List[EvaluationResultInterface]:
        raise NotImplementedError()

    def to_dicts(self) -> List[Dict]:
        raise NotImplementedError()

    def to_csv(self, path: str):
        raise NotImplementedError()
