import os
import struct
from collections import OrderedDict
from typing import BinaryIO

from .constants import MAC_NONE, PathLike
from .exceptions import FileParserError


def is_crypt_file(filename: PathLike) -> bool:
	"""True if the file looks like a crpt file."""
	with open(filename, 'rb') as fh:
		return fh.read(4) == ContainerFormat.magic_bytes


class ContainerFormat(object):
	"""Header for a binary container file format for storing data encrypted."""

	magic_bytes = b'CRYP'  #: Magic byte values

	file_type = (
		('magic_bytes', '4s'),  # 4 Char
		('format_version', 'B'),  # uchar
	)  #: File type fields and data types
	file_type_format = '<' + ''.join(b for _, b in file_type)  #: File type struct definition

	@staticmethod
	def create(*args, **kwargs) -> "ContainerFormat":
		"""Construct a ContainerFormat object for a new file."""
		versions = ContainerFormat.get_supported_versions()
		klass = versions[max(versions.keys())]
		return klass(*args, **kwargs)

	@staticmethod
	def create_from_file(fh: BinaryIO) -> "ContainerFormat":
		"""Create ContainerFormat object from an existing file."""
		fh.seek(0)
		klass = ContainerFormat.get_version_class(fh)

		size = struct.calcsize(klass.format)
		header_bytes = fh.read(size)[:size]

		if len(header_bytes) != size:
			raise RuntimeError('Failed to read the whole header.')

		# Unpack the header
		fields = struct.unpack(klass.format, header_bytes)
		header = klass(*fields, file_handle=fh)
		return header

	@classmethod
	def get_version_class(cls, fh: BinaryIO) -> 'ContainerFormat':
		"""Returns the child class that is registered to handle the version number from the file.

		:raises
			FileParserError: There is an error parsing and encrypted file.

		:meta private:
		"""
		size = struct.calcsize(cls.file_type_format)
		check_bytes = fh.read(size)[:size]
		magic_bytes, format_version = struct.unpack(cls.file_type_format, check_bytes)
		if magic_bytes != cls.magic_bytes:
			raise FileParserError('Bad magic number')

		versions = cls.get_supported_versions()
		if format_version not in versions:
			raise FileParserError(
				'Unknown version number. The file could be corrupt, or created by a newer version of '
				'this software.')

		return versions[format_version]

	@classmethod
	def get_supported_versions(cls):
		"""Queries all the sub-classes for the format versions they represent.

		:meta private:
		"""
		return {subclass.format_version: subclass for subclass in cls.__subclasses__()}

	def __init__(self):
		# The rest are offset/length pairs to allow for variable length.
		self.file_size = None

	def __getattr__(self, item):
		if item in self.fields:
			return self.fields[item]

	def __getitem__(self, item):
		return self.fields[item]

	def __bytes__(self):
		return struct.pack(ContainerFormat.file_type_format, self.magic_bytes, self.format_version)

	def __len__(self):
		return struct.calcsize(ContainerFormat.file_type_format)

	def length(self):
		"""The length in bytes when serialized into a struct."""
		return struct.calcsize(ContainerFormat.file_type_format)

	def to_bytes(self):
		"""Serialize into a struct."""
		return bytes(self)

	def load_variable_size_fields(self, fh):
		"""Parse the file and unpack any know variable length data described in the header.

		:meta private:
		"""
		return NotImplemented

	def set_file_size(self, file_size):
		"""Set the size of the file on disk.

		This is used to calculate some missing lengths and offsets for the data payload and signature.
		"""
		self.file_size = file_size

	@property
	def data_length(self):
		"""The length of the data payload in bytes.

		This is usually only available after the file size is set.

		:meta private:
		"""
		return NotImplemented


class ContainerFormatV1(ContainerFormat):
	labels = (
		('algorithm', 'B'),  # uchar
		('algorithm_mode', 'B'),  # uchar
		('algorithm_pad', 'B'),  # uchar
		('algorithm_mac', 'B'),  # uchar
		('algorithm_mac_hash', 'B'),  # uchar
		('chunk_size', 'i'),  # int

		('nonce_offset', 'I'),  # uint
		('nonce_length', 'I'),  # uint
		('key_offset', 'I'),  # uint
		('key_length', 'I'),  # uint

		('data_offset', 'I'),  # uint

		('mac_length', 'h'),  # short int
	)  #: Fields and data types

	format = '<' + ''.join(b for a, b in labels)  #: Struct definition

	format_version = 1  #: Registered version number

	def __init__(self, *args, file_handle=None, **kwargs):
		super(ContainerFormatV1, self).__init__()
		# Fields are packed into the header
		self.fields = OrderedDict(zip([a for a, b in self.labels], args))

		self.nonce = None
		self.key_material = None
		self.mac = None

		for field, value in kwargs.items():
			self.fields[field] = value

		if file_handle:
			self.load_variable_size_fields(file_handle)

	def __bytes__(self):
		self.update_offsets()
		field_values = [self.fields[label] for label, _ in self.labels]
		return super(ContainerFormatV1, self).__bytes__() + struct.pack(self.format, *field_values)

	def __len__(self):
		return super(ContainerFormatV1, self).__len__() + struct.calcsize(self.format)

	def length(self):
		return len(self)

	def load_variable_size_fields(self, fh):
		# Use the header info to get the nonce
		fh.seek(self.nonce_offset)
		self.set_nonce(fh.read(self.nonce_length))

		# Use the self info to get the encrypted key material
		fh.seek(self.key_offset)
		self.set_key_material(fh.read(self.key_length))

		# Use the self info to get the mac
		if self.mac_length != MAC_NONE:
			fh.seek(self.mac_end_offset, os.SEEK_END)
			self.set_mac(fh.read(self.mac_length))

	def update_offsets(self):
		head = self.length()
		self.fields['nonce_offset'] = head
		head += self.fields['nonce_length']

		self.fields['key_offset'] = head
		head += self.fields['key_length']

		self.fields['data_offset'] = head

	def set_nonce(self, nonce):
		self.nonce = nonce
		self.fields['nonce_length'] = len(nonce)

	def set_key_material(self, key_material):
		self.key_material = key_material
		self.fields['key_length'] = len(key_material)

	def set_mac(self, code):
		self.mac = code
		self.fields['mac_length'] = len(code)

	def set_mac_length(self, mac_length):
		self.fields['mac_length'] = mac_length

	@property
	def mac_offset(self):
		return self.file_size + self.mac_end_offset

	@property
	def mac_end_offset(self):
		# Relative to the end of file so we don't need to know the data length to recover it.
		return -self.mac_length

	@property
	def data_length(self):
		# Calculate this dynamically so we don't need to know it before we start writing the header.
		return self.file_size - self.mac_length - self.data_offset
