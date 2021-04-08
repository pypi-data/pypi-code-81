"""Helpers for working with RSA keys."""
import os
import typing
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey

from .types import RSAPrivateKeySet, RSAPublicKeySet

PathLike = typing.TypeVar("PathLike", str, bytes, os.PathLike)


#
# Create
#

def generate_private_key(key_size: int = 2048) -> RSAPrivateKey:
	"""Create a new RSAPrivateKey"""
	return rsa.generate_private_key(
			public_exponent=65537,
			key_size=key_size,
	)


def generate_private_pem(key_size: int = 2048, password: typing.Optional[str] = None) -> bytes:
	"""Create a new RSAPrivateKey encoded into PEM bytes"""
	private_key = generate_private_key(key_size)
	pem = private_key_to_pem(private_key, password)
	return pem


def generate_keypair(key_size: int = 2048) -> typing.Tuple[RSAPrivateKey, RSAPublicKey]:
	"""Create a new RSAPrivateKey and its matching RSAPublicKey"""
	private_key = generate_private_key(key_size)
	public_key = private_key.public_key()
	return private_key, public_key


#
# Transform
#

def pem_to_private_key(key_bytes, password: typing.Optional[str] = None) -> RSAPrivateKey:
	"""Load PEM bytes into an RSAPrivateKey"""
	if password is not None:
		password = password.encode()
	private_key = serialization.load_pem_private_key(key_bytes, password=password)
	return private_key


def pem_to_keypair(
		key_bytes: bytes, password: typing.Optional[str] = None) -> typing.Tuple[RSAPrivateKey, RSAPublicKey]:
	"""Load PEM bytes into an RSAPrivateKey and its matching RSAPublicKey"""
	private_key = pem_to_private_key(key_bytes, password)
	return private_key, private_key.public_key()


def pem_file_to_private_key(filepath: PathLike, password: typing.Optional[str] = None):
	"""Load PEM bytes from a file into an RSAPrivateKey"""
	filepath = Path(filepath)
	with filepath.open('rb') as fh:
		return pem_to_private_key(fh.read(), password)


def pem_file_to_keypair(
		filepath: PathLike, password: typing.Optional[str] = None) -> typing.Tuple[RSAPrivateKey, RSAPublicKey]:
	"""Load PEM bytes from a file into an RSAPrivateKey and its matching RSAPublicKey"""
	private_key = pem_file_to_private_key(filepath, password)
	return private_key, private_key.public_key()


def private_key_to_pem(private_key: RSAPrivateKey, password: typing.Optional[str] = None) -> bytes:
	"""Serialize an RSAPrivateKey into PEM bytes"""
	if password:
		password = password.encode()
		encryption_algorithm = serialization.BestAvailableEncryption(password)
	else:
		encryption_algorithm = serialization.NoEncryption()

	return private_key.private_bytes(
	   encoding=serialization.Encoding.PEM,
	   format=serialization.PrivateFormat.PKCS8,
	   encryption_algorithm=encryption_algorithm
	)


def private_key_to_pem_file(
		filepath: PathLike, private_key: RSAPrivateKey, password: typing.Optional[str] = None) -> Path:
	"""Serialize an RSAPrivateKey into PEM bytes and write them into a file."""
	filepath = Path(filepath)
	with filepath.open('wb') as fh:
		fh.write(private_key_to_pem(private_key, password))
	return filepath


#
# Pack into KeySets
#

def to_public_key(key_set: typing.Union[RSAPublicKeySet, RSAPrivateKeySet]) -> RSAPublicKey:
	"""Extract a single public key from the key set."""
	key = key_set
	if not isinstance(key_set, (RSAPrivateKey, RSAPublicKey)):
		key = key_set[0]
	if isinstance(key, RSAPrivateKey):
		return key.public_key()
	return key


def to_public_key_set(key_set: RSAPrivateKeySet) -> RSAPublicKeySet:
	"""Recover the RSAPublic key from each RSAPrivateKey in the set."""
	if isinstance(key_set, (RSAPrivateKey, RSAPublicKey)):
		key_set = [key_set, ]
	return [key.public_key() for key in key_set]
