# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import List, Optional
from decimal import Decimal

# Pip
from tabulate import tabulate

# Local
from ..models import FunctionStats, TableFormat

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------ class: Renderer ----------------------------------------------------------- #

class Renderer:

    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    @classmethod
    def render(
        cls,
        stats: List[FunctionStats],
        times_ran: int,
        table_format: TableFormat
    ) -> None:
        headers = ['Name', 'Avg (ms)', 'Total (ms)', 'Best (ms)', 'Worst (ms)', 'Benchmark']
        table = [
            [s.name, s.duration_average, s.duration_total, s.duration_best, s.duration_worst, cls.__relative_speed_str(s.relative_speed)]
            for i, s in enumerate(stats)
        ]

        print(
            'Ran {} functions. {} times each.\n\n{}'.format(
                len(stats),
                times_ran,
                tabulate(
                    table,
                    headers=headers,
                    tablefmt=(table_format or TableFormat.FANCY_GRID).value,
                    showindex=True,
                    floatfmt='.6f',
                    colalign=['right' for _ in range(len(headers)+1)]
                )
            )
        )

    @staticmethod
    def __relative_speed_str(relative_speed: Decimal) -> Optional[str]:
        if relative_speed <= 1:
            return None

        if relative_speed == Decimal(int(relative_speed)):
            relative_speed = Decimal(int(relative_speed))
        else:
            precision = Decimal(100)
            relative_speed = Decimal(int(relative_speed * precision)) / precision

        return '~{}x'.format(relative_speed)


# ---------------------------------------------------------------------------------------------------------------------------------------- #