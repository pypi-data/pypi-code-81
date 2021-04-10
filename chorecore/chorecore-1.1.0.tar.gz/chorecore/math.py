import functools


def closest(needle, arr):
	return functools.reduce(lambda a, b: b if abs(b - needle) < abs(a - needle) else a, arr)


def parse_fraction_string(fraction):
	split = fraction.split("/")
	return int(split[0]) / int(split[1])
