from typing import Generic, Iterator, List, Optional, TypeVar

from . import Parameter

ParameterT = TypeVar("ParameterT", bound=Parameter, covariant=True)


class ParameterSpace(Generic[ParameterT]):
    """
    Class describing the set of all design parameters for a specific problem
    """

    def __init__(self, parameters: List[ParameterT]):
        self.__parameters = parameters.copy()

    def __iter__(self) -> Iterator[ParameterT]:
        return iter(self.__parameters)

    def get_parameter_by_id(self, id_: str) -> Optional[ParameterT]:
        for parameter in self.__parameters:
            if parameter.get_id() == id_:
                return parameter

        return None

    def get_parameter_by_name(self, id_: str) -> Optional[ParameterT]:
        for parameter in self.__parameters:
            if parameter.get_name() == id_:
                return parameter

        return None

    def size(self):
        return len(self.__parameters)
