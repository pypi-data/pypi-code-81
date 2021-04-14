from typing import Dict


class EvaluationResultInterface:
    def get_evaluation_uuid(self) -> str:
        raise NotImplementedError()

    def get_design_values(self) -> Dict[str, float]:
        raise NotImplementedError()

    def get_kpi_values(self) -> Dict[str, float]:
        raise NotImplementedError()

    def is_pareto_optimal(self) -> bool:
        raise NotImplementedError()
