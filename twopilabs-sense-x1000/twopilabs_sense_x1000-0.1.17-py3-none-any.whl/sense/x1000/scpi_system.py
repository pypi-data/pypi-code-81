from twopilabs.utils.scpi import *
import yaml


class ScpiSystem(object):
    """Class containing SCPI commands concerning SYSTEM subsystem"""

    def __init__(self, device: ScpiDevice) -> None:
        self.device = device

    def error_next(self):
        return self.device.execute('SYST:ERR:NEXT?', result=ScpiEvent)

    def info(self):
        """returns a system information dictionary"""
        config = self.device.execute('SYST:INFO?', result=ScpiString).as_bytes()

        self.device.raise_error()
        return yaml.load(config, Loader=yaml.FullLoader)