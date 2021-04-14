'''
Utilitiy functions for Elite.
'''

import sys, os
from Crypto.Protocol.KDF import HKDF
from Crypto.Hash import SHA512
from typing import List, Tuple

if sys.version_info >= (3, 8):
    def ashex(data: bytes, sep: str, count: int):
        'Returns a hex representation with separator and byte count.'
        return data.hex(sep, count)
else:
    def ashex(data: bytes, sep: str, count: int):
        'Returns a hex representation with separator and byte count.'
        value = data.hex()
        return sep.join(value[i:i+count*2] for i in range(0, len(value), count*2))

def split_data(data: bytes, *sizes: int) -> List[bytes]:
    'Splits the data into small chunks.'
    results = []
    for size in sizes:
        results.append(data[:size])
        data = data[size:]
    results.append(data)
    return results

def derive_key(secret: bytes, salt: bytes=b'', length: int=32) -> Tuple[bytes, bytes]:
    'Derives a secret into a cryptographic key.'
    salt = salt or os.urandom(get_salt_size())
    key = HKDF(secret, length, salt, SHA512)
    return key, salt

def get_salt_size() -> int:
    'Gets the salt length.'
    return SHA512.digest_size
