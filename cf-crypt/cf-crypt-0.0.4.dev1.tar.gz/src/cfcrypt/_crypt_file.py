"""Base class for EncryptedIO implementations."""

import io
import warnings
from pathlib import Path
from typing import BinaryIO, Iterable

from .constants import parameter_to_name, PathLike, ReadableBuffer
from .file_format import ContainerFormat

from .rsa import encrypt, decrypt
from .rsa.key_helpers import to_public_key
from .rsa.types import RSAPrivateKeySet


class EncryptedIOBase(io.RawIOBase):
	"""Provides a frame work for reading and writing to and encrypted container file.

	Sub classes should implement the stubs to provide the actual encryption.
	"""

	def __init__(self, filename: PathLike, mode: str, encryption_key: RSAPrivateKeySet, verify: bool = True):
		self.suppress_verification_warning = True

		self.encryption_key_private = encryption_key

		self.read_only = mode == 'rb'
		self.write_only = mode == 'wb'

		self.filename = filename
		if self.read_only:
			self.fh = open(filename, 'rb')
		elif self.write_only:
			self.fh = open(filename, 'wb')
		else:
			raise RuntimeError('File mode not supported.')

		self.block_size = 16
		self.header = None

		self.key = None
		self.nonce = None
		self.counter = 0

		self.data_offset = None
		self.data_length = None

		self.head = 0
		self.block_offset = 0

		self.verification_complete = False
		if self.readable():
			self._prepare_for_reading(verify)
		elif self.writable():
			self._prepare_for_writing()
		else:
			raise RuntimeError('Only reading or writing supported.')

		self.suppress_verification_warning = False

	@property
	def _encryption_config(self) -> dict:
		"""The settings used to setup the encryption library."""
		return dict()

	def _check_encryption_config(self, parameter: str):
		"""Check that the encryption settings the file was generated with match the active encryption settings."""
		hp = self.header[parameter]
		cp = self._encryption_config[parameter]
		if hp != cp:
			raise RuntimeError(
				f'Mismatched parameter: {parameter}. The active encryption setting is {parameter_to_name(parameter, cp)} but '
				f'the file was encrypted with {parameter_to_name(parameter, hp)}.')

	def _prepare_for_reading(self, verify: bool):
		"""Read the header from the file. Get the state needed to decrypt. Run the verification check for file tampering."""
		self.header = self._read_file_header(self.fh)

		for parameter in ('algorithm', 'algorithm_mode', 'algorithm_pad', 'algorithm_mac', 'algorithm_mac_hash'):
			self._check_encryption_config(parameter)

		file_size = Path(self.filename).stat().st_size
		self.header.set_file_size(file_size)

		self.key = self._decrypt_symmetric_key()
		self.nonce = self.header.nonce
		self.data_offset = self.header.data_offset
		self.data_length = self.header.data_length

		if verify:
			self.verify()

		self.fh.seek(self.data_offset)

	def _prepare_for_writing(self):
		"""Setup our state needed for encrypting data. Create the file header and write it to the stream."""
		self.key, self.nonce = self.generate_key_material()
		encrypted_key_material = self._encrypted_symmetric_key()

		self.header = self._create_header()
		self.header.set_nonce(self.nonce)
		self.header.set_key_material(encrypted_key_material)
		self.header.set_mac_length(self.mac.length)

		header_bytes = self.header.to_bytes()
		self._write(header_bytes)
		self._write(self.nonce)
		self._write(encrypted_key_material)

	def _write(self, data: bytes):
		"""Tee the write operation to all the places it needs to go."""
		self.fh.write(data)
		if self.mac:
			self.mac.update(data)

	#
	# Interface
	#

	# Support context manager and therefore supports the with statement. In this example, file is closed after the with
	# statement’s suite is finished—even if an exception occurs
	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, exc_traceback):
		self.suppress_verification_warning = exc_type is not None
		self.close()

	def __iter__(self) -> bytes:
		if not self.readable():
			raise io.UnsupportedOperation('This file is not open read mode.')

		read_length = self.block_offset + self.block_size
		buffer = self.read(read_length)
		while len(buffer) > 0:
			for char in buffer:
				yield char.to_bytes(1, 'big')
			buffer = self.read(self.block_size)

	def close(self):
		"""Flush and close this stream. This method has no effect if the stream is already closed. If the stream has not
		already been finalized, it will now be finalized."""
		if self.fh.closed:
			return

		if self.readable():
			if not self.verification_complete and not self.suppress_verification_warning:
				warnings.warn('This file has not been verified. Do not trust the contents until you run a successful verification.')

		if self.writable():
			if not self.finalized:
				self.finalize()

		self.fh.close()

	@property
	def closed(self) -> bool:
		"""True if the stream is closed."""
		return self.fh.closed

	# noinspection SpellCheckingInspection
	def fileno(self) -> int:
		"""Return the underlying file descriptor (an integer) of the stream if it exists. An OSError is raised if the
		IO object does not use a file descriptor. """
		return self.fh.fileno()

	def finalize(self):
		"""Complete the writing operations by appending a cryptographic signature. Once finalized you can no longer
		write more data to the stream."""
		return NotImplemented

	@property
	def finalized(self) -> bool:
		"""True if the stream has been finalized."""
		return False

	def flush(self):
		"""Flush the write buffers of the stream if applicable. This does nothing for read-only and non-blocking streams."""
		return self.fh.flush()

	# noinspection SpellCheckingInspection
	def isatty(self) -> bool:
		"""Return True if the stream is interactive (i.e., connected to a terminal/tty device)."""
		return False

	def read(self, size=-1) -> bytes:
		"""Read up to size bytes from the object and return them. As a convenience, if size is unspecified or -1,
		all bytes until EOF are returned."""
		if not self.readable():
			raise io.UnsupportedOperation('This file is not open read mode.')

		if size < 0 or size is None:
			size = max(self.data_length - self.head, 0)
		else:
			size = size

		# We need to read from the start of a block to make the decryption work.
		read_size = self.block_offset + size

		decryptor = self.decryptor
		encrypted_data = self.fh.read(read_size)
		data = decryptor.update(encrypted_data) + decryptor.finalize()

		# Don't give the user the extra data between the block start and the head position
		data = data[self.block_offset:]

		# Don't give them more bytes than they asked for.
		data = data[:size]

		# Trim off any data after the edge of the container boundary.
		read_size = len(data)
		if self.head + read_size > self.data_length:
			overshoot = self.head + read_size - self.data_length
			data = data[:read_size - overshoot]
		self.head += len(data)

		# The seek here is important. It puts the file head on a block boundary and sets up
		# the self.block_offset value for the next read.
		self.seek(self.head)
		return data

	def readable(self) -> bool:
		"""Return True if the stream can be read from."""
		return self.read_only

	# noinspection SpellCheckingInspection
	def readline(self, size=-1):
		r"""Read and return one line from the stream. If size is specified, at most size bytes will be read.

		The line terminator is always b'\\n' for binary files; for text files, the newline argument to open() can be
		used to select the line terminator(s) recognized.
		"""
		return NotImplemented

	# noinspection SpellCheckingInspection
	def readlines(self, hint=-1):
		"""
		Read and return a list of lines from the stream. hint can be specified to control the number of lines read:
		no more lines will be read if the total size (in bytes/characters) of all lines so far exceeds hint.

		Note that it’s already possible to iterate on file objects using for line in file: ... without calling
		file.readlines().
		"""
		return NotImplemented

	def seek(self, offset, whence=io.SEEK_SET) -> int:
		"""Change the stream position to the given byte offset. offset is interpreted relative to the position indicated
		by whence. The default value for whence is SEEK_SET. Values for whence are:

			SEEK_SET or 0 – start of the stream (the default); offset should be zero or positive
			SEEK_CUR or 1 – current stream position; offset may be negative
			SEEK_END or 2 – end of the stream; offset is usually negative

		Return the new absolute position."""
		if not self.seekable():
			raise io.UnsupportedOperation('seek')

		if whence == io.SEEK_SET:
			# Relative to the start
			self.head = offset
		elif whence == io.SEEK_CUR:
			# Relative to the current position
			self.head = self.head + offset
		elif whence == io.SEEK_END:
			# Relative to the end
			self.head = self.data_length - 1 + offset
		else:
			raise NotImplementedError(f"Whence of '{whence}' is not supported.")

		self.head = self._clamp_to_file_bounds(self.head)
		self.counter = self.head // self.block_size
		self.block_offset = self.head % self.block_size
		block_start = self.counter * self.block_size

		file_offset = self.data_offset + block_start
		if self.fh.tell() != file_offset:
			self.fh.seek(self.data_offset + block_start)
		return self.head

	def seekable(self) -> True:
		"""Return True if the stream supports random access."""
		return self.read_only

	def tell(self) -> int:
		"""Return the current stream position."""
		return self.head

	def truncate(self, size=None):
		"""Not supported."""
		raise io.UnsupportedOperation('truncate')

	def writable(self) -> bool:
		"""Return True if the stream supports writing."""
		return self.write_only

	def write(self, data: ReadableBuffer):
		"""Write the given data to the stream."""
		if not self.writable():
			raise io.UnsupportedOperation('This file is not open write mode.')
		if self.finalized:
			raise io.UnsupportedOperation('This file has already been finalized.')

		encrypted_data = self.encryptor.update(data)
		self._write(encrypted_data)

	def writelines(self, lines: Iterable[ReadableBuffer]):
		"""Write a list of lines to the stream. Line separators are not added, so it is usual for each of the lines
		provided to have a line separator at the end."""
		return NotImplemented

	def verify(self):
		"""Check the file signature matches the given identity key. Verify that file has not been modified since creation."""
		return NotImplemented

	#
	# Internal
	#

	def _clamp_to_file_bounds(self, position: int) -> int:
		"""Make sure our read and seek don't go outside the bounds of the data payload."""
		return min(max(0, position), self.data_length)

	def _create_header(self) -> ContainerFormat:
		"""Return a header object."""
		return NotImplemented

	def generate_key_material(self):
		"""Generate the required symmetric key material.
		The values should come from a strong random source like os.urandom()

		WARNING: This value MUST NOT be hardcoded.
		"""
		return NotImplemented

	def _read_file_header(self, fh: BinaryIO):
		"""Read the file header and return an object representation."""
		return NotImplemented

	@property
	def decryptor(self):
		"""Return a fresh decryptor."""
		return NotImplemented

	@property
	def encryptor(self):
		return NotImplemented

	@property
	def mac(self):
		return NotImplemented

	@property
	def signature_hash(self):
		return NotImplemented

	def _encrypted_symmetric_key(self) -> bytes:
		"""Return the symmetric key after it has been encrypted with the rsa_key.

		The encrypted_key will be written into the file. The private_key will need to be used to recover the contents.
		"""
		try:
			return encrypt(self.key, to_public_key(self.encryption_key_private))
		except ValueError:
			raise RuntimeError('Failed to encrypt the symmetric key. The RSA public key may not be long enough.')

	def _decrypt_symmetric_key(self) -> bytes:
		"""Return the symmetric key after it has been decrypted with the private_key.

		The symmetric will be used to decrypt the file contents.
		"""
		encrypted_key_material = self.header.key_material
		return decrypt(encrypted_key_material, self.encryption_key_private)
