from twopilabs.utils.scpi import *
from .x1000_base import SenseX1000Base


class ScpiTrigger(object):
    """Class containing SCPI commands concerning the TRIGGER subsystem"""

    def __init__(self, device: ScpiDevice) -> None:
        self.device = device

    def immediate(self):
        self.device.execute("TRIG:IMMEDIATE")
        self.device.raise_error()

    def source(self, source: Optional[SenseX1000Base.TrigSource] = None) -> SenseX1000Base.TrigSource:
        """Sets or gets the trigger source"""
        if source is not None:
            self.device.execute('TRIG:SOURCE', param=ScpiChars(source.name))
        else:
            source = SenseX1000Base.TrigSource[self.device.execute('TRIG:SOURCE?', result=ScpiChars).as_string()]

        self.device.raise_error()
        return source
