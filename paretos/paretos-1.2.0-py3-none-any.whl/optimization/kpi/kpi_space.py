from typing import List

from ..parameter import ParameterSpace
from . import KpiParameter


class KpiSpace(ParameterSpace[KpiParameter]):
    """
    Class describing the set of all design parameters for a specific problem
    """

    def __init__(self, parameters: List[KpiParameter] = None):
        super().__init__(parameters)
