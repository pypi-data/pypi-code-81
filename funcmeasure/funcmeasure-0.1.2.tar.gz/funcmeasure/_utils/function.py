# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, List
from decimal import Decimal
import timeit

# Local
from .measurement_set import MeasurementSet

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------ class: Function ----------------------------------------------------------- #

class Function:

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        function: callable,
        function_name: Optional[str] = None
    ):
        self.__function = function
        self.__function_name = function_name or function.__name__
        self.__measurement_set = MeasurementSet()


    # ------------------------------------------------------ Public properties ------------------------------------------------------- #

    @property
    def function(self) -> callable:
        return self.__function

    @property
    def name(self) -> str:
        return self.__function_name

    @property
    def real_name(self) -> str:
        return self.__function.__name__

    @property
    def measurement_set(self) -> MeasurementSet:
        return self.__measurement_set


    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    def measure(
        self,
        times: int
    ) -> None:
        for _ in range(times):
            start = Decimal(timeit.default_timer())*Decimal(1000)
            self.function()
            duration_ms = (Decimal(timeit.default_timer())*Decimal(1000)) - start

            self.__measurement_set.add_measurement(duration_ms)


# ---------------------------------------------------------------------------------------------------------------------------------------- #