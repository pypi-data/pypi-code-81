from enum import Enum


class Device(str, Enum):
    IonQDevice = "aws/ionq/ionQdevice"
    Aspen8 = "aws/rigetti/Aspen-8"
    Aspen9 = "aws/rigetti/Aspen-9"
