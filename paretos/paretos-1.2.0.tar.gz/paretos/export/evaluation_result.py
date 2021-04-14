from typing import Dict

from ..interface import EvaluationResultInterface


class EvaluationResult(EvaluationResultInterface):
    def __init__(
        self,
        evaluation_uuid: str,
        design_values: Dict[str, float],
        kpi_values: Dict[str, float],
        is_pareto_optimal: bool,
    ):
        self.__evaluation_uuid = evaluation_uuid
        self.__design_values = design_values
        self.__kpi_values = kpi_values
        self.__is_pareto_optimal = is_pareto_optimal

    def get_evaluation_uuid(self) -> str:
        return self.__evaluation_uuid

    def get_design_values(self) -> Dict[str, float]:
        return self.__design_values

    def get_kpi_values(self) -> Dict[str, float]:
        return self.__kpi_values

    def is_pareto_optimal(self) -> bool:
        return self.__is_pareto_optimal
