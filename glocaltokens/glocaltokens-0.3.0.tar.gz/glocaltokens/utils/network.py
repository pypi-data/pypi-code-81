"""Network utilities"""
import socket

import glocaltokens.utils.types as type_utils


def is_valid_ipv4_address(address):
    """Check if ip address is ipv4"""
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count(".") == 3
    except socket.error:  # not a valid address
        return False

    return True


def is_valid_ipv6_address(address):
    """Check if ip address is ipv6"""
    try:
        socket.inet_pton(socket.AF_INET6, address)
    except socket.error:  # not a valid address
        return False
    return True


def is_valid_port(port) -> bool:
    """Check if port is valid"""
    return type_utils.is_integer(port) and 0 <= port <= 65535
