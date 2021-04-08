import array
import mmap
import os
from typing import TypeVar

ALGO_AES = 1  #: AES algorithm
ALGO_MODE_CBC = 1  #: Algorithm mode Cipher Block Chaining  # Not implemented
ALGO_MODE_CTR = 2  #: Algorithm mode Counter
PAD_NONE = 0  #: Padding algorithm None
PAD_PKCS7 = 1  #: Padding algorithm PKCS#7  # Not implemented
HASH_SHA256 = 1  #: Hashing algorithm SHA256
MAC_NONE = 0  #: Message authentication code None
MAC_HMAC = 1  #: Message authentication code HMAC
MAC_RSA_SIGNED = 2  #: Message authentication code RSA signature
constant_names = {
	'algorithm': {
		ALGO_AES: 'AES',
	},
	'algorithm_mode': {
		ALGO_MODE_CBC: 'CBC',
		ALGO_MODE_CTR: 'CTR',
	},
	'algorithm_pad': {
		PAD_NONE: 'None',
		PAD_PKCS7: 'PKCS7',
	},
	'algorithm_mac': {
		MAC_NONE: 'None',
		MAC_HMAC: 'HMAC',
		MAC_RSA_SIGNED: 'RSA signed',
	},
	'algorithm_mac_hash': {
		HASH_SHA256: 'SHA256',
	},
}


def parameter_to_name(parameter, parameter_value):
	return constant_names[parameter].get(parameter_value, parameter_value)


PathLike = TypeVar("PathLike", str, bytes, os.PathLike)
ReadableBuffer = TypeVar("ReadableBuffer", bytes, bytearray, memoryview, array.array, mmap.mmap)
WriteableBuffer = TypeVar("WriteableBuffer", bytes, bytearray, memoryview, array.array, mmap.mmap)

SIZE_8MiB = 1024 * 1024 * 8
