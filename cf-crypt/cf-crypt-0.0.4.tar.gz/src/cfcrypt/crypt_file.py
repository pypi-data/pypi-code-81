"""Provides a container format and implementation to store files on disk encrypted."""

import io
import os

import typing
from cryptography.hazmat.primitives import ciphers
from cryptography.hazmat.primitives.ciphers import algorithms, modes

from ._crypt_file import EncryptedIOBase
from .file_format import ContainerFormat
from .message_authentication import MessageAuthenticatorRSA

from .constants import ALGO_AES, ALGO_MODE_CTR, PAD_NONE, HASH_SHA256, MAC_RSA_SIGNED, SIZE_8MiB, PathLike
from .rsa.types import RSAPrivateKeySet

__all__ = ['CryptFileTextIO', 'CryptFileBinaryIO']


class CryptFileBinaryIO(EncryptedIOBase):
	"""Implementation of EncryptedIO using AES-CTR

	Writing:
		The rsa_key is used to lock the file after writing, providing secrecy of the symmetric keys.
		The private_key is used to sign the file after writing, providing material for Integrity and Authentication.

	Reading:
		The private_key is used to unlock the file for reading, removing the secrecy of the symmetric keys.
		The rsa_key is used to verify the signature, proving Integrity and Authentication.
	"""

	def __init__(self, filename: PathLike, mode, encryption_key: RSAPrivateKeySet, signing_key: RSAPrivateKeySet, *args, **kwargs):

		self._config = {
			'algorithm': ALGO_AES,
			'algorithm_mode': ALGO_MODE_CTR,
			'algorithm_pad': PAD_NONE,
			'algorithm_mac': MAC_RSA_SIGNED,
			'algorithm_mac_hash': HASH_SHA256,
		}

		self.signing_key_private = signing_key

		self.encryptor_finalized = False

		self._encryptor = None
		self.mac_object = None

		super(CryptFileBinaryIO, self).__init__(filename, mode, encryption_key, *args, **kwargs)

	@property
	def _encryption_config(self):
		return self._config

	@property
	def finalized(self):
		return self.writable() and self.encryptor_finalized

	@property
	def cipher(self):
		"""Construct and return the Cipher object base on the encryption config.

		Note: We should **not** cache the cipher object. We need to issue a fresh instance every time self.counter changes.

		:meta private:
		"""
		if self.header.algorithm != self._encryption_config['algorithm']:
			raise RuntimeError('Encryption algorithm not supported')
		if self.header.algorithm_mode != self._encryption_config['algorithm_mode']:
			raise RuntimeError('Encryption mode not supported')

		# Note: We need to keep the nonce in sync with the file position. This gets out of sync if we seek around the
		# file, so we have to manually re-sync it.
		nonce = add_int_to_bytes(self.nonce, self.counter, self.block_size)
		algorithm = algorithms.AES(self.key)
		algorithm_mode = modes.CTR(nonce)
		return ciphers.Cipher(algorithm, algorithm_mode)

	@property
	def mac(self):
		"""Construct and return the message authenticator.

		:meta private:
		"""
		if self.header.algorithm_mac != self._encryption_config['algorithm_mac']:
			raise RuntimeError('MAC algorithm not supported')
		if self.header.algorithm_mac_hash != self._encryption_config['algorithm_mac_hash']:
			raise RuntimeError('Hash algorithm not supported')
		if not self.mac_object:
			self.mac_object = MessageAuthenticatorRSA(self.signing_key_private)
		return self.mac_object

	@property
	def decryptor(self):
		"""Return a fresh decryptor.

		NOTE: It's important that we use a fresh decryptor after any seek operation. This gives us a chance to update
		the counter value to match the seek location. For contagious reads this is not an issue as it gets managed
		internally to the cipher.

		:meta private:
		"""
		return self.cipher.decryptor()

	@property
	def encryptor(self):
		"""Return the active encryptor.

		Note: It's important that we use the same encryptor when writing to the file. We need the internal nonce values
		to stay in sync so we can decrypt the stream later.

		:meta private:
		"""
		if self.finalized:
			raise RuntimeError('This file has been finalized.')
		if self._encryptor is None:
			self._encryptor = self.cipher.encryptor()
		return self._encryptor

	def _read_file_header(self, fh: io.FileIO):
		"""Construct a file header object from the given file handle."""
		return ContainerFormat.create_from_file(fh)

	def verify(self):
		"""Check the file signature matches the given identity key. Verify that file has not been modified since creation."""
		mac = self.mac
		head = self.tell()
		try:
			self.fh.seek(0)

			mac_offset = self.header.mac_offset
			mac_length = self.header.mac_length

			data_end = mac_offset

			bytes_read = 0
			while True:
				chunk = max(min(data_end - bytes_read, SIZE_8MiB), 0)
				data = self.fh.read(chunk)
				if not data:
					break
				bytes_read += len(data)

				mac.update(data)

			self.fh.seek(mac_offset)
			signature = self.fh.read(mac_length)
			self.mac.verify(signature)

		finally:
			self.seek(head)
			self.verification_complete = True

		return True

	def _create_header(self):
		"""Construct a file header object for a new file."""

		chunk_size = -1

		header = ContainerFormat.create(
			self._encryption_config['algorithm'], self._encryption_config['algorithm_mode'], self._encryption_config['algorithm_pad'],
			self._encryption_config['algorithm_mac'], self._encryption_config['algorithm_mac_hash'], chunk_size,
			nonce_length=len(self.nonce),
			key_length=len(self._encrypted_symmetric_key()),
			)

		return header

	def generate_key_material(self):
		"""Generate the symmetric key material for the file encryption.

		:meta private:
		"""
		key_material = os.urandom(32)
		nonce = os.urandom(16)
		return key_material, nonce

	def finalize(self):
		"""Complete the writing operations by appending a cryptographic signature. Once finalized you can no longer
		write more data to the stream."""
		if not self.writable():
			raise io.UnsupportedOperation('This file is not open write mode.')
		if self.finalized:
			raise io.UnsupportedOperation('This file has already been finalized.')

		encrypted_data = self.encryptor.finalize()
		self.fh.write(encrypted_data)

		if self.mac:
			authentication = self.mac.finalize()
			self.fh.write(authentication)

		self.fh.flush()
		self.fh.close()

		self.encryptor_finalized = True


class CryptFileTextIO(io.TextIOWrapper):
	"""A buffered text stream wrapper on CryptFileBinaryIO."""

	def __init__(self, filename: PathLike, encryption_key: RSAPrivateKeySet, signing_key: RSAPrivateKeySet,
				 mode: str = 'r', verify=True, encoding=None, errors=None, newline=None, line_buffering=False,
				 write_through=False):

		if encryption_key is None:
			raise TypeError('CryptFileTextIO expected an encryption_key')
		if encryption_key is None:
			raise TypeError('CryptFileTextIO expected a signing_key')

		if mode in ('r', 'rb'):
			mode = 'rb'
		elif mode in ('w', 'wb'):
			mode = 'wb'
		else:
			raise io.UnsupportedOperation(f'Mode "{mode}" not supported. Mode must be one of "r", "w"')

		buffer = CryptFileBinaryIO(filename, mode, encryption_key, signing_key, verify)
		buffer = typing.cast(typing.IO[bytes], buffer)
		super(CryptFileTextIO, self).__init__(buffer, encoding, errors, newline, line_buffering, write_through)


def add_int_to_bytes(b, i, block_size):
	"""Add an integer to a byte string."""
	MAX = int.from_bytes(b'\xff' * block_size, byteorder='big') + 1
	# If the counter overflows, it wraps back to zero
	i = (int.from_bytes(b, byteorder='big') + i) % MAX
	return i.to_bytes(block_size, 'big')
