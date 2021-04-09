from decimal import ROUND_HALF_UP, Decimal


def round(f):
    return Decimal(f"{f}").quantize(0, ROUND_HALF_UP).__int__()
