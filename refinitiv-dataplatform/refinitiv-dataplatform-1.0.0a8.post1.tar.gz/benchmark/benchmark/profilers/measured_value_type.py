from enum import Enum, unique


@unique
class MeasuredValueType(Enum):
    time = 'time'
    memory = 'memory'
