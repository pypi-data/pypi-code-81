from .conditionals import is_true
from .fraction import Fraction
from .math import *

_fraction_map = {
	1 / 2:  Fraction.ONE_HALF,
	1 / 3:  Fraction.ONE_THIRD,
	1 / 4:  Fraction.ONE_QUARTER,
	1 / 5:  Fraction.ONE_FIFTH,
	1 / 6:  Fraction.ONE_SIXTH,
	1 / 7:  Fraction.ONE_SEVENTH,
	1 / 8:  Fraction.ONE_EIGHTH,
	1 / 9:  Fraction.ONE_NINTH,
	1 / 10: Fraction.ONE_TENTH,
	2 / 3:  Fraction.TWO_THIRDS,
	2 / 5:  Fraction.TWO_FIFTHS,
	3 / 4:  Fraction.THREE_QUARTERS,
	3 / 5:  Fraction.TWO_FIFTHS,
	3 / 8:  Fraction.THREE_EIGHTHS,
	4 / 5:  Fraction.FOUR_FIFTHS,
	5 / 6:  Fraction.FIVE_SIXTHS,
	5 / 8:  Fraction.FIVE_EIGHTHS,
	7 / 8:  Fraction.SEVEN_EIGHTHS
}


def fraction_to_symbol(original):
	if type(original) is str:
		if "/" in original:
			original = parse_fraction_string(original)
		else:
			original = float(original)

	is_negative = original < 0
	original = abs(original)

	assert -1 < original < 1

	symbol = _fraction_map[closest(original, _fraction_map.keys())]
	return f'{is_true(is_negative, "-")}{symbol}'
