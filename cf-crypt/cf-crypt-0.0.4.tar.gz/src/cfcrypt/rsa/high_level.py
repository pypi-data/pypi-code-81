import base64
import binascii
import json

import typing

from .types import RSAKeySet
from .low_level import encrypt, decrypt


# TODO: Think about adding signing to these helpers, or switching up encryption modes to something with verification.


def encrypt_string(message: str, rsa_key: RSAKeySet) -> str:
	"""Encrypt the given string."""
	# Encode it down to ASCII
	message = message.encode()

	# Encrypt the message
	encrypted_message = encrypt(message, rsa_key)

	# Wrap binary in base64
	encrypted_message = base64.b64encode(encrypted_message)

	# Convert the bytes back into a python str
	encrypted_message = encrypted_message.decode('utf-8')

	return encrypted_message


def decrypt_string(encrypted_message: str, private_keys: RSAKeySet) -> str:
	"""Decrypt the given string."""
	# Encode it down to ASCII
	encrypted_message = encrypted_message.encode()

	# Strip base64, back to binary
	encrypted_message = base64.b64decode(encrypted_message)

	# Decrypt the message
	message = decrypt(encrypted_message, private_keys).decode()

	return message


def encrypt_object(message: typing.Any, rsa_key: RSAKeySet) -> str:
	"""Encrypt an python object. Must be json serializable."""
	# Wrap it in JSON
	message = json.dumps(message)

	# Encode it down to ASCII
	message = message.encode()

	# Encrypt the message
	encrypted_message = encrypt(message, rsa_key)

	# Wrap binary in base64
	encrypted_message = base64.b64encode(encrypted_message)

	# Convert the bytes back into a python str
	encrypted_message = encrypted_message.decode('utf-8')

	return encrypted_message


def decrypt_object(encrypted_message: str, private_keys: RSAKeySet, ignore_failure: bool = False) -> typing.Any:
	"""Decrypt the message back into python objects."""
	# Encode it down to ASCII
	encrypted_message = encrypted_message.encode()

	# Strip base64, back to binary
	try:
		encrypted_message = base64.b64decode(encrypted_message)
	except binascii.Error:
		if ignore_failure:
			return encrypted_message.decode('utf-8')
		raise

	# Decrypt the message
	message = decrypt(encrypted_message, private_keys).decode()

	# Unwrap the JSON
	message = json.loads(message)

	return message
