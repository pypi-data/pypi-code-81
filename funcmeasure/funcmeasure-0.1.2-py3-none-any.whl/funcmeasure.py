# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import List, Callable, Union, Tuple, Dict, Optional

# Local
from ._utils import FunctionMeasurer, Renderer
from .models import FunctionStats, TableFormat

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------ Public methods ------------------------------------------------------------ #

def measure(
    funcs: Union[List[Union[Callable, Tuple[Callable, str]]], Dict[Callable, Optional[str]]],
    times: int = 1000,
    print_benchmark: bool = True,
    benchmark_table_format: TableFormat = TableFormat.FANCY_GRID
) -> List[FunctionStats]:
    """Measure and compare execution times of functions

    Args:
        funcs (Union[List[Union[Callable, Tuple[Callable, str]]], Dict[Callable, Optional[str]]]):
            The functions that will be measured.
            This can be a list or a dictionary.
            If dictionary is passed, the name of the function will be
                overwritten with the name of the specified value.
            If a list is passed, the values can be either a Callable
                or a Tuple of Callable and string(custom function name)

            Example values:
                - List: [f1, (f2, 'second'), f3]
                - Dict: {
                      f1: 'first',
                      f2: 'second',
                      f3: None
                  }

    Kwargs:
        times (int, optional): How many times will each function be measured. Defaults to 1000.

        print_benchmark (bool, optional): Print results or no. Defaults to True.

        benchmark_table_format (TableFormat, optional): if print_benchmark is True, decides, the table format od the printed data. (Check funcmeasure.models.enums.TableFormat for more)

    Returns:
        List[Measurement]: List of Measurement objects
    """
    stats = FunctionMeasurer.measure(funcs, times)

    if print_benchmark:
        Renderer.render(stats, times_ran=times, table_format=benchmark_table_format)

    return stats

def partial(func: Callable, *args, **kwargs):
    from functools import partial as _partial

    return _partial(func, *args, **kwargs)


# ---------------------------------------------------------------------------------------------------------------------------------------- #