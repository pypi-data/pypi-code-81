import csv
from typing import Dict, List

from ..interface.optimization_result_interface import OptimizationResultInterface
from ..optimization import Evaluations
from .evaluation_result import EvaluationResult


class OptimizationResult(OptimizationResultInterface):
    def __init__(self, evaluations: Evaluations):
        self.__evaluations = evaluations
        self.__results = []
        self.__pareto_optimal_results = []

        for evaluation in evaluations.get_evaluations():
            is_pareto_optimal = evaluation.is_pareto_optimal() or False
            design_values = evaluation.get_design().to_dict()
            kpi_values = evaluation.get_kpis().to_dict()

            result = EvaluationResult(
                evaluation_uuid=evaluation.get_id(),
                design_values=design_values,
                kpi_values=kpi_values,
                is_pareto_optimal=is_pareto_optimal,
            )

            self.__results.append(result)

            if is_pareto_optimal:
                self.__pareto_optimal_results.append(result)

    def get_evaluations(self) -> List[EvaluationResult]:
        return self.__results.copy()

    def get_pareto_optimal_evaluations(self) -> List[EvaluationResult]:
        return self.__pareto_optimal_results.copy()

    def to_dicts(self) -> List[Dict]:
        data = []

        for evaluation in self.__evaluations.get_evaluations():
            evaluation_id = evaluation.get_id()
            is_pareto_optimal = evaluation.is_pareto_optimal() or False

            evaluation_data = {
                "evaluation_id": evaluation_id,
                "is_pareto_optimal": is_pareto_optimal,
            }

            for design_parameter in evaluation.get_design():
                design_parameter_column = (
                    "design__" + design_parameter.get_parameter().get_name()
                )
                evaluation_data[design_parameter_column] = design_parameter.get_value()

            for kpi in evaluation.get_kpis():
                kpi_column = "kpi__" + kpi.get_parameter().get_name()
                evaluation_data[kpi_column] = kpi.get_value()

            data.append(evaluation_data)

        return data

    def to_csv(self, path: str):
        data = self.to_dicts()

        with open(path, "w", newline="", encoding="utf-8") as csv_file:
            fieldnames = [field for field in data[0]]

            csv_writer = csv.DictWriter(csv_file, fieldnames, delimiter=";")
            csv_writer.writeheader()

            csv_writer.writerows(data)
