from dataclasses import dataclass
from datetime import date, time

from requests import Response

from pvoutput_publisher.base.service import ResponseDataHandler, Service
from pvoutput_publisher.publisher import publish

ADD_STATUS_URL = "https://pvoutput.org/service/r2/addstatus.jsp"

MISSING_ENERGY_ERROR = "One of v1, v2, v3 or v4 aka Energy Generation, Power Generation, Energy Consumption " \
                       "or Power Consumption must be supplied: date:{date}, time:{time}"


@dataclass
class AddStatus:
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
        if self.energy_generation is None and \
                self.energy_consumption is None and \
                self.power_generation is None and \
                self.power_consumption is None:
            raise TypeError(
                MISSING_ENERGY_ERROR.format(date=date.strftime(self.date, self.date_formatter),
                                            time=time.strftime(self.time, self.time_formatter)))


class AddStatusService(Service):

    @property
    def url(self):
        return ADD_STATUS_URL

    @property
    def data(self):
        return self._data

    def set_status(self, add_status: AddStatus, is_donation_mode: bool):
        self._data["d"] = add_status.date.strftime(add_status.date_formatter)
        self._data["t"] = add_status.time.strftime(add_status.time_formatter)
        self._data["v1"] = add_status.energy_generation
        self._data["v2"] = add_status.power_generation
        self._data["v3"] = add_status.energy_consumption
        self._data["v4"] = add_status.power_consumption
        self._data["v5"] = add_status.temperature
        self._data["v6"] = add_status.voltage
        self._data["c1"] = add_status.cumulative_flag
        self._data["n"] = add_status.net_flag
        if is_donation_mode:
            self._data["v7"] = add_status.extended_value_1
            self._data["v8"] = add_status.extended_value_2
            self._data["v9"] = add_status.extended_value_3
            self._data["v10"] = add_status.extended_value_4
            self._data["v11"] = add_status.extended_value_5
            self._data["v12"] = add_status.extended_value_6
            self._data["m1"] = add_status.text_message_1
        add_status.validate()


class AddStatusResponse(ResponseDataHandler):
    def handle(self, response: Response):
        pass


def publish_add_status(system_id: str, secret_api_key: str, add_status: AddStatus,
                       is_donation_mode: bool) -> AddStatusResponse:
    add_status_service = AddStatusService()
    add_status_service.set_status(add_status, is_donation_mode)
    add_status_response = AddStatusResponse()
    add_status_service.set_system(system_id=system_id, secret_api_key=secret_api_key)
    publish(add_status_service, data_handler=add_status_response)
    return add_status_response
