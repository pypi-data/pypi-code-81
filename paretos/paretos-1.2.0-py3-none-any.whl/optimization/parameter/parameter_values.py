from typing import Iterator, List

from . import ParameterValue


class ParameterValues:
    """
    Containing a list of values
    """

    def __init__(self, values: List[ParameterValue]):
        self.__values = values.copy()

    def __iter__(self) -> Iterator[ParameterValue]:
        return iter(self.get_values())

    def get_values(self) -> List[ParameterValue]:
        return self.__values.copy()

    def get_value_by_name(self, name: str) -> float:
        searched_value = next(
            (
                value
                for value in self.__values
                if value.get_parameter().get_name() == name
            ),
            None,
        )

        if searched_value is None:
            raise ValueError(f"There is no Value for id '{id}'")

        return searched_value.get_value()

    def to_dict(self):
        dict_data = {}

        for parameter_value in self.__values:
            name = parameter_value.get_parameter().get_name()
            float_value = parameter_value.get_value()

            dict_data[name] = float_value

        return dict_data
