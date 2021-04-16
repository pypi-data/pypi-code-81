'''
This module provides top-level encryption scheme that is already fully
integrated, ready for use. You can also define your own encryption schemes.
Predefined ones include secp256k1 with AES_EAX and secp384r1 with AES_GCM.
'''

from ecdsa.keys import BadSignatureError
from elite import EliteError
from .cipher import *
from .secret import *
from .utils import *

__all__ = ['getscheme', 'ECCScheme', 'P256k1AesEaxScheme', 'P384r1AesGcmScheme']

class EliteSchemeError(EliteError):
    'General base class for scheme errors.'

class MissingRemoteKey(EliteSchemeError):
    'Remote key is missing.'

class ECCScheme:
    'Represents an ecc scheme.'
    def __init__(self, kind: CurveKind, provider: CryptoProvider):
        'Initializes a new instance with a private key and a crypto provider.'
        self._kind = kind
        self._privateKey = generate(kind)
        self._publicKey = self._privateKey.publicKey()
        self._remoteKey = None
        self._provider = provider
    def _check(self) -> None:
        'Checks if the remote key is present.'
        if self._remoteKey is None:
            raise MissingRemoteKey
    def exportBinaryKey(self) -> bytes:
        'Exports the binary version of the public key.'
        return self._publicKey.export().binary
    def exportHexKey(self) -> str:
        'Exports the hex version of the public key.'
        return self._publicKey.export().hexadecimal
    def importBinaryKey(self, key: bytes) -> bytes:
        'Imports the binary version of the remote key.'
        self._remoteKey = PublicKey.fromBinary(key, self._kind)
    def importHexKey(self, key: str) -> str:
        'Imports the hex version of the remote key.'
        self._remoteKey = PublicKey.fromHex(key, self._kind)
    @property
    def privateKey(self) -> PrivateKey:
        'Gets the private key.'
        return self._privateKey
    @property
    def publicKey(self) -> PublicKey:
        'Gets the public key.'
        return self._publicKey
    @property
    def remoteKey(self) -> PublicKey:
        'Gets the remote key.'
        return self._remoteKey
    def sign(self, data: bytes) -> bytes:
        'Signs the data with remote key.'
        return self._privateKey._key.sign(data)
    def verify(self, data: bytes, signature: bytes) -> bool:
        'Verified the data with local private key.'
        self._check()
        try:
            self._remoteKey._key.verify(signature, data)
            return True
        except BadSignatureError:
            return False
    def encrypt(self, data: bytes) -> bytes:
        'Encrypts the specific data with remote key.'
        self._check()
        ephemeral = generate(self._kind)
        ephemeral_pub = ephemeral.publicKey()
        secret = shared_secret(self._kind, ephemeral, self._remoteKey)
        key, salt = derive_key(secret)
        data = self._provider.encrypt(key, data)
        return ephemeral_pub.export().binary + salt + data
    def decrypt(self, data: bytes) -> bytes:
        'Decrypts the specific data with local private key.'
        ephemeral, salt, data = split_data(data, public_key_size(self._kind), get_salt_size())
        ephemeral = PublicKey.fromBinary(ephemeral, self._kind)
        secret = shared_secret(self._kind, self._privateKey, ephemeral)
        key = derive_key(secret, salt)[0]
        data = self._provider.decrypt(key, data)
        return data
    def secret(self) -> bytes:
        'Gets the established shared secret.'
        self._check()
        return shared_secret(self._kind, self._privateKey, self._remoteKey)

class P256k1AesEaxScheme(ECCScheme):
    'Secp256k1 with AES_EAX.'
    def __init__(self):
        'Initializes a new instance.'
        super().__init__(CurveKind.CK_SECP256K1, AesEaxCryptoProvider())

class P384r1AesGcmScheme(ECCScheme):
    'Secp384r1 with AES_GCM.'
    def __init__(self):
        'Initializes a new instance.'
        super().__init__(CurveKind.CK_SECP384R1, AesGcmCryptoProvider())

def getscheme() -> ECCScheme:
    'Gets the default scheme.'
    return P256k1AesEaxScheme()
