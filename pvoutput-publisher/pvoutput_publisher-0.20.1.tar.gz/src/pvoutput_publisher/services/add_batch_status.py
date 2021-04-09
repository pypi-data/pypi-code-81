from dataclasses import dataclass, field
from datetime import datetime, date, time
from typing import List

from requests import Response

from pvoutput_publisher.base.service import ResponseDataHandler, Service
from pvoutput_publisher.publisher import publish
from pvoutput_publisher.services.add_status import AddStatus
from pvoutput_publisher.services.common.group_builder import Builder

ADD_BATCH_STATUS_URL = "https://pvoutput.org/service/r2/addbatchstatus.jsp"

MISSING_ENERGY_ERROR = "One of v1, v2, v3 or v4 aka Energy Generation, Power Generation, Energy Consumption " \
                       "or Power Consumption must be supplied: date:{date}, time:{time}"


@dataclass
class AddBatchStatus:
    status_list: List[AddStatus] = field(default_factory=list)

    def add_status(self, status: AddStatus):
        self.status_list.append(status)


class AddBatchStatusService(Service):

    @property
    def url(self):
        return ADD_BATCH_STATUS_URL

    @property
    def data(self):
        return self._data

    def set_status(self, add_batch_status: AddBatchStatus, is_donation_mode: bool):
        first_status = add_batch_status.status_list[0]
        self._data["c1"] = first_status.cumulative_flag
        self._data["n"] = first_status.net_flag
        self._data["data"] = self.build_data(add_batch_status, is_donation_mode)

    def build_data(self, add_batch_status: AddBatchStatus, is_donation_mode: bool):
        builder = Builder()
        for add_status in add_batch_status.status_list:
            builder.next_group()
            builder.add_value(add_status.date.strftime(add_status.date_formatter))
            builder.add_value(add_status.time.strftime(add_status.time_formatter))
            builder.add_value(add_status.energy_generation)
            builder.add_value(add_status.power_generation)
            builder.add_value(add_status.energy_consumption)
            builder.add_value(add_status.power_consumption)
            builder.add_value(add_status.temperature)
            builder.add_value(add_status.voltage)
            if is_donation_mode:
                builder.add_value(add_status.extended_value_1)
                builder.add_value(add_status.extended_value_2)
                builder.add_value(add_status.extended_value_3)
                builder.add_value(add_status.extended_value_4)
                builder.add_value(add_status.extended_value_5)
                builder.add_value(add_status.extended_value_6)
                builder.add_value(add_status.text_message_1)
            add_status.validate()
        return builder.text


@dataclass
class ReadingResponse:
    reading_date: date
    reading_time: time
    status_added: bool


class AddBatchStatusResponse(ResponseDataHandler):
    def __init__(self, reading_responses: List[ReadingResponse] = None):
        super().__init__()
        self._reading_responses = reading_responses

    def handle(self, response: Response):
        super(AddBatchStatusResponse, self).handle(response)
        self._reading_responses = split_records(response.text)

    @property
    def reading_responses(self) -> List[ReadingResponse]:
        return self._reading_responses


def publish_add_batch_status(system_id: str, secret_api_key: str, add_batch_status: AddBatchStatus,
                             is_donation_mode: bool = False) -> AddBatchStatusResponse:
    add_batch_status_service = AddBatchStatusService()
    add_batch_status_service.set_status(add_batch_status, is_donation_mode)
    add_batch_status_response = AddBatchStatusResponse()
    add_batch_status_service.set_system(system_id=system_id, secret_api_key=secret_api_key)
    publish(add_batch_status_service, data_handler=add_batch_status_response)
    return add_batch_status_response


def split_records(record_string: str = None, records_separator: str = ";", value_separator: str = ",") \
        -> List[ReadingResponse]:
    values = record_string.split(records_separator)
    return [split_value(value, value_separator) for value in values]


def split_value(record: str, separator: str) -> ReadingResponse:
    parts = record.split(separator)
    reading_date = datetime.strptime(parts[0], "%Y%m%d").date()
    reading_time = datetime.strptime(parts[1], "%H:%M").time()
    status = True if parts[2] == "1" else False
    return ReadingResponse(reading_date=reading_date, reading_time=reading_time, status_added=status)
