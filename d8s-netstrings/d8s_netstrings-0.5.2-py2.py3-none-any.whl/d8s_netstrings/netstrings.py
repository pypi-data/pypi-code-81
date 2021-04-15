def string_to_netstring_ascii(string: str, *args):
    """Convert the given string to a netstring (and return it's ascii representation)."""
    netstring = f'{len(string)}:{string},'

    if any(args):
        for arg in args:
            netstring += string_to_netstring_ascii(arg)
        netstring = string_to_netstring_ascii(netstring)

    return netstring


def string_to_netstring_hex(string: str, *args):
    """Convert the given string to a netstring (and return it's hex representation)."""
    netstring_ascii = string_to_netstring_ascii(string, *args)
    nestring_hex = netstring_ascii_to_netstring_hex(netstring_ascii)
    return nestring_hex


def netstring_ascii_to_netstring_hex(netstring_ascii: str):
    """Convert a netstring (represented as ascii) to its hex representation."""
    from d8s_strings import string_to_hex  # pylint: disable=C0415

    nestring_hex = string_to_hex(netstring_ascii, seperator=' ')
    return nestring_hex


def netstring_hex_to_netstring_ascii(netstring_hex: str):
    """Convert a netstring (represented as hex) to its ascii representation."""
    from d8s_strings import hex_to_string  # pylint: disable=C0415

    nestring_ascii = hex_to_string(netstring_hex)
    return nestring_ascii


def netstring_ascii_to_string(netstring_ascii: str):
    """Get the string portion of the given netstring (represented as ascii)."""
    # TODO: there should be a construct for splitting and getting the first item of the split
    _ = netstring_ascii.split(':')[0]
    ascii_string = ':'.join(netstring_ascii.split(':')[1:])
    # this will remove the trailing comma
    ascii_string = ascii_string[:-1]
    return ascii_string


def netstring_hex_to_string(netstring_hex: str):
    """Get the string portion of the given netstring (represented as hex)."""
    netstring_ascii = netstring_hex_to_netstring_ascii(netstring_hex)
    ascii_string = netstring_ascii_to_string(netstring_ascii)
    return ascii_string
