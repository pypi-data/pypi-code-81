from __future__ import annotations

import abc
from typing import TYPE_CHECKING, Any, ClassVar

from loguru import logger
from pydantic import BaseModel, root_validator, validator
from pydantic.networks import AnyUrl

if TYPE_CHECKING:
    from dataclasses import dataclass
    from typing import Any, Dict, List, Optional, Union

    StdTypes = Union[bool, int, float, str, dict]
    DictAny = Dict[str, Any]

else:
    from pydantic.dataclasses import dataclass

import httpx
from lyono.abstract import BaseClient, BaseConfig, BaseInput, BaseStrategy
from lyono.formatting.enums import CRUD
from lyono.typings import DictAny

# from lyono


class HTTPInput(BaseInput):
    method: CRUD
    path: str
    data: Optional[Union[str, List[str]]] = None
    headers: Dict[str, Any] = {}
    params: Dict[str, Any] = {}


class HTTPConfig(BaseConfig):
    base_url: AnyUrl
    https: bool = True
    params: Union[List[str], str, None] = None
    default_content_type: Optional[str] = "application/json"

    @validator("base_url")
    def validate_base_url(cls, url: AnyUrl, values: dict):
        print(values)
        if "https" in values:
            tls = values["https"]
            if tls is True:
                url.scheme = "https"
            else:
                url.scheme = "http"
        return url


class HTTPStrategy(BaseStrategy):
    connection: ClassVar[httpx.Client] = httpx.Client()

    @root_validator
    def create_connection(cls, values: dict):
        config: HTTPConfig = values.get("config")
        header = cls.connection.headers
        cls.connection.headers = {
            **header,
            **{"content-type": config.default_content_type},
        }
        return values

    def get_url(self, path: str):

        base_url: AnyUrl = self.config.base_url
        base_url.path = path
        return base_url

    def step(self, data: HTTPInput) -> httpx.Response:
        header = self.connection.headers
        return self.connection.request(
            method=data.method, url=data.path, params={**header, **data.params}
        )


class HTTPClient(BaseClient):
    def __init__(self, http_config: HTTPConfig, **data):
        data["strategy"] = HTTPStrategy(config=http_config)
        super().__init__(**data)

    def step(self, data: HTTPInput) -> httpx.Response:
        return self.strategy.step(HTTPInput)


if __name__ == "__main__":
    # Please don't break
    HTTPClient(http_config=HTTPConfig(base_url="http://example.com"))
