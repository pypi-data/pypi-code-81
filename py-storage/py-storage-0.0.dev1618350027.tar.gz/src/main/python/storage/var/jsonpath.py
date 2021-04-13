from __future__ import annotations

import abc
from typing import Any, Iterable

import jsonpath_ng

from storage.var import BaseVar


class JsonPath(BaseVar[Any, Any]):
    json_path: Any

    def __init__(self, json_path):
        self.json_path = json_path

    @classmethod
    def from_str(cls, json_path: str):
        return cls(jsonpath_ng.parse(json_path))

    def find(self, item):
        return [match.value for match in self.json_path.find(item)]

    @abc.abstractmethod
    def __call__(self, item: Any) -> Any:
        raise NotImplementedError()

    @staticmethod
    def array(json_path: str) -> JsonPath:
        return ArrayJsonPath.from_str(json_path)

    @staticmethod
    def single(json_path: str) -> JsonPath:
        return SingleJsonPath.from_str(json_path)


class ArrayJsonPath(JsonPath):

    def __call__(self, item: Any) -> Iterable[Any]:
        return self.find(item)


class SingleJsonPath(JsonPath):

    def __call__(self, item: Any) -> Any:
        for item in self.find(item):
            return item
        return None
