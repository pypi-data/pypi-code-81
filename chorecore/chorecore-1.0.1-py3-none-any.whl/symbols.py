from . import conditionals, fraction, math

_fraction_map = {
	1 / 2:  fraction.Fraction.ONE_HALF,
	1 / 3:  fraction.Fraction.ONE_THIRD,
	1 / 4:  fraction.Fraction.ONE_QUARTER,
	1 / 5:  fraction.Fraction.ONE_FIFTH,
	1 / 6:  fraction.Fraction.ONE_SIXTH,
	1 / 7:  fraction.Fraction.ONE_SEVENTH,
	1 / 8:  fraction.Fraction.ONE_EIGHTH,
	1 / 9:  fraction.Fraction.ONE_NINTH,
	1 / 10: fraction.Fraction.ONE_TENTH,
	2 / 3:  fraction.Fraction.TWO_THIRDS,
	2 / 5:  fraction.Fraction.TWO_FIFTHS,
	3 / 4:  fraction.Fraction.THREE_QUARTERS,
	3 / 5:  fraction.Fraction.TWO_FIFTHS,
	3 / 8:  fraction.Fraction.THREE_EIGHTHS,
	4 / 5:  fraction.Fraction.FOUR_FIFTHS,
	5 / 6:  fraction.Fraction.FIVE_SIXTHS,
	5 / 8:  fraction.Fraction.FIVE_EIGHTHS,
	7 / 8:  fraction.Fraction.SEVEN_EIGHTHS
}


def fraction_to_symbol(original):
	if type(original) is str:
		if "/" in original:
			original = math.parse_fraction_string(original)
		else:
			original = float(original)

	is_negative = original < 0
	original = abs(original)

	assert -1 < original < 1

	symbol = _fraction_map[math.closest(original, _fraction_map.keys())]
	return f'{conditionals.is_true(is_negative, "-")}{symbol}'
