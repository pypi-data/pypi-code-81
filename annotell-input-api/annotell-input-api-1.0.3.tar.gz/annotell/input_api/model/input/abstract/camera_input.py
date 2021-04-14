from abc import ABC, abstractmethod
from dataclasses import dataclass

from annotell.input_api.model.input.sensor_specification import SensorSpecification
from annotell.input_api.model.input.abstract.camera_frame import CameraFrame


@dataclass
class CameraInput(ABC):
    sensor_specification: SensorSpecification

    @abstractmethod
    def get_first_camera_frame(self) -> CameraFrame:
        return NotImplementedError
