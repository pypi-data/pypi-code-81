from twopilabs.utils.scpi import *


class ScpiSystem(object):
    """Class containing SCPI commands concerning SYSTEM subsystem"""

    def __init__(self, device: ScpiDevice) -> None:
        self.device = device

    def error_next(self):
        return self.device.execute('SYST:ERR:NEXT?', result=ScpiEvent)
