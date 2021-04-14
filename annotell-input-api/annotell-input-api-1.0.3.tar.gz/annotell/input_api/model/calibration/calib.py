from annotell.input_api.model.abstract.abstract_models import Response
from annotell.input_api.util import ts_to_dt
from datetime import datetime
from typing import Mapping, Optional
from dataclasses import dataclass
from typing import Dict, Union
from annotell.input_api.model.calibration.sensors import (
    CameraCalibration, LidarCalibration
)


@dataclass
class SensorCalibration:
    external_id: str
    calibration: Dict[str, Union[CameraCalibration, LidarCalibration]]

    def to_dict(self):
        return {
            'externalId': self.external_id,
            'calibration': {k: v.to_dict() for (k, v) in self.calibration.items()}
        }

@dataclass
class SensorCalibrationEntry(Response):
    id: str
    external_id: str
    created: datetime
    calibration: Optional[Mapping[str, Union[CameraCalibration, LidarCalibration]]]

    @staticmethod
    def from_json(js: dict):
        return SensorCalibrationEntry(
            id=js["id"],
            external_id=js["externalId"],
            created=ts_to_dt(js["created"]),
            calibration=js.get("calibration")
        )
