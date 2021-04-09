import struct
import time
from typing import Union, List, Type

import serial
from crcmod import predefined

from ...daq.daq_labjack import DAQLabJack

__all__ = [
    "ExceptionUART",
    "UARTCommon",
    "SimpleUARTProt",
]


class ExceptionUART(Exception):
    pass


class UARTCommon:
    CU_LABJACK = 'labjack'
    CU_SERIAL = 'serial'

    def __init__(self, device: str = 'ANY', connection_type: str = 'ANY', id: str = 'ANY', port: str = None,
                 baud_rate: int = 9600, pin_tx: str = None, pin_rx: str = None,
                 dev_handle: int = None, timeout: float = 1.0):
        """
        Creates a new UART device.

        Parameters
        ----------
        device : str
            Device Type. "T4", "T7" or "ANY"
        connection_type : str
            Can be: "ANY", "USB", "TCP", "ETHERNET", and "WIFI".
        id : str
            This can be a serial number, IP address, "ANY"
            or device name
        port : str
            Path to serial device. Starts with "/dev"
        baud_rate : int
            Baud rate
        pin_tx : str
            Tranceiver pin number
        pin_rx : str
            Receiver pin number
        dev_handle : int
            Device handle to an existing Labjack device
        timeout : float
            Timeout in seconds
        """

        self.__timeout = timeout

        if port:
            self.__uart_device = self.CU_SERIAL
            self._uart = serial.Serial(port=port, baudrate=baud_rate)

            if not self._uart.is_open:
                self._uart.open()
        else:
            self.__uart_device = self.CU_LABJACK
            self._uart = DAQLabJack(device, connection_type, id, handle=dev_handle)
            self._uart.config_uart(pin_tx, pin_rx, baud_rate)

    def transmit(self, msg: Union[List[int], str]) -> None:
        """

        Parameters
        ----------
        msg :

        Returns
        -------

        """
        if self.__uart_device == self.CU_SERIAL:
            _msg = struct.pack(f'={len(msg)}B', *msg)
            self._uart.write(_msg)
            self._uart.flush()

        elif self.__uart_device == self.CU_LABJACK:

            if isinstance(msg, str):
                msg = msg.encode()

            if isinstance(msg, bytes):
                msg = list(msg)
            self._uart.transmit(msg)

    def receive(self, num_bytes: int = None) -> Union[List, str, int]:
        """

        Parameters
        ----------
        num_bytes :

        Returns
        -------

        """
        t0 = time.time()
        while True:
            bytes_in_buffer = self._uart.in_waiting

            if num_bytes and num_bytes <= bytes_in_buffer:
                to_read = num_bytes
            else:
                to_read = bytes_in_buffer

            if to_read > 0:
                if self.__uart_device == self.CU_SERIAL:
                    msg = self._uart.read(to_read)
                    return list(msg)

                elif self.__uart_device == self.CU_LABJACK:
                    msg = self._uart.receive()
                    return msg

            if (time.time() - t0) > self.__timeout:
                raise ExceptionUART('Timeout')

    def write(self, msg: str) -> None:
        """

        Parameters
        ----------
        msg :

        Returns
        -------

        """
        self.transmit(msg)

    def read(self, num_bytes: int = None) -> Union[List, str, int]:
        """

        Parameters
        ----------
        num_bytes :

        Returns
        -------

        """
        return self.receive(num_bytes)

    def receive_byte(self) -> int:
        """

        Returns
        -------

        """
        msg = self.receive(1)
        if len(msg) > 1:
            raise ExceptionUART('Too many bytes')

        return msg[0]

    def close(self) -> None:
        """

        Returns
        -------

        """

        self._uart.close()

    def reset_input_buffer(self) -> None:
        """

        Returns
        -------

        """
        if hasattr(self._uart, "reset_input_buffer"):
            self._uart.reset_input_buffer()


class SimpleUARTProt(UARTCommon):
    """
    Simple UART protocol:
    ---------------------//----------
    |cnt of bytes*| 1 | 2 | n | CRC8 |
    ---------------------//----------

    * Count of bytes without first byte.
    """
    CRC_TYPE = 'crc8'

    def __init__(self, device: str = 'ANY', connection_type: str = 'ANY', id: str = 'ANY', port: str = None,
                 baud_rate: int = 9600, pin_tx: str = None, pin_rx: str = None,
                 dev_handle: int = None, timeout: float = 1.0):
        """
        Creates a new UART device.

        Parameters
        ----------
        device : str
            Device Type. "T4", "T7" or "ANY"
        connection_type : str
            Can be: "ANY", "USB", "TCP", "ETHERNET", and "WIFI".
        id : str
            This can be a serial number, IP address, "ANY"
            or device name
        port : str
            Path to serial device. Starts with "/dev"
        baud_rate : int
            Baud rate
        pin_tx : str
            Transceiver pin number
        pin_rx : str
            Receiver pin number
        dev_handle : int
            Device handle to an existing Labjack device
        timeout : float
            Timeout in seconds
        """
        super().__init__(device, connection_type, id, port, baud_rate, pin_tx, pin_rx, dev_handle, timeout)
        self.crc = predefined.mkPredefinedCrcFun(self.CRC_TYPE)

    def __calc_checksum(self, msg: Union[List, bytes]) -> int:
        """
        Calculates the CRC checksum for a message.

        Parameters
        ----------
        msg : Union[List, bytes]
            Message for which the checksum will be calculated.

        Returns
        -------
        int
            Checksum as integer.
        """
        if isinstance(msg, str):
            msg = msg.encode()

        msg = bytearray(msg)
        checksum = self.crc(msg)
        return checksum

    def read(self, format: Type[str] = None) -> Union[List[int], str]:
        """
        Read/receive a message from UART and verifies the checksum.

        Parameters
        ----------
        format : Type[str]
            Output format. If format is "str", a string will be returned. Otherwise a list of bytes.

        Raises
        ------
            ExceptionUART: If checksum was wrong.

        Returns
        -------
        Union[List[int], str]
            Received message without protocol frame.
        """
        buf = []

        while True:
            buf += super().receive()

            if len(buf) > 0:
                expected_bytes = buf[0]
                if expected_bytes == len(buf) - 1:
                    break

        checksum = self.__calc_checksum(buf[1:])

        if checksum != 0:
            raise ExceptionUART(f'Checksum Error: {checksum}, {str(buf)}')

        buf = buf[1:-1]
        if format is str:
            return ''.join([chr(c) for c in buf])

        return buf

    def write(self, payload: Union[str, bytes], format: str = None):
        """
        Write/send/transmit a message. Calculates the checksum and adds the amount of bytes.

        Parameters
        ----------
        payload : Union[str, bytes]
            The message which will be send.
        format : str
            A string which contains the desired format of the message. Contains a syntax for struct.pack() function.

        Raises
        ------
            ExceptionUART: If wrong format type.

        """
        if isinstance(payload, str) and not format:
            payload = payload.encode()
            data = struct.pack('={}B'.format(len(payload)), *payload)
        elif format:
            data = struct.pack(format, *payload)
        else:
            raise ExceptionUART('Wrong Data format')

        checksum = self.__calc_checksum(data)
        msg = [len(data) + 1] + list(data) + [checksum]
        super().transmit(msg)


if __name__ == '__main__':
    uart = UARTCommon(UARTCommon.CU_LABJACK)
    # data = [1, 2, 3, 4, 5, 6, 7, 8]
    data = 'flash\n'
    uart.transmit(data)
    res = uart.receive()
    print(res)
    uart.close()
