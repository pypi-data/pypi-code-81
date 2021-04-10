import abc
from typing import Optional, Iterable, Dict, Union

from olxbrasil.constants import LOCATIONS_URL
from olxbrasil.exceptions import FilterNotFoundError
from olxbrasil.utils import build_boolean_parameters, build_search_parameters


class Filter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_filters(self, params: Optional[Dict] = None) -> str:
        ...  # pragma: nocover

    @abc.abstractmethod
    def get_endpoint(self) -> str:
        ...  # pragma: nocover


class ItemFilter(Filter):
    def __init__(
        self,
        *,
        manufacturer: Optional[str] = None,
        model: Optional[str] = None,
        boolean_filters: Optional[Iterable] = tuple(),
        search_filters: Optional[Dict] = None,
    ):
        self.__manufacturer = manufacturer
        self.__model = model
        self.__boolean_filters = boolean_filters
        self.__search_filters = search_filters

    def get_filters(self, params: Optional[Dict] = None) -> Dict:
        car_filters = params or {}
        if self.__boolean_filters:
            car_filters.update(
                build_boolean_parameters(*self.__boolean_filters)
            )
        if self.__search_filters:
            car_filters.update(
                build_search_parameters(**self.__search_filters)
            )

        return car_filters

    def get_endpoint(self) -> str:
        endpoint = ""

        if self.__manufacturer:
            endpoint += f"/{self.__manufacturer.lower()}"
            if self.__model:
                endpoint += f"/{self.__model.lower()}"

        return endpoint


class LocationFilter(Filter):
    def __init__(self, state: str, ddd: Optional[Union[int, float]] = None):
        self.state = state.upper()
        self.__ddd = ddd
        self.__validate()

    def __validate(self) -> bool:
        if self.state not in LOCATIONS_URL:
            raise FilterNotFoundError(f"State {self.state} not found")
        elif self.__ddd and self.__ddd not in LOCATIONS_URL[self.state]:
            raise FilterNotFoundError(
                f"DDD {self.__ddd} was not found in state {self.state}"
            )

        return True

    def get_filters(
        self, params: Optional[Dict] = None
    ) -> str:  # pragma: nocover
        pass

    def get_endpoint(self) -> str:
        if self.__ddd:
            return LOCATIONS_URL[self.state][self.__ddd]
        return ""
