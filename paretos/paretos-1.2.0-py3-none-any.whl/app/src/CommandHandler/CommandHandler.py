from typing import List, Union

from ..CommandHandler.Outcome.Outcome import Outcome


class CommandHandler:
    _schema = None
    _methods = ["POST"]

    def process(self, request_data: dict) -> Union[dict, Outcome]:
        return {}

    def get_name(self) -> str:
        return self.__class__.__module__ + "." + self.__class__.__name__

    def get_schema(self) -> Union[dict, None]:
        return self._schema

    def get_methods(self) -> List[str]:
        return self._methods
