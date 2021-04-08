from typing import TypeVar, Iterable, Union

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey

RSAKey = TypeVar('RSAKey', RSAPrivateKey, RSAPublicKey)
RSAPrivateKeySet = TypeVar("RSAPrivateKeySet", Iterable[RSAPrivateKey], RSAPrivateKey)
RSAPublicKeySet = TypeVar("RSAPublicKeySet", Iterable[RSAPublicKey], RSAPublicKey)
RSAKeySet = TypeVar("RSAKeySet", Iterable[Union[RSAPrivateKey, RSAPublicKey]], Union[RSAPrivateKey, RSAPublicKey])
