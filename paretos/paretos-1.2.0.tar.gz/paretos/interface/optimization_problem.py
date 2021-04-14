from typing import List

from .design_parameter import DesignParameter
from .kpi_parameter import KpiParameter


class OptimizationProblem:
    """
    Summing up all relevant information for an optimization run.
    """

    def __init__(
        self,
        design_parameters: List[DesignParameter],
        kpi_parameters: List[KpiParameter],
    ):
        self.__design_parameters = design_parameters
        self.__kpi_parameters = kpi_parameters

    def get_design_parameters(self) -> List[DesignParameter]:
        return self.__design_parameters

    def get_kpi_parameters(self) -> List[KpiParameter]:
        return self.__kpi_parameters
