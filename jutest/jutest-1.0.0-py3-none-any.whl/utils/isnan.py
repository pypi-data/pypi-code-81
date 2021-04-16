import math


def isnan(value) -> bool:
    return isinstance(value, float) and math.isnan(value)
