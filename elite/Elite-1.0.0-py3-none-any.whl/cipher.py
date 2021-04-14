'''
The cipher module for Elite. Uses the Hmac-based Key Deriviation Function
(HKDF) to generate byte-format keys out of elliptic-curve shared secrets.
The cipher used for the encryption scheme is Advanced Encryption Standard
(AES), which is a popular algorithm of symmetric encryptions.
'''

from Crypto.Cipher import AES
from typing import List
from elite import EliteError
from .utils import split_data
import os

__all__ = ['EliteCryptoError', 'AuthorizationCodeInvalid', 'getprovider',
           'CryptoProvider', 'AesEaxCryptoProvider', 'AesGcmCryptoProvider']

# constants
DEFAULT_NONCE_SIZE = 16
DEFAULT_MAC_SIZE = 16

class EliteCryptoError(EliteError):
    'General base class for cryptographic errors. Class stub.'

class AuthorizationCodeInvalid(EliteCryptoError):
    'The MAC code provided is invalid.'
    def __init__(self, mac: bytes=b''):
        'Initializes with MAC code.'
        super().__init__(mac)
        self.mac = mac

class CryptoProvider:
    'General base class for crypto providers. Defines method stubs.'
    def encrypt(self, key: bytes, data: bytes) -> bytes:
        'Encrypts the specific data.'
        raise NotImplementedError
    def decrypt(self, key: bytes, data: bytes) -> bytes:
        'Decrypts the specific data.'
        raise NotImplementedError

class AesGcmCryptoProvider(CryptoProvider):
    'Represents a AES_GCM crypto provider.'
    def __init__(self, nonce_size: int=DEFAULT_NONCE_SIZE, mac_size: int=DEFAULT_MAC_SIZE):
        'Initializes using given nonce and mac size.'
        self._nonceSize = nonce_size
        self._macSize = mac_size
    def encrypt(self, key: bytes, data: bytes) -> bytes:
        'Encrypts the data using given key.'
        nonce = os.urandom(self._nonceSize)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce, mac_len=self._macSize)
        message, mac = cipher.encrypt_and_digest(data)
        return nonce+mac+message
    def decrypt(self, key: bytes, data: bytes) -> bytes:
        'Decrypts the data using given key.'
        nonce, mac, data = split_data(data, self._nonceSize, self._macSize)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce, mac_len=self._macSize)
        try:
            message = cipher.decrypt_and_verify(data, mac)
            return message
        except ValueError:
            raise AuthorizationCodeInvalid(mac) from None

class AesEaxCryptoProvider(CryptoProvider):
    'Represents a AES_EAX crypto provider.'
    def __init__(self, nonce_size: int=DEFAULT_NONCE_SIZE, mac_size: int=DEFAULT_MAC_SIZE):
        'Initializes using given nonce and mac size.'
        self._nonceSize = nonce_size
        self._macSize = mac_size
    def encrypt(self, key: bytes, data: bytes) -> bytes:
        'Encrypts the data using given key.'
        nonce = os.urandom(self._nonceSize)
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce, mac_len=self._macSize)
        message, mac = cipher.encrypt_and_digest(data)
        return nonce+mac+message
    def decrypt(self, key: bytes, data: bytes) -> bytes:
        'Decrypts the data using given key.'
        nonce, mac, data = split_data(data, self._nonceSize, self._macSize)
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce, mac_len=self._macSize)
        try:
            message = cipher.decrypt_and_verify(data, mac)
            return message
        except ValueError:
            raise AuthorizationCodeInvalid(mac) from None

def getprovider() -> CryptoProvider:
    'Returns a default provider.'
    return AesEaxCryptoProvider()
