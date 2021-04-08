from abc import abstractmethod, ABC
from dataclasses import dataclass

from requests import Response


def set_param(param_name, value, params):
    if value is not None:
        params[param_name] = value


@dataclass
class Data:
    pass


@dataclass
class SystemDetails:
    api_key: str
    system_id: str
    is_donation_mode: bool = False


@dataclass
class RequestBase(Data):
    url: str
    system_details: SystemDetails


@dataclass
class ResponseBase(Data):
    resp: Response = None


class Service(ABC):

    @abstractmethod
    def create_request(self, data: Data, url: str, system: SystemDetails) -> dict:
        pass

    @abstractmethod
    def parse_response(self, response_text: str, response: Response) -> Data:
        pass
