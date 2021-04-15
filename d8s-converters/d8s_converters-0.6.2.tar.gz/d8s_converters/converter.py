from typing import Union

import pint

ureg = pint.UnitRegistry()


def _pint_is_valid_unit(unit: str):
    """."""
    if hasattr(ureg, unit):
        return True
    else:
        return False


def convert(quantity: Union[int, float], starting_unit: str, converted_unit: str):
    """Convert the quantity from the starting_unit to the converted_unit."""
    if not _pint_is_valid_unit(starting_unit):
        print(
            f'The given starting_unit ("{starting_unit}") is not a recognized unit. '
            + 'See https://github.com/hgrecco/pint/blob/master/pint/default_en.txt for a list of units '
            + ' and recognized abbreviations/symbols.'
        )
        raise pint.UndefinedUnitError(starting_unit)
    elif not _pint_is_valid_unit(converted_unit):
        print(
            f'The given converted_unit ("{converted_unit}") is not a recognized unit. '
            + 'See https://github.com/hgrecco/pint/blob/master/pint/default_en.txt for a list of units '
            + ' and recognized abbreviations/symbols.'
        )
        raise pint.UndefinedUnitError(converted_unit)
    else:
        pint_starting_quantity = ureg.Quantity(quantity, starting_unit)
        pint_converted_quantity = pint_starting_quantity.to(converted_unit)
        return pint_converted_quantity.m
