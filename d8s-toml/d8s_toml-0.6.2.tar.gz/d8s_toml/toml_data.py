"""Functions to work with toml."""

import toml


def toml_read(toml_data: str):
    """Read the toml data."""
    parsed_toml_data = toml.loads(toml_data)
    return parsed_toml_data


def is_toml(possible_toml_data: str) -> bool:
    """Determine whether the possible_toml_data is valid toml data."""
    try:
        toml_read(possible_toml_data)
    except:  # pylint: disable=W0702  # noqa: E722
        return False
    else:
        return True


# todo: are there other input types possible?
# TODO: can we do this using atomic/safe writing?
def toml_write(data: dict) -> str:
    """Convert the given data to a toml string."""
    result = toml.dumps(data)
    return result
