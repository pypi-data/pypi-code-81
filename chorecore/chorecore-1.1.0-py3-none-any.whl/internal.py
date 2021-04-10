from enum import Enum


class Default(Enum):
	PARAMETER = None


def is_default_parameter(test_val, return_val):
	if test_val is Default.PARAMETER:
		return return_val
	return test_val
