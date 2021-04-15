# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, List
from decimal import Decimal

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# --------------------------------------------------------- class: MeasurementSet -------------------------------------------------------- #

class MeasurementSet:

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(self):
        self.__measurements = []


    # ------------------------------------------------------ Public properties ------------------------------------------------------- #

    @property
    def measurements(self) -> List[Decimal]:
        return self.__measurements

    @property
    def best(self) -> Optional[Decimal]:
        return self.__get_first_sorted_element(sort_reverse=False)

    @property
    def worst(self) -> Optional[Decimal]:
        return self.__get_first_sorted_element(sort_reverse=True)

    @property
    def total(self) -> float:
        return sum(self.__measurements)

    @property
    def avarage(self) -> Optional[Decimal]:
        if len(self.__measurements) == 0:
            return None

        return self.total / Decimal(len(self.__measurements))


    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    def add_measurement(
        self,
        duration_ms: Decimal
    ) -> None:
        self.__measurements.append(duration_ms)


    # ------------------------------------------------------- Private methods -------------------------------------------------------- #

    def __get_first_sorted_element(
        self,
        sort_reverse: bool = False
    ) -> Optional[float]:
        if len(self.__measurements) == 0:
            return None

        return sorted(self.__measurements, reverse=sort_reverse)[0]


# ---------------------------------------------------------------------------------------------------------------------------------------- #