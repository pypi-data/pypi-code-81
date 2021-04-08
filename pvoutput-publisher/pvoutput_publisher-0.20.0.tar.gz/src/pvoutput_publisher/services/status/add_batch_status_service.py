from dataclasses import dataclass, field
from datetime import date, time, datetime
from typing import List

from requests import Response

from pvoutput_publisher.services.common.common import Data, RequestBase, Service, SystemDetails, set_param, ResponseBase
from pvoutput_publisher.services.common.group_builder import Builder
from pvoutput_publisher.services.status.add_status_service import AddStatus


@dataclass
class AddBatchStatus(Data):
    status_list: List[AddStatus] = field(default_factory=list)

    def add_status(self, status: AddStatus):
        self.status_list.append(status)


@dataclass
class AddBatchStatusRequest(RequestBase):
    data: AddBatchStatus


class AddBatchStatusService(Service):
    def create_request(self, data: Data, url: str, system: SystemDetails) -> dict:
        params = {}
        add_batch_status: AddBatchStatus = data

        first_status = add_batch_status.status_list[0]
        set_param("c1", first_status.cumulative_flag, params)
        set_param("n", first_status.net_flag, params)
        set_param("data", self.build_data(add_batch_status, system), params)
        return params

    def build_data(self, add_batch_status, system):
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
            if system.is_donation_mode:
                builder.add_value(add_status.extended_value_1)
                builder.add_value(add_status.extended_value_2)
                builder.add_value(add_status.extended_value_3)
                builder.add_value(add_status.extended_value_4)
                builder.add_value(add_status.extended_value_5)
                builder.add_value(add_status.extended_value_6)
                builder.add_value(add_status.text_message_1)
            add_status.validate()
        return builder.text

    def parse_response(self, resp_text: str, response: Response) -> Data:
        response = StatusSplitter().split_records(resp_text)
        response.resp = response
        return response


@dataclass
class StatusResponse(Data):
    date: date
    time: time
    status_added: bool


@dataclass
class AddBatchStatusResponse(ResponseBase):
    statuses: List[StatusResponse] = field(default_factory=list)

    def add_status(self, status: StatusResponse):
        self.statuses.append(status)


class StatusSplitter:
    def split_records(self, records: str = None, record_separator: str = ";", value_separator: str = ",") -> AddBatchStatusResponse:
        response = AddBatchStatusResponse()
        for record in records.split(record_separator):
            response.add_status(self.split(record, value_separator))
        return response

    def split(self, record: str, separator: str) -> StatusResponse:
        split = record.split(separator)
        date = datetime.strptime(split[0], "%Y%m%d").date()
        time = datetime.strptime(split[1], "%H:%M").time()
        status = True if split[2] == "1" else False
        return StatusResponse(date=date, time=time, status_added=status)
