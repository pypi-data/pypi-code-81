from . import internal

Default = internal.Default


def is_equal(original_val, test_val, return_val=Default.PARAMETER, else_val=''):
	if original_val == test_val:
		if return_val is Default.PARAMETER:
			return_val = original_val
		return return_val

	return else_val


def is_even(test_val, return_val=Default.PARAMETER, else_val=''):
	if test_val % 2 == 0:
		if return_val is Default.PARAMETER:
			return_val = test_val
		return return_val

	return else_val


def is_false(test_val, return_val=Default.PARAMETER, else_val=''):
	if not test_val:
		if return_val is Default.PARAMETER:
			return_val = test_val
		return return_val

	return else_val


def is_gt(original_val, test_val, return_val=Default.PARAMETER, else_val=''):
	if original_val > test_val:
		if return_val is Default.PARAMETER:
			return_val = original_val
		return return_val

	return else_val


def is_gte(original_val, test_val, return_val=Default.PARAMETER, else_val=''):
	if original_val >= test_val:
		if return_val is Default.PARAMETER:
			return_val = original_val
		return return_val

	return else_val


def is_lt(original_val, test_val, return_val=Default.PARAMETER, else_val=''):
	if original_val < test_val:
		if return_val is Default.PARAMETER:
			return_val = original_val
		return return_val

	return else_val


def is_lte(original_val, test_val, return_val=Default.PARAMETER, else_val=''):
	if original_val <= test_val:
		if return_val is Default.PARAMETER:
			return_val = original_val
		return return_val

	return else_val


def is_none(test_val, return_val=Default.PARAMETER, else_val=''):
	if test_val is None:
		if return_val is Default.PARAMETER:
			return_val = test_val
		return return_val

	return else_val


def is_not_equal(original_val, test_val, return_val=Default.PARAMETER, else_val=''):
	if original_val != test_val:
		if return_val is Default.PARAMETER:
			return_val = original_val
		return return_val

	return else_val


def is_not_none(test_val, return_val=Default.PARAMETER, else_val=''):
	if test_val is not None:
		if return_val is Default.PARAMETER:
			return_val = test_val
		return return_val

	return else_val


def is_odd(test_val, return_val=Default.PARAMETER, else_val=''):
	if test_val % 2 != 0:
		if return_val is Default.PARAMETER:
			return_val = test_val
		return return_val

	return else_val


def is_true(test_val, return_val=Default.PARAMETER, else_val=''):
	if test_val:
		if return_val is Default.PARAMETER:
			return_val = test_val
		return return_val

	return else_val
