# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import List, Callable, Union, Tuple, Dict, Optional
from decimal import Decimal

# Local
from .function import Function
from ..models import FunctionStats

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# -------------------------------------------------------- class: FunctionMeasurer ------------------------------------------------------- #

class FunctionMeasurer:

    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    @classmethod
    def measure(
        cls,
        funcs: Union[List[Union[Callable, Tuple[Callable, str]]], Dict[Callable, Optional[str]]],
        times: float
    ) -> List[Function]:
        functions = cls.__get_functions(funcs)

        for function in functions:
            function.measure(times)

        functions = sorted(functions, key=lambda x: x.measurement_set.total, reverse=False)
        fastest_dur_ms = functions[0].measurement_set.total

        return [
            FunctionStats(
                function,
                function.measurement_set.total/fastest_dur_ms if i > Decimal(0) else Decimal(1)
            )

            for i, function in enumerate(functions)
        ]


    # ------------------------------------------------------- Private methods -------------------------------------------------------- #

    @staticmethod
    def __get_functions(funcs: Union[List[Union[Callable, Tuple[Callable, str]]], Dict[Callable, Optional[str]]]) -> List[Function]:
        if isinstance(funcs, list):
            _funcs = {}

            for func in funcs:
                if isinstance(func, tuple):
                    _funcs[func[0]] = func[1]
                else:
                    _funcs[func] = func.__name__

            funcs = _funcs

        return [Function(func, func_name) for func, func_name in funcs.items()]


# ---------------------------------------------------------------------------------------------------------------------------------------- #