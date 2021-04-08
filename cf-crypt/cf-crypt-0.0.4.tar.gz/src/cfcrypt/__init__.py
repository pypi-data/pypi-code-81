from cfcrypt.crypt_file import CryptFileBinaryIO, CryptFileTextIO
from cfcrypt.file_format import is_crypt_file

import cfcrypt.file_utils

from cfcrypt.exceptions import CryptException, FileParserError
from cfcrypt.rsa.exceptions import RSAException, EncryptionFailed, DecryptionFailed, InvalidSignature


KEY_SERIALIZATION_ENABLED = True
try:
	from cfjson.cfjson import JsonTypeRegister
except ImportError:
	KEY_SERIALIZATION_ENABLED = False


__all__ = (
	'is_crypt_file', 'CryptFileBinaryIO', 'CryptFileTextIO',
	'CryptException', 'RSAException', 'EncryptionFailed', 'DecryptionFailed', 'InvalidSignature')

__version__ = '0.0.4'


def register_serde():
	"""Registers with cf-json serialization."""
	def rsa_private_key_decode(dct):
		"""Decode json dict into class objects."""
		from cfcrypt.rsa.key_helpers import pem_to_private_key
		cls_name = dct['__json_type__']
		if cls_name in ('_RSAPrivateKey',):
			return pem_to_private_key(dct['private_key'].encode())
		raise TypeError()

	def rsa_private_key_encode(obj):
		"""Encode the object into a json safe dict."""
		from cfcrypt.rsa.key_helpers import private_key_to_pem
		return {
			'__json_type__': type(obj).__name__,
			'private_key': private_key_to_pem(obj).decode('utf-8')
		}

	JsonTypeRegister.register('_RSAPrivateKey', rsa_private_key_encode, rsa_private_key_decode)


if KEY_SERIALIZATION_ENABLED:
	register_serde()
