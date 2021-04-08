from dataclasses import dataclass

from pvoutput_api.services.common.common import SystemDetails


@dataclass
class AddBatchStatusConfig:
    max_status_in_request: int = 30
    max_status_age_days: int = 14


@dataclass
class SystemConfig:
    system_details: SystemDetails
    add_batch_status_config: AddBatchStatusConfig


def load_system_config():
    pass