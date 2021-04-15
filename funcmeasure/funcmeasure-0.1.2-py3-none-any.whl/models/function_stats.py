# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional
from decimal import Decimal

# Pip
from jsoncodable import JSONCodable

# Local
from .._utils import Function

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# --------------------------------------------------------- class: FunctionStats --------------------------------------------------------- #

class FunctionStats(JSONCodable):

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        function: Function,
        relative_speed: Decimal
    ):
        self.name = function.name
        self.real_name = function.real_name

        self.duration_best = function.measurement_set.best
        self.duration_worst = function.measurement_set.worst
        self.duration_total = function.measurement_set.total
        self.duration_average = function.measurement_set.avarage
        self.durations = function.measurement_set.measurements

        self.relative_speed = relative_speed


# ---------------------------------------------------------------------------------------------------------------------------------------- #