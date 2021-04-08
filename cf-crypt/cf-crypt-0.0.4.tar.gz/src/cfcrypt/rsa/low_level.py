import typing

from cryptography import exceptions
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, utils
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from cryptography.hazmat.primitives.hashes import HashAlgorithm

from .types import RSAKeySet
from .exceptions import InvalidSignature, EncryptionFailed, DecryptionFailed


def encrypt(message: bytes, public_key: RSAKeySet) -> bytes:
	"""Encrypt the bytes with the key."""
	if not isinstance(public_key, (RSAPrivateKey, RSAPublicKey)):
		public_key = public_key[0]
	if isinstance(public_key, RSAPrivateKey):
		public_key = public_key.public_key()

	try:
		ciphertext = public_key.encrypt(
			message,
			padding.OAEP(
				mgf=padding.MGF1(algorithm=hashes.SHA256()),
				algorithm=hashes.SHA256(),
				label=None
			)
		)
		return ciphertext
	except ValueError:
		pass
	raise EncryptionFailed('Encryption failed')


def decrypt(ciphertext: bytes, private_keys: RSAKeySet) -> bytes:
	"""Decrypt the bytes with the key."""
	if isinstance(private_keys, (RSAPrivateKey, RSAPublicKey)):
		private_keys = (private_keys,)
	pad = padding.OAEP(
				mgf=padding.MGF1(algorithm=hashes.SHA256()),
				algorithm=hashes.SHA256(),
				label=None
			)
	for private_key in private_keys:
		try:
			message = private_key.decrypt(ciphertext, pad)
			return message
		except ValueError:
			pass
	raise DecryptionFailed('Decryption failed')


def sign(digest: bytes, private_key: RSAKeySet, chosen_hash: typing.Optional[HashAlgorithm] = None) -> bytes:
	"""Generate a signature for the bytes with the key."""
	if not isinstance(private_key, (RSAPrivateKey, RSAPublicKey)):
		private_key = private_key[0]

	if chosen_hash is None:
		chosen_hash = hashes.SHA256()

	return private_key.sign(
		digest,
		padding.PSS(
			mgf=padding.MGF1(hashes.SHA256()),
			salt_length=padding.PSS.MAX_LENGTH
		),
		utils.Prehashed(chosen_hash)
	)


def verify(
		digest: bytes, sig: bytes, public_keys: RSAKeySet,
		chosen_hash: typing.Optional[HashAlgorithm] = None) -> None:
	"""Verify the given signature matches the bytes."""
	if isinstance(public_keys, (RSAPrivateKey, RSAPublicKey)):
		public_keys = (public_keys,)

	if chosen_hash is None:
		chosen_hash = hashes.SHA256()
	pad = padding.PSS(
					mgf=padding.MGF1(hashes.SHA256()),
					salt_length=padding.PSS.MAX_LENGTH
				)
	pre_hash = utils.Prehashed(chosen_hash)

	for public_key in public_keys:
		try:
			public_key.verify(sig, digest, pad, pre_hash)
			return
		except exceptions.InvalidSignature:
			pass
	raise InvalidSignature('Signature verification failed')
