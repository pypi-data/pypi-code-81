class Time:
	MILLISECOND = 1
	SECOND = 1000
	MINUTE = 60000
	HOUR = 3600000
	DAY = 86400000
	WEEK = 604800000


def days(multiplier):
	return multiplier * Time.DAY


def hours(multiplier):
	return multiplier * Time.HOUR


def milliseconds(multiplier):
	return multiplier * Time.MILLISECOND


def minutes(multiplier):
	return multiplier * Time.MINUTE


def seconds(multiplier):
	return multiplier * Time.SECOND


def weeks(multiplier):
	return multiplier * Time.WEEK