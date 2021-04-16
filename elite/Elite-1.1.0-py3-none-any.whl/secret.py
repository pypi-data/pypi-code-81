'''
Key module for Elite. This module is for generating and operating with
private and public keys, as well as performing key agreement with peer
and creating shared secrets for encrypting.
'''

from ecdsa import SigningKey, VerifyingKey, SECP256k1, NIST384p, ECDH
from ecdsa.keys import MalformedPointError
from enum import IntEnum
from elite import EliteError
from .utils import ashex
from hashlib import sha256, sha384
from typing import Tuple, Union

__all__ = ['EliteKeyError', 'CurveKind', 'UnsupportedCurve', 'KeyExport', 'PrivateKey',
           'PublicKey', 'generate', 'generate_pair', 'shared_secret', 'public_key_size']

class EliteKeyError(EliteError):
    'General base class for key errors.'

class CurveKind(IntEnum):
    'Enumerates the name of the curves.'
    # unknown curve
    CK_UNKNOWN = 0
    # secp256k1
    CK_SECP256K1 = 1
    # secp384r1
    CK_SECP384R1 = 2

# curve mapping
curve_map = {
    CurveKind.CK_SECP256K1: SECP256k1,
    CurveKind.CK_SECP384R1: NIST384p
    }

class UnsupportedCurve(EliteKeyError):
    'Curve is not supported.'
    def __init__(self, kind: CurveKind):
        self.kind = kind
        super().__init__('{!s} is not supported'.format(kind))

class CurveKindMismatch(EliteKeyError):
    'The provided key does not match the curve.'
    def __init__(self, kind: CurveKind):
        self.kind = kind
        super().__init__('key is not of curve {!s}'.format(kind))

class KeyExport:
    'A key export which describes the key.'
    def __init__(self, key: Union[SigningKey, VerifyingKey]):
        'Initializes a new instance. For internal use only.'
        self._key = key
    @property
    def fingerprint(self) -> str:
        'Gets the sha-256 fingerprint of the key.'
        data = sha256(self._key.to_string()).digest()
        return ashex(data, ':', 2)
    @property
    def binary(self) -> bytes:
        'Gets the binary data of the key.'
        return self._key.to_string()
    @property
    def hexadecimal(self) -> bytes:
        'Returns the hex value of the binary data.'
        return self.binary.hex()
        
class PublicKey:
    'Represents an ECC public key.'
    def __init__(self, key: VerifyingKey):
        'Initializes a new instance. For internal use only.'
        self._key = key
    def export(self) -> KeyExport:
        'Returns a key export containing the information about this key.'
        return KeyExport(self._key)
    @staticmethod
    def fromHex(value: str, kind: CurveKind) -> 'PublicKey':
        'Constructs a public key from a hexadecimal value.'
        return PublicKey.fromBinary(bytes.fromhex(value), kind)
    @staticmethod
    def fromBinary(value: bytes, kind: CurveKind) -> 'PublicKey':
        'Constructs a public key from a binary value.'
        if kind in curve_map:
            try:
                return PublicKey(VerifyingKey.from_string(value, curve_map[kind], hashfunc=sha384))
            except MalformedPointError:
                raise CurveKindMismatch(kind) from None
        raise UnsupportedCurve(kind)

class PrivateKey:
    'Represents an ECC private key.'
    def __init__(self, key: SigningKey):
        'Initializes a new instance. For internal use only.'
        self._key = key
    def publicKey(self) -> PublicKey:
        'Returns the public key of this key.'
        return PublicKey(self._key.get_verifying_key())
    def export(self) -> KeyExport:
        'Returns a key export containing the information about this key.'
        return KeyExport(self._key)

def generate(kind: CurveKind) -> PrivateKey:
    'Generates a new key using given curve.'
    if kind in curve_map:
        return PrivateKey(SigningKey.generate(curve_map[kind], hashfunc=sha384))
    raise UnsupportedCurve(kind)

def generate_pair(kind: CurveKind) -> Tuple[PrivateKey, PublicKey]:
    'Generates a pair of keys using given curve.'
    private = generate(kind)
    public = private.publicKey()
    return private, public

def shared_secret(kind: CurveKind, priv_key: PrivateKey, pub_key: PublicKey) -> bytes:
    'Performs ECDH key agreement on two keys.'
    if kind in curve_map:
        curve = curve_map[kind]
    else:
        raise UnsupportedCurve(kind)
    ecdh = ECDH(curve, priv_key._key, pub_key._key)
    return ecdh.generate_sharedsecret_bytes()

def public_key_size(kind: CurveKind) -> int:
    'Gets the public key size of specific curve.'
    if kind in curve_map:
        return curve_map[kind].verifying_key_length
    raise UnsupportedCurve(kind)
