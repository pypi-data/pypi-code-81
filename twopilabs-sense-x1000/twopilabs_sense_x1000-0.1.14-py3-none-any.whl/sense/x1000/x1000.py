from typing import *
from twopilabs.utils.scpi import ScpiResource
from .x1000_base import SenseX1000Base
from .x1000_scpi import SenseX1000ScpiDevice


class SenseX1000(SenseX1000Base):
    @classmethod
    def open_device(cls, resource: Union[ScpiResource], **kwargs):
        # Use as a factory function
        # As of this time, only scpi is supported
        return SenseX1000ScpiDevice(resource, **kwargs)

    @classmethod
    def find_devices(cls) -> List[Union[ScpiResource]]:
        devices = []

        # As of this time we only search for Scpi devices
        devices += SenseX1000ScpiDevice.find_devices()

        return devices
