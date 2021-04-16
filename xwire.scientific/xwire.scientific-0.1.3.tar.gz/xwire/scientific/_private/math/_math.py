import math


def log_return(initial: float, final: float, period: float, decimals=None) -> float:
    if initial == 0 and final == 0:
        return 0
    elif initial == 0 and final > 0:
        return math.inf
    elif final == 0 and initial > 0:
        return -math.inf
    else:
        return_value = math.log(final/initial) / period
        if decimals is not None:
            return round(return_value, decimals)
        else:
            return return_value
