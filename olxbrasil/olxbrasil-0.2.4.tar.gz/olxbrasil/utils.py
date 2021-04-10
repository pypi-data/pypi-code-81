from typing import Optional, Any, NoReturn

from olxbrasil.constants import (
    ALLOWED_BOOLEAN_FILTERS,
    ALLOWED_DYNAMIC_FILTERS,
)


def format_price(price: Optional[str] = None) -> float:
    try:
        price_value = (
            price.replace("R$ ", "").replace(".", "").replace(",", ".")
        )
        return float(price_value)
    except (ValueError, AttributeError):
        return 0


def build_boolean_parameters(*olx_filters: str) -> dict:
    params = {}
    for olx_filter in olx_filters:
        if olx_filter not in ALLOWED_BOOLEAN_FILTERS:
            continue

        for key, value in ALLOWED_BOOLEAN_FILTERS[olx_filter].items():
            append_parameter(params, key, value)

    return params


def build_search_parameters(**parameters) -> dict:
    params = {}
    for search_filter, value in parameters.items():
        if search_filter not in ALLOWED_DYNAMIC_FILTERS:
            continue

        chosen_value = value
        chosen_filter = ALLOWED_DYNAMIC_FILTERS[search_filter]
        if chosen_filter.get("has_parse_dict"):
            try:
                chosen_value = chosen_filter["parse_dict"][value]
            except KeyError:
                chosen_value = list(chosen_filter["parse_dict"].values())[0]

        append_parameter(params, chosen_filter["filter_name"], chosen_value)

    return params


def append_parameter(parameters: dict, parameter: str, value: Any) -> NoReturn:
    if parameter in parameters and not isinstance(parameters[parameter], list):
        parameters[parameter] = sorted([parameters[parameter], value])
    elif parameter not in parameters:
        parameters[parameter] = value
    else:
        parameters[parameter].append(value)
