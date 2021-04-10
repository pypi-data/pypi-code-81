from .internal import Default, is_default_parameter


def is_equal(original_val, test_val, return_val=Default.PARAMETER, else_val=''):
	if original_val == test_val:
		return_val = is_default_parameter(return_val, original_val)
		return return_val

	return else_val


def is_even(test_val, return_val=Default.PARAMETER, else_val=''):
	if test_val % 2 == 0:
		return_val = is_default_parameter(return_val, test_val)
		return return_val

	return else_val


def is_false(test_val, return_val=Default.PARAMETER, else_val=''):
	if not test_val:
		return_val = is_default_parameter(return_val, test_val)
		return return_val

	return else_val


def is_gt(original_val, test_val, return_val=Default.PARAMETER, else_val=''):
	if original_val > test_val:
		return_val = is_default_parameter(return_val, original_val)
		return return_val

	return else_val


def is_gte(original_val, test_val, return_val=Default.PARAMETER, else_val=''):
	if original_val >= test_val:
		return_val = is_default_parameter(return_val, original_val)
		return return_val

	return else_val


def is_lt(original_val, test_val, return_val=Default.PARAMETER, else_val=''):
	if original_val < test_val:
		return_val = is_default_parameter(return_val, original_val)
		return return_val

	return else_val


def is_lte(original_val, test_val, return_val=Default.PARAMETER, else_val=''):
	if original_val <= test_val:
		return_val = is_default_parameter(return_val, original_val)
		return return_val

	return else_val


def is_none(test_val, return_val=Default.PARAMETER, else_val=''):
	if test_val is None:
		return_val = is_default_parameter(return_val, test_val)
		return return_val

	return else_val


def is_not_equal(original_val, test_val, return_val=Default.PARAMETER, else_val=''):
	if original_val != test_val:
		return_val = is_default_parameter(return_val, original_val)
		return return_val

	return else_val


def is_not_none(test_val, return_val=Default.PARAMETER, else_val=''):
	if test_val is not None:
		return_val = is_default_parameter(return_val, test_val)
		return return_val

	return else_val


def is_odd(test_val, return_val=Default.PARAMETER, else_val=''):
	if test_val % 2 != 0:
		return_val = is_default_parameter(return_val, test_val)
		return return_val

	return else_val


def is_true(test_val, return_val=Default.PARAMETER, else_val=''):
	if test_val:
		return_val = is_default_parameter(return_val, test_val)
		return return_val

	return else_val
