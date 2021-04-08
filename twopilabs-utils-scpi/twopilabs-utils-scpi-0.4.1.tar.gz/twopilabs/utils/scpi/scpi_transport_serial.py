import serial
import logging
from typing import *
from typing import BinaryIO
from .scpi_transport_base import ScpiTransportBase
from .scpi_resource import ScpiResource
from .scpi_exceptions import ScpiTransportException

class ScpiSerialTransport(ScpiTransportBase):
    _transport_name = 'ScpiSerialTransport'
    _transport_info = 'Serial SCPI Transport'
    _transport_type = 'Serial'

    @classmethod
    def discover(cls, usb_vid: Optional[int] = None, usb_pid: Optional[int] = None) -> List[ScpiResource]:
        import serial.tools.list_ports

        return [ScpiResource(transport=ScpiSerialTransport,
                             location=f'{"usb" if port.pid is not None else "serial"}' + f':{port.location}' if port.location is not None else '',
                             address=port.device,
                             name=port.description,
                             manufacturer=port.manufacturer if port.manufacturer is not None else None,
                             model=port.product if port.product is not None else None,
                             serialnum=port.serial_number if port.serial_number is not None else None,
                             info=port
                             ) for port in serial.tools.list_ports.comports()
                if ((usb_vid is None) or (usb_vid == port.vid))
                and ((usb_pid is None) or (usb_pid == port.pid))]

    def __init__(self, port: str, timeout: float = 5, **kwargs):
        super().__init__(**kwargs)
        self.logger = logging.getLogger(__name__)
        try:
            port = serial.Serial(port=port, timeout=timeout, exclusive=True, **kwargs)
        except serial.SerialException as msg:
            raise ScpiTransportException(msg) from msg

        self.io = cast(BinaryIO, port)

        port.reset_input_buffer()
        port.reset_output_buffer()
        port.timeout = 0
        while port.read() != b'':
            pass
        port.timeout = timeout
