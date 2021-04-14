from dataclasses import dataclass

from annotell.input_api.model.input.abstract import *
from annotell.input_api.model.input.cameras.frame import Frame
from annotell.input_api.model.input.sensor_specification import SensorSpecification


@dataclass
class Cameras(CameraInput):
    external_id: str
    sensor_specification: SensorSpecification
    frame: Frame

    def to_dict(self) -> dict:
        return dict(frame=self.frame.to_dict(),
                    sensorSpecification=self.sensor_specification.to_dict(),
                    externalId=self.external_id)

    def get_first_camera_frame(self) -> CameraFrame:
        return self.frame
