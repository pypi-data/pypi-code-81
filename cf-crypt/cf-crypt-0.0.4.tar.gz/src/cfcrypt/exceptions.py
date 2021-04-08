class CryptException(Exception):
	"""Base class for all exceptions in the module."""
	pass


class FileParserError(CryptException):
	"""Used when there is an error parsing and encrypted file."""
	pass
