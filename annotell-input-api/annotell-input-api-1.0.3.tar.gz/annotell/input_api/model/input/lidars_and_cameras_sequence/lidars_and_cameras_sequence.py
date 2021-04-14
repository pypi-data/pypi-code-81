from dataclasses import dataclass

from typing import List
from annotell.input_api.model.input.abstract import *
from annotell.input_api.model.input.lidars_and_cameras_sequence.frame import Frame
from annotell.input_api.model.input.sensor_specification import SensorSpecification


@dataclass
class LidarsAndCamerasSequence(CameraInput):
    external_id: str
    frames: List[Frame]
    calibration_id: str
    sensor_specification: SensorSpecification

    def to_dict(self) -> dict:
        return dict(frames=[frame.to_dict() for frame in self.frames],
                    sensorSpecification=self.sensor_specification.to_dict(),
                    externalId=self.external_id,
                    calibrationId=self.calibration_id)

    def get_first_camera_frame(self) -> CameraFrame:
        return self.frames[0]
