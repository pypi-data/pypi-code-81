import sys

try:
	from cfcrypt.exceptions import CryptException
except ImportError:
	CryptException = RuntimeError


ENABLE_STACK_TRACE = False


class RSAException(CryptException):
	pass


class CryptExceptionNoStack(RSAException):
	"""The exception handler is hooked to not show the stack trace for these exceptions."""
	pass


class EncryptionFailed(CryptExceptionNoStack):
	pass


class DecryptionFailed(CryptExceptionNoStack):
	pass


class InvalidSignature(CryptExceptionNoStack):
	pass


current_handler = sys.excepthook


def exception_handler(exception_type, exception, traceback):
	if not ENABLE_STACK_TRACE and issubclass(exception_type, CryptExceptionNoStack):
		print("%s: %s" % (exception_type.__name__, exception), file=sys.stderr)
		sys.exit(1)
	return current_handler(exception_type, exception, traceback)


# noinspection SpellCheckingInspection
sys.excepthook = exception_handler
