from enum import Enum


class mb(Enum):
    STP1 = 0
    STP2 = 1
    DUMMY = 0
    DO = 1
    PWM = 2
    DI = 3
    ADC = 4
    DIPU = 5
    DIPD = 6


class lite(Enum):
    JOG = 0
    PTP = 1
    CP = 2
    ARC = 3


class mg(Enum):
    JOG = 0
    PTP = 1
    CP = 2
    ARC = 3