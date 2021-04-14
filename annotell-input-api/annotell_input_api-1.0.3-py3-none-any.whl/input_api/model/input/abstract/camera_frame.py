from abc import ABC
from dataclasses import dataclass, field
from typing import List

from annotell.input_api.model.input.resources import Image, VideoFrame


@dataclass
class CameraFrame(ABC):
    images: List[Image] = field(default_factory=list)
    video_frames: List[VideoFrame] = field(default_factory=list)


