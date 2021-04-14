from typing import Optional

from ..parameter import Parameter
from .continuity import Continuity


class DesignParameter(Parameter):
    """
    Class describing a single design parameter including its options
    """

    def __init__(
        self,
        name: str,
        minimum: float,
        maximum: float,
        continuity: Continuity,
        uuid: Optional[str] = None,
    ):
        super().__init__(
            name=name,
            uuid=uuid,
        )

        self.__minimum = minimum
        self.__maximum = maximum
        self.__continuity = continuity

    def get_minimum(self) -> float:
        return self.__minimum

    def get_maximum(self) -> float:
        return self.__maximum

    def get_continuity(self) -> Continuity:
        return self.__continuity
