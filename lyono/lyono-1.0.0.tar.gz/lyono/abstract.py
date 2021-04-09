from __future__ import annotations

import abc
from typing import TYPE_CHECKING, Any, Dict, Generic, List, Optional, TypeVar, Union

from pydantic.networks import AnyUrl

if TYPE_CHECKING:
    from enum import Enum
    from typing import Any

    StdTypes = Union[bool, int, float, str, dict]
    DictAny = Dict[str, Any]

else:
    pass

import httpx

from lyono import BaseModel


class BaseConfig(BaseModel, abc.ABC):
    class Config:
        arbitrary_types_allowed = True


class BaseInput(BaseModel, abc.ABC):
    class Config:
        arbitrary_types_allowed = True


TypeConfig = TypeVar("TypeConfig")
TypeInput = TypeVar("TypeInput")
TypeOutput = TypeVar("TypeOutput")


class BaseStrategy(BaseModel, abc.ABC):
    config: TypeConfig

    class Config:
        arbitrary_types_allowed = True

    def step(self, context: TypeInput) -> TypeOutput:
        raise NotImplementedError


class BaseClient(BaseModel, abc.ABC):
    """Create a client to process data inputs from the user.

    Args:
        strategy (BaseStrategy): The strategy we'd take on to send to the sink (storage, http, (g)RPC, library attr) from the step function. The strategy has the requirements for I/O validation.
        config (BaseConfiguration): The strategy we'd take on to send to the sink (storage, http, (g)RPC, library attr) from the step function. The strategy has the requirements for I/O validation.
    """

    default_config: Optional[BaseConfig] = None
    strategy: BaseStrategy

    def step(self, data: TypeInput) -> TypeOutput:
        """Runs a step like the OpenAI Step Environment.

        Args:
            data (BaseInput): The data we're using to send information to the user.

        Returns:
            Any: Allowed to get the get the return type of the
        """
        return self.strategy.step(data)

    @classmethod
    def create_strategy(cls, values: dict):
        if not "strategy" in values:
            if "default_config" not in values:
                raise AttributeError(
                    "You either need to have a default configuration for your strategy or specify a strategy on creation."
                )
            values["strategy"] = HTTPStrategy(values["default_config"])
        return values


class HTTPInput(BaseInput):
    method: str
    path: str
    data: Optional[Union[str, List[str]]] = None


class HTTPConfig(BaseConfig):
    base_url: AnyUrl
    https: bool = True
    params: Optional[Union[str, List[str]]] = None
    default_content_type: Optional[str] = "application/json"


class HTTPStrategy(BaseStrategy):
    _connection = httpx.Client()

    def step(self, data: TypeInput) -> TypeOutput:
        print(data)


class HTTPClient(BaseClient):
    def __init__(self, config: HTTPConfig, **data):
        data["strategy"] = HTTPStrategy(config=config)
        super().__init__(**data)


if __name__ == "__main__":
    # Please don't break
    try_config = HTTPConfig(base_url="http://example.com")
    print(HTTPClient)
    # client: HTTPClient = HTTPClient()
    # print(client)
    HTTPClient(config=try_config)
