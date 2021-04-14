from typing import Optional, List
from dataclasses import dataclass

from annotell.input_api.model.input.abstract import *
from annotell.input_api.model.input.cameras_sequence.frame import Frame
from annotell.input_api.model.input.sensor_specification import SensorSpecification


@dataclass
class CamerasSequence(CameraInput):
    external_id: str
    frames: List[Frame]
    sensor_specification: SensorSpecification
    start_timestamp: Optional[int] = None

    def to_dict(self) -> dict:
        return dict(frames=[frame.to_dict() for frame in self.frames],
                    sensorSpecification=self.sensor_specification.to_dict(),
                    startTs=self.start_timestamp,
                    externalId=self.external_id)

    def get_first_camera_frame(self) -> CameraFrame:
        return self.frames[0]
