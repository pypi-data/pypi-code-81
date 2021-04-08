from twopilabs.utils.scpi import *


class ScpiCore(object):
    """Class containing core SCPI commands"""

    def __init__(self, device: ScpiDevice) -> None:
        self.device = device

    def idn(self) -> List[str]:
        """Eecutes a *IDN? command to read device identification string"""
        idn = self.device.execute('*IDN?', result=ScpiChars)
        return idn.as_string().split(',')

    def cls(self) -> None:
        """Executes a *CLS command to clear all status data structures in the device"""
        self.device.execute('*CLS')

    def rst(self) -> None:
        """Executes a *RST command to stop execution of all overlapped (asynchronous) commands and resets the device"""
        self.device.execute('*RST')

    def trg(self) -> None:
        """Executes a *TRG command to soft-trigger the device in initiated state waiting for a trigger"""
        self.device.execute('*TRG')

    def wai(self) -> None:
        """Executes a *WAI command to wait for all overlapped (asynchronous) commands to finish"""
        self.device.execute('*WAI')

    def opc(self) -> bool:
        """Executes a *OPC? command to wait for all overlapped (asynchronous) commands to finish and returns '1'"""
        completed = self.device.execute('*OPC?', result=ScpiBool)
        return completed.as_bool()
