from . import Parameter


class ParameterValue:
    """
    Containing one Value for a KPI or Design
    """

    def __init__(self, parameter: Parameter, value: float):
        self.__parameter = parameter
        self.__value = value

    def get_parameter(self) -> Parameter:
        return self.__parameter

    def get_value(self) -> float:
        return self.__value
