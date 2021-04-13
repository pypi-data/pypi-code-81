from enum import Enum


class QueryCommandsEnumeration(Enum):
    BUFFER_STATUS = 'F'
    FIRMWARE_VERSION = '&'
    FIRMWARE_CHECKSUM = '#'
    PUMP_STATUS = 'Q'
    ABSOLUTE_SYRINGE_POSITION = '?'
    START_VELOCITY = '?1'
    MAXIMUM_VELOCITY = '?2'
    STOP_VELOCITY = '?3'
    ACTUAL_SYRINGE_POSITION = '?4'
    NUMBER_OF_RETURN_STEPS = '?12'
    STATUS_AUXILIARY_INPUT_1 = '?13'
    STATUS_AUXILIARY_INPUT_2 = '?14'
    RETURNS_255 = '?22'
    NUMBER_OF_BACKOFF_STEPS = '?24'
    SYRINGE_STATUS = '?10000'
    SYRINGE_HOME_SENSOR_STATUS = '?10001'
    SYRINGE_MODE = '?11000'
    VALVE_STATUS = '?20000'
    VALVE_TYPE = '?21000'
    VALVE_LOGICAL_POSITION = '?23000'
    VALVE_NUMERICAL_POSITION = '?24000'
    VALVE_ANGLE = '?25000'
    LAST_DIGITAL_OUT_VALUE = '?37000'
    SYRINGE_DIAGNOSTIC_TIMER_VALUE = '?38000'


class PositionInShortestDirection(Enum):
    INPUT = 1
    OUTPUT = 2
    WASH = 3
    RETURN = 4
    BYPASS = 5
    EXTRA = 6


class PSDTypes(Enum):
    psd4 = '4'
    psd6 = '6'
    psd4SmoothFlow = '4sf'
    psd6SmoothFlow = '6sf'





