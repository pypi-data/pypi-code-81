import os
import stat
from getpass import getpass
from pathlib import Path
from typing import Optional, TypeVar
import string
import secrets

# import cfjson

from cfcrypt import CryptFileBinaryIO, CryptFileTextIO
from cfcrypt.rsa.types import RSAPrivateKeySet, RSAPrivateKey
from cfcrypt.rsa.key_helpers import generate_private_key, generate_private_pem, pem_file_to_private_key, \
	private_key_to_pem, private_key_to_pem_file


PathLike = TypeVar("PathLike", str, bytes, os.PathLike)


class MetaKeyRing(type):
	"""Singleton for accessing the key ring."""

	_instances = {}

	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super(MetaKeyRing, cls).__call__(*args, **kwargs)
		return cls._instances[cls]

	def __init__(cls, *args, **kwargs):
		super(MetaKeyRing, cls).__init__(*args, **kwargs)


def confirm_password(msg: str, confirmation: bool = True) -> str:
	"""Get a password from the user, with confirmation.

	:type msg: Message to print before the prompts.
	:param confirmation: If True the user will be asked to confirm the password.

	:meta private:
	"""
	while True:
		print(msg)
		password = getpass('Password: ')
		if not confirmation:
			break
		password2 = getpass('Confirm Password: ')
		if password == password2:
			break
		print('Passwords were different. Try again.')
	return password


class KeyRingBase(object, metaclass=MetaKeyRing):
	"""KeyRing helps you keep track of your applications RSA keys in a secure way.

	:meta private:
	"""

	@classmethod
	def create_key_ring_interactive(cls):
		"""Create a new KeyRing.

		Note: Must be called from an interactive prompt to allow for password entry.
		"""
		if 'CRYPT_KEYRING' not in os.environ:
			raise RuntimeError('KeyRing path not set in environment variable CRYPT_KEYRING')

		kek_path = KeyRingBase.main_key_file()
		if kek_path.exists():
			raise RuntimeError('Cannot create a new key ring as one already exists here: {}'.format(kek_path))

		print('Creating new KeyRing')
		password = confirm_password(
			'Enter a new password.\n'
			'This will be used to unlock the KeyRingBase. Choose a strong password with a length of at least 16.')

		print('Creating new master key.')
		pem_data = generate_private_pem(4096, password)
		with kek_path.open('wb') as fh:
			fh.write(pem_data)
		os.chmod(kek_path, stat.S_IREAD)

		instance = cls(password=password)
		instance._dump()
		return instance

	@classmethod
	def create_key_ring(cls):
		"""Create a new KeyRing.

		Note: During the creation an access token will be displayed. This is the only time it can been seen.
		Make sure you get a copy of it to access the KeyRing in future.
		"""

		if 'CRYPT_KEYRING' not in os.environ:
			raise RuntimeError('KeyRing path not set in environment variable CRYPT_KEYRING')

		kek_path = KeyRingBase.main_key_file()
		if kek_path.exists():
			raise RuntimeError('Cannot create a new key ring as one already exists here: {}'.format(kek_path))

		print('Creating new KeyRing')
		password = password_generator(50)

		print('Creating new master key.')
		private_key = generate_private_key(4096)
		private_key_to_pem_file(kek_path, private_key, password)
		os.chmod(kek_path, stat.S_IREAD)

		print(
			f'KeyRing has been created in {KeyRingBase.directory()}\n'
			f'Your access token is:\n'
			f'{password}\n'
			f'The token goes into the environmental variable CRYPT_KEYRING_TOKEN\n'
			f'Keep a backup of the token in a safe place as KeyRing does not keep a copy of it.')

		instance = cls(password=password)
		instance._dump()
		return instance

	@classmethod
	def change_password_interactive(cls):
		"""Change the password or access token of the KeyRing.

		Note: Must be called from an interactive prompt to allow for password entry.
		"""
		kek_path = KeyRingBase.main_key_file()
		if not kek_path.exists():
			raise RuntimeError('Could not find the key: {}'.format(kek_path))

		current_password = getpass('Current Password: ')
		kek = pem_file_to_private_key(kek_path, current_password.encode())

		password = confirm_password(
			'Enter a new password.\n'
			'This will be used to unlock the KeyRingBase. Choose a strong password with a length of at least 16.')

		temp = kek_path.with_suffix('.temp')
		try:
			with temp.open('wb') as fh:
				fh.write(private_key_to_pem(kek, password))
		except Exception:
			temp.unlink(missing_ok=True)
			raise
		os.chmod(kek_path, stat.S_IREAD | stat.S_IWRITE)
		temp.replace(kek_path)
		os.chmod(kek_path, stat.S_IREAD)

		return cls(password)

	@staticmethod
	def directory() -> Path:
		"""Get the working directory of the KeyRing.

		:meta private:
		"""
		working_dir = Path(os.environ.get('CRYPT_KEYRING', '..'))
		working_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
		return working_dir

	@staticmethod
	def main_key_file() -> Path:
		"""The location of the KeyRing's main RSAPrivateKey. All data is secured with this key.

		:meta private:
		"""
		return KeyRingBase.directory() / 'main.pem'

	@property
	def main_key(self) -> RSAPrivateKey:
		"""The main encryption key used to encrypt all other keys.

		:meta private:
		"""
		if self._kek is None:
			self._kek = pem_file_to_private_key(self.main_key_file(), self.password)
		return self._kek

	def __init__(self, namespace=None, password=None):
		"""Instance of the KeyRingBase."""
		if password is None:
			password = os.environ['CRYPT_KEYRING_TOKEN']
		self.password = password

		self._active_namespace = namespace or 'default'

		self._kek = None
		self.cache_file = self.directory() / 'keyring.crpt'

		self.key_store = dict()
		self._load()

	def _load(self):
		"""Load the keyring data from disk."""
		if self.cache_file.exists():
			with CryptFileBinaryIO(self.cache_file, 'rb', self.main_key, self.main_key) as fh:
				blob = cfjson.load(fh)
				self.key_store = blob['key_store']

	def _dump(self):
		"""Write the keyring data to disk."""
		temp_file = self.cache_file.with_suffix('.temp')
		try:
			with CryptFileTextIO(temp_file, self.main_key, self.main_key, 'wb') as fh:
				cfjson.dump({'key_store': self.key_store}, fh)
			temp_file.replace(self.cache_file)
		finally:
			temp_file.unlink(missing_ok=True)


class KeyRing(KeyRingBase):
	"""KeyRing helps you keep track of your applications RSA keys in a secure way.

	KeyRing uses a key-value store, where the key is a string and the value is an RSA PrivateKey or PrivateKeySet.
	"""

	def __init__(self, namespace=None, password=None):
		super(KeyRingBase, self).__init__(namespace, password)

	@property
	def namespace(self) -> str:
		"""Return the active namespace."""
		return self._active_namespace

	def set_namespace(self, namespace: str):
		"""Set the active namespace so you don't have to do it per call. If the namespace didn't previously exist it will be created.

		:param namespace: The namespace to mak active.
		"""
		self._active_namespace = namespace

	def attach_key(self, key_name: str, key: RSAPrivateKey, namespace: Optional[str] = None) -> RSAPrivateKey:
		"""Attach an existing RSAPrivate key to the KeyRing.

		:param key_name: The name used to access the key.
		:param key: RSAPrivateKey object.
		:param namespace: Namespace in which the key will be saved.
		"""
		namespace = namespace or self.namespace
		if namespace not in self.key_store:
			self.key_store[namespace] = dict()
		if key_name not in self.key_store[namespace]:
			self.key_store[namespace][key_name] = list()

		self.key_store[namespace][key_name].insert(0, key)
		self._dump()
		return key

	def attach_key_file(
			self, key_name: str, pem_file: PathLike, password: Optional[str] = None,
			namespace: Optional[str] = None) -> RSAPrivateKey:
		"""Attach an existing RSAPrivate key (from disk) to the KeyRing.

		:param key_name: The name used to access the key.
		:param pem_file: Path of the existing PEM file on disk.
		:param password: Password for the PEM file if required.
		:param namespace: Namespace in which the key will be saved.
		"""
		return self.attach_key(key_name, pem_file_to_private_key(pem_file, password), namespace)

	def create_key(self, key_name: str, namespace: Optional[str] = None, key_size: int = 4096) -> RSAPrivateKey:
		"""Create a new key and attach it to the KeyRing.

		:param key_name: key_name: The name used to access the key.
		:param namespace: Namespace in which the key will be saved.
		:param key_size: How big the key should be in bits
		"""
		new_key = generate_private_key(key_size)
		return self.attach_key(key_name, new_key, namespace)

	def delete_key(self, key_name: str, namespace: str):
		"""Deletes the given key with out any further prompt or chance of undo.

		:param key_name: key_name: The name of the key to delete.
		:param namespace: Namespace in which the key is saved.

		WARNING: There are no recovery options. The key will be destroyed and all data encrypted with it will be
		permanently encrypted, effectively destroyed.
		"""
		namespace = namespace or self.namespace
		del self.key_store[namespace][key_name]
		self._dump()

	def roll_key(self, key_name: str, namespace: Optional[str] = None) -> RSAPrivateKey:
		"""Replace the existing key with a new one of the same strength. The old key will still be available in the
		key set for decrypting, but all future encrypting should be done with the new key.

		:param key_name: key_name: The name used to access the key.
		:param namespace: Namespace in which the key will be saved.
		"""
		existing_key = self.get_key(key_name, namespace)
		new_key = generate_private_key(existing_key.key_size)
		self.attach_key(key_name, new_key, namespace)
		return new_key

	def get_key(self, key_name: str, namespace: Optional[str] = None) -> RSAPrivateKey:
		"""Get the first key in the key set for the given key_name.

		:param key_name: key_name: The name used to access the key.
		:param namespace: Namespace in which the key will be saved.
		"""
		namespace = namespace or self.namespace
		return self.key_store[namespace][key_name][0]

	def get_keys(self, key_name: str, namespace: Optional[str] = None) -> RSAPrivateKeySet:
		"""Get the key set for the given key_name.

		:param key_name: key_name: The name used to access the key.
		:param namespace: Namespace in which the key will be saved.
		"""
		namespace = namespace or self.namespace
		return self.key_store[namespace][key_name]


def password_generator(length: int) -> str:
	"""Generate a new access token of the given length.

	:param length: The length of the generated access token.

	:meta private:
	"""
	symbols = r"""!#$%&*+-?@_~"""
	alphabet = string.ascii_letters + string.digits + symbols

	def is_symbol(c):
		return c in symbols

	while True:
		password = ''.join(secrets.choice(alphabet) for _ in range(length))
		if (
				any(c.islower() for c in password)
				and any(c.isupper() for c in password)
				and sum(c.isdigit() for c in password) >= 3
				and sum(is_symbol(c) for c in password) >= 3):
			break
	return password


if __name__ == '__main__':
	# os.environ['']

	# KeyRingBase.create()
	# KeyRingBase.change_main_password()
	# ring = KeyRing(namespace='bank')
	# ring.attach_key_file('encryption_key', Path('c:/source/bank/config/active.pem'))
	# print(ring.get_keys('encryption_key'))

	# print(password_gen(50))

	# keyring = KeyRing(namespace='bank')
	#
	# keyring.key_store['bank']['cache'] = keyring.key_store['bank']['encryption_key']
	# # keyring.key_store['bank']['config'] = keyring.key_store['bank']['encryption_key']
	# keyring.key_store['bank']['crypt_file'] = keyring.key_store['bank']['encryption_key']
	# keyring.key_store['bank']['identity'] = keyring.key_store['bank']['encryption_key']
	#
	# keyring.roll_key('cache')
	# keyring.roll_key('crypt_file')
	# keyring.roll_key('identity')

	# keyring.create_key('cache')
	# keyring.create_key('config')
	# keyring.create_key('crypt_file')
	# keyring.create_key('identity')
	pass
