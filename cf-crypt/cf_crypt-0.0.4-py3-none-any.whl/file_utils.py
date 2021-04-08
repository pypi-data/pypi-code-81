import shutil
from pathlib import Path
from typing import Iterable

from . import is_crypt_file, CryptFileBinaryIO
from .constants import PathLike, SIZE_8MiB
from cfcrypt.rsa.types import RSAPrivateKeySet


def encrypt_folder(
		folder_path: PathLike, encryption_key: RSAPrivateKeySet, identity_key: RSAPrivateKeySet,
		buffer_size: int = SIZE_8MiB, recursive: bool = False):
	"""
	Encrypt all files in the given folder.

	:param folder_path: Folder to search for files in.
	:param encryption_key: The encryption key to use.
	:param identity_key: The identity key to use.
	:param buffer_size: Control how much of the file is read into memory each loop.
	:param recursive: If True check sub-folders for files as well.
	"""
	folder_path = Path(folder_path)

	if recursive:
		filepaths = folder_path.glob('**/*')
	else:
		filepaths = folder_path.glob('*')

	filepaths = [f for f in filepaths if f.is_file()]
	encrypt_files(filepaths, encryption_key, identity_key, buffer_size)


def encrypt_files(
		filepaths: Iterable[PathLike], encryption_key: RSAPrivateKeySet, identity_key: RSAPrivateKeySet,
		buffer_size: int = SIZE_8MiB):
	"""
	Encrypt a list of files in place.

	:param filepaths: Files to encrypt.
	:param encryption_key: The encryption key to use.
	:param identity_key: The identity key to use.
	:param buffer_size: Control how much of the file is read into memory each loop.
	"""
	for filepath in filepaths:
		if is_crypt_file(filepath):
			continue
		encrypt_file(filepath, encryption_key, identity_key, buffer_size)


def encrypt_file(
		filepath: PathLike, encryption_key: RSAPrivateKeySet, identity_key: RSAPrivateKeySet, buffer_size: int = SIZE_8MiB):
	"""
	Encrypt a single file in place.

	:param filepath: File to encrypt.
	:param encryption_key: The encryption key to use.
	:param identity_key: The identity key to use.
	:param buffer_size: Control how much of the file is read into memory each loop.
	"""
	filepath = Path(filepath)
	if is_crypt_file(filepath):
		raise RuntimeError('File is already encrypted.')

	output_filepath = filepath.with_suffix('.encrypting')
	try:
		with filepath.open('rb') as input_fh, \
				CryptFileBinaryIO(output_filepath, 'wb', encryption_key, identity_key) as output_fh:
			while True:
				chunk = input_fh.read(buffer_size)
				if len(chunk) == 0:
					break
				output_fh.write(chunk)
		output_filepath.replace(filepath)

	finally:
		output_filepath.unlink(missing_ok=True)


def decrypt_folder(
		folder_path: PathLike, encryption_key: RSAPrivateKeySet, identity_key: RSAPrivateKeySet,
		buffer_size: int = SIZE_8MiB, recursive: bool = False):
	"""
	Decrypt all files in the given folder.

	:param folder_path: Folder to search for files in.
	:param encryption_key: The encryption key to use.
	:param identity_key: The identity key to use.
	:param buffer_size: Control how much of the file is read into memory each loop.
	:param recursive: If True check sub-folders for files as well.
	"""
	folder_path = Path(folder_path)

	if recursive:
		filepaths = folder_path.glob('**/*')
	else:
		filepaths = folder_path.glob('*')

	filepaths = [f for f in filepaths if f.is_file()]
	decrypt_files(filepaths, encryption_key, identity_key, buffer_size)


def decrypt_files(
		filepaths: Iterable[PathLike], encryption_key: RSAPrivateKeySet, identity_key: RSAPrivateKeySet,
		buffer_size: int = SIZE_8MiB):
	"""
	Decrypt a list of files in place.

	:param folder_path: Files to encrypt.
	:param encryption_key: The encryption key to use.
	:param identity_key: The identity key to use.
	:param buffer_size: Control how much of the file is read into memory each loop.
	"""
	for filepath in filepaths:
		if not is_crypt_file(filepath):
			continue
		decrypt_file(filepath, encryption_key, identity_key, buffer_size)


def decrypt_file(
		filepath: PathLike, encryption_key: RSAPrivateKeySet, identity_key: RSAPrivateKeySet, buffer_size: int = SIZE_8MiB):
	"""
	Decrypt a single file in place.

	:param filepath: File to encrypt.
	:param encryption_key: The encryption key to use.
	:param identity_key: The identity key to use.
	:param buffer_size: Control how much of the file is read into memory each loop.
	"""
	filepath = Path(filepath)
	if not is_crypt_file(filepath):
		raise RuntimeError('File is not encrypted.')

	output_filepath = filepath.with_suffix('.decrypting')
	try:
		with CryptFileBinaryIO(filepath, 'rb', encryption_key, identity_key) as input_fh, \
			output_filepath.open('wb') as output_fh:
			while True:
				chunk = input_fh.read(buffer_size)
				if len(chunk) == 0:
					break
				output_fh.write(chunk)
		output_filepath.replace(filepath)

	finally:
		output_filepath.unlink(missing_ok=True)


def secure_file_move(
		source_file: PathLike, target_file: PathLike, encryption_key: RSAPrivateKeySet, identity_key: RSAPrivateKeySet,
		buffer_size: int = SIZE_8MiB):
	"""Move the source to the target and encrypt it."""
	source_file = Path(source_file)
	if is_crypt_file(source_file):
		shutil.move(source_file, target_file)
		return

	try:
		with source_file.open('rb') as input_fh, \
				CryptFileBinaryIO(target_file, 'wb', encryption_key, identity_key) as output_fh:

			while True:
				chunk = input_fh.read(buffer_size)
				if len(chunk) == 0:
					break
				output_fh.write(chunk)

	except Exception:
		target_file.unlink(missing_ok=True)
		raise


def encrypt_data():
	from crypt.key_ring import KeyRing
	ring = KeyRing('bank')
	encryption_key = ring.get_keys('crypt_file')
	identity_key = ring.get_keys('identity')
	encrypt_folder(Path('c:/source/bank/data'), encryption_key, identity_key, True)


def merge():
	from crypt.key_ring import KeyRing
	ring = KeyRing('bank')
	encryption_key = ring.get_keys('crypt_file')
	identity_key = ring.get_keys('identity')
	# decrypt_file(Path('c:/source/bank/scratch/merge.csv'), encryption_key, identity_key)
	# encrypt_file(Path('c:/source/bank/scratch/merge.csv'), encryption_key, identity_key)


if __name__ == '__main__':
	merge()
