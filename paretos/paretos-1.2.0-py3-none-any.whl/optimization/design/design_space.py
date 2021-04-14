from typing import List

from ..parameter import ParameterSpace
from . import DesignParameter


class DesignSpace(ParameterSpace[DesignParameter]):
    def __init__(self, parameters: List[DesignParameter] = None):
        super().__init__(parameters)
