def find_term_match(values: list, term_id: str, default_val={}):
    """
    Return the element in a list which matches the `Term` with the given `@id`.

    Parameters
    ----------
    values
        The list in which to search for. Example: `cycle['inputs']`.
    term_id
        The `@id` of the `Term`. Example: `sandContent`
    default_val
        The returned value if no match was found.

    Returns
    -------
    dict
        The matching object.
    """
    return next((v for v in values if v.get('term', {}).get('@id') == term_id), default_val)


def find_primary_product(cycle: dict) -> dict:
    """
    Return the `Product` of a `Cycle` which is set to `primary`, `None` if none present.

    Parameters
    ----------
    cycle
        The JSON-LD of the `Cycle`.

    Returns
    -------
    dict
        The primary `Product`.
    """
    products = cycle.get('products', [])
    return next((p for p in products if p.get('primary', False)), products[0]) if len(products) > 0 else None


def _convert_m3_to_kg(value: float, **kwargs): return value * kwargs.get('density')


def _convert_m3_to_l(value: float, **kwargs): return value * 1000


def _convert_kg_to_m3(value: float, **kwargs): return value / kwargs.get('density')


def _convert_kg_to_l(value: float, **kwargs): return value / kwargs.get('density') * 1000


def _convert_liter_to_kg(value: float, **kwargs): return value * kwargs.get('density') / 1000


def _convert_liter_to_m3(value: float, **kwargs): return value / 1000


def _convert_mj_to_kwh(value: float, **kwargs): return value / 3.6


def _convert_kwh_to_mj(value: float, **kwargs): return value * 3.6


CONVERTERS = {
    'm3': {
        'kg': _convert_m3_to_kg,
        'L': _convert_m3_to_l
    },
    'kg': {
        'm3': _convert_kg_to_m3,
        'L': _convert_kg_to_l
    },
    'L': {
        'kg': _convert_liter_to_kg,
        'm3': _convert_liter_to_m3
    },
    'kWh': {
        'MJ': _convert_kwh_to_mj
    },
    'MJ': {
        'kWh': _convert_mj_to_kwh
    }
}


def convert_value(value: float, from_unit: str, to_unit: str, **kwargs: dict) -> float:
    """
    Converts a value of unit into a different unit.
    Depending on the destination unit, additional arguments might be provided by name, see the list of parameters.

    Parameters
    ----------
    value
        The value to convert, usually a float or an integer.
    from_unit
        The unit the value is specified in.
    to_unit
        The unit the converted value should be.
    density
        Optional. When converting from a 2d unit to 3d or the opposite, a density is required.

    Returns
    -------
    float
        The converted value in the destination unit.
    """
    return CONVERTERS[from_unit][to_unit](value, **kwargs)
