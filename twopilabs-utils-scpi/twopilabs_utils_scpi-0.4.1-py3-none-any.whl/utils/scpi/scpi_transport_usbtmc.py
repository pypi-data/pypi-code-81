import logging
from typing import *
from typing import BinaryIO
from twopilabs.utils import usbtmc
from .scpi_transport_base import ScpiTransportBase
from .scpi_resource import ScpiResource
from .scpi_exceptions import ScpiTransportException


class ScpiUsbTmcTransport(ScpiTransportBase):
    _transport_name = 'ScpiUsbTmcTransport'
    _transport_info = 'USBTMC SCPI Transport'
    _transport_type = 'USBTMC'

    @classmethod
    def discover(cls, usb_vid: Optional[int] = None, usb_pid: Optional[int] = None) -> List[ScpiResource]:
        return [ScpiResource(transport=ScpiUsbTmcTransport,
                             location=device.location,
                             address=device.address,
                             name=None,
                             manufacturer=device.manufacturer,
                             model=device.product,
                             serialnum=device.serial_number,
                             info=device
                             ) for device in usbtmc.UsbTmcDevice.list_devices(usb_vid=usb_vid, usb_pid=usb_pid)]

    def __init__(self, address: usbtmc.UsbTmcDeviceAddress, timeout: float = 5, **kwargs):
        super().__init__(**kwargs)
        self.logger = logging.getLogger(__name__)
        try:
            device = usbtmc.UsbTmcDevice(address=address, timeout=timeout, **kwargs)
        except usbtmc.UsbTmcException as msg:
            raise ScpiTransportException(msg) from msg

        self.io = cast(BinaryIO, device)
