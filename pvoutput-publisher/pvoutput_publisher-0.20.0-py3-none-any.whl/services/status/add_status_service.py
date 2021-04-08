from dataclasses import dataclass
from datetime import date, time

from requests import Response

from pvoutput_publisher.constants import ADD_STATUS_MISSING_ENERGY_ERROR
from pvoutput_publisher.services.common.common import Data, RequestBase, Service, SystemDetails, set_param, ResponseBase


@dataclass
class AddStatus(Data):
    date: date
    time: time
    energy_generation: int = None
    power_generation: int = None
    energy_consumption: int = None
    power_consumption: int = None
    temperature: float = None
    voltage: float = None
    cumulative_flag: int = None
    net_flag: int = None
    extended_value_1: float = None
    extended_value_2: float = None
    extended_value_3: float = None
    extended_value_4: float = None
    extended_value_5: float = None
    extended_value_6: float = None
    text_message_1: str = None
    date_formatter: str = "%Y%m%d"
    time_formatter: str = "%H:%M"

    def validate(self):
        if self.energy_generation is None and self.energy_consumption is None and self.power_generation is None and self.power_consumption is None:
            raise TypeError(
                ADD_STATUS_MISSING_ENERGY_ERROR.format(date=date.strftime(self.date, self.date_formatter), time=time.strftime(self.time, self.time_formatter)))


@dataclass
class AddStatusRequest(RequestBase):
    data: AddStatus


class AddStatusService(Service):
    def create_request(self, data: Data, url: str, system: SystemDetails) -> dict:
        params = {}

        set_param("d", data.date.strftime(data.date_formatter), params)
        set_param("t", data.time.strftime(data.time_formatter), params)
        set_param("v1", data.energy_generation, params)
        set_param("v2", data.power_generation, params)
        set_param("v3", data.energy_consumption, params)
        set_param("v4", data.power_consumption, params)
        set_param("v5", data.temperature, params)
        set_param("v6", data.voltage, params)
        set_param("c1", data.cumulative_flag, params)
        set_param("n", data.net_flag, params)
        if system.is_donation_mode:
            set_param("v7", data.extended_value_1, params)
            set_param("v8", data.extended_value_2, params)
            set_param("v9", data.extended_value_3, params)
            set_param("v10", data.extended_value_4, params)
            set_param("v11", data.extended_value_5, params)
            set_param("v12", data.extended_value_6, params)
            set_param("m1", data.text_message_1, params)

        data.validate()
        return params

    def parse_response(self, response_text: str, reponse: Response) -> Data:
        return AddStatusResponse(reponse)


@dataclass
class AddStatusResponse(ResponseBase):
    pass
