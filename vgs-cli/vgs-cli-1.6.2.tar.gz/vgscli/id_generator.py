import uuid
import base58

base58.alphabet = b'123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'


def base58_to_uuid(base58_string: str, version=4) -> str:
    """
    >>> base58_to_uuid('fBpkbaCp2dqfowSaRDL3g7')
    '765159e7-750c-4b0b-8be0-a07fbc8f3ac4'
    >>> base58_to_uuid('gwBwv1PeYLXpxsMyrSKYbw')
    '7dbf495e-254b-4e76-aaab-1bb5b726a53a'
    """
    raw_bytes = base58.b58decode(base58_string)
    return str(uuid.UUID(bytes=raw_bytes, version=version))


def uuid_to_base58(prefix, id):
    """
    >>> uuid_to_base58('GR', '765159e7-750c-4b0b-8be0-a07fbc8f3ac4')
    'GRfBpkbaCp2dqfowSaRDL3g7'
    >>> uuid_to_base58('GR', '7dbf495e-254b-4e76-aaab-1bb5b726a53a')
    'GRgwBwv1PeYLXpxsMyrSKYbw'
    """
    unencoded_byte_array = bytearray.fromhex(uuid.UUID(id).hex)
    return prefix + base58.b58encode(bytes(unencoded_byte_array)).decode()
