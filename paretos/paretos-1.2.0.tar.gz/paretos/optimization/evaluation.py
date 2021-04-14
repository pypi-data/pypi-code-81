from typing import Optional
from uuid import uuid4

from .design import DesignValues
from .kpi import KpiValues


class Evaluation:
    """
    Class for a single evaluation with matching design and kpis
    """

    def __init__(
        self,
        design: DesignValues,
        kpis: KpiValues = None,
        is_pareto_optimal: Optional[bool] = None,
        uuid: str = None,
    ):
        self.__id = uuid or str(uuid4())
        self.__design = design
        self.__kpis = kpis
        self.__is_pareto_optimal = is_pareto_optimal

    def add_result(self, kpis: KpiValues):
        self.__kpis = kpis

    def get_id(self) -> str:
        return self.__id

    def get_design(self) -> DesignValues:
        return self.__design

    def get_kpis(self) -> Optional[KpiValues]:
        return self.__kpis

    def is_pareto_optimal(self) -> Optional[bool]:
        return self.__is_pareto_optimal

    def update_pareto_optimality(self, is_pareto_optimal: bool):
        self.__is_pareto_optimal = is_pareto_optimal
