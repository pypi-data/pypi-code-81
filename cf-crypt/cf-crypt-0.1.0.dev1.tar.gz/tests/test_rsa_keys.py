import random
import string
from pathlib import Path
from unittest import TestCase

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey

from cfcrypt.rsa.key_helpers import generate_private_key, generate_private_pem, generate_keypair, pem_to_private_key, \
	pem_to_keypair, pem_file_to_keypair, private_key_to_pem, private_key_to_pem_file, pem_file_to_private_key


def unlink(path_test_file):
	# The missing_ok flag didn't come in until python 3.8
	if path_test_file.exists():
		path_test_file.unlink()


class Test(TestCase):

	def test_generate_private_key(self):
		result = generate_private_key()
		self.assertIsInstance(result, RSAPrivateKey)

	def test_generate_private_key_size(self):
		size = 2048
		result = generate_private_key(size)
		self.assertIsInstance(result, RSAPrivateKey)
		self.assertEqual(result.key_size, size)

		size = 4096
		result = generate_private_key(size)
		self.assertIsInstance(result, RSAPrivateKey)
		self.assertEqual(result.key_size, size)

		size = 0
		self.assertRaises(ValueError, generate_private_key, size)

	def test_generate_private_pem(self):
		pem = generate_private_pem()
		self.assertIsInstance(pem, bytes)

		pem = generate_private_pem(4096)
		self.assertIsInstance(pem, bytes)

	def test_generate_keypair(self):
		private_key, public_key = generate_keypair()
		self.assertIsInstance(private_key, RSAPrivateKey)
		self.assertIsInstance(public_key, RSAPublicKey)

	def test_pem_to_private_key(self):
		password = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=12))

		pem = generate_private_pem()
		self.assertIsInstance(pem, bytes)
		private_key = pem_to_private_key(pem)
		self.assertIsInstance(private_key, RSAPrivateKey)

		pem = generate_private_pem(2048, password)
		self.assertIsInstance(pem, bytes)
		private_key = pem_to_private_key(pem, password)
		self.assertIsInstance(private_key, RSAPrivateKey)

		pem = generate_private_pem(2048, password)
		self.assertIsInstance(pem, bytes)
		self.assertRaises(ValueError, pem_to_private_key, pem, 'wrong_password')

		pem = generate_private_pem(2048, password)
		self.assertIsInstance(pem, bytes)
		self.assertRaises(TypeError, pem_to_private_key, pem)

	def test_pem_to_keypair(self):
		pem = generate_private_pem()
		self.assertIsInstance(pem, bytes)

		private_key, public_key = pem_to_keypair(pem)
		self.assertIsInstance(private_key, RSAPrivateKey)
		self.assertIsInstance(public_key, RSAPublicKey)

	def test_pem_file_to_keypair(self):
		pem_file = Path('./test.pem')
		password = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=12))

		pem = generate_private_pem()
		self.assertIsInstance(pem, bytes)
		try:
			with pem_file.open('wb') as fh:
				fh.write(pem)

			private_key, public_key = pem_file_to_keypair(pem_file)
			self.assertIsInstance(private_key, RSAPrivateKey)
			self.assertIsInstance(public_key, RSAPublicKey)

		finally:
			unlink(pem_file)

		pem = generate_private_pem(2048, password)
		self.assertIsInstance(pem, bytes)
		try:
			with pem_file.open('wb') as fh:
				fh.write(pem)

			private_key, public_key = pem_file_to_keypair(pem_file, password)
			self.assertIsInstance(private_key, RSAPrivateKey)
			self.assertIsInstance(public_key, RSAPublicKey)

		finally:
			unlink(pem_file)

		pem = generate_private_pem(2048, password)
		self.assertIsInstance(pem, bytes)
		try:
			with pem_file.open('wb') as fh:
				fh.write(pem)

			self.assertRaises(ValueError, pem_file_to_keypair, pem_file, 'bad_password')

		finally:
			unlink(pem_file)

		pem = generate_private_pem(2048, password)
		self.assertIsInstance(pem, bytes)
		try:
			with pem_file.open('wb') as fh:
				fh.write(pem)

			self.assertRaises(TypeError, pem_file_to_keypair, pem_file)

		finally:
			unlink(pem_file)

	def test_private_key_to_pem(self):
		size = 2048
		password = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=12))

		private_key = generate_private_key(size)
		self.assertIsInstance(private_key, RSAPrivateKey)

		pem = private_key_to_pem(private_key)
		self.assertIsInstance(pem, bytes)
		private_key = pem_to_private_key(pem)
		self.assertIsInstance(private_key, RSAPrivateKey)

		pem = private_key_to_pem(private_key, password)
		self.assertIsInstance(pem, bytes)
		private_key = pem_to_private_key(pem, password)
		self.assertIsInstance(private_key, RSAPrivateKey)
		self.assertRaises(ValueError, pem_to_private_key, pem, 'bad_password')

		pem = private_key_to_pem(private_key, password)
		self.assertIsInstance(pem, bytes)
		private_key = pem_to_private_key(pem, password)
		self.assertIsInstance(private_key, RSAPrivateKey)
		self.assertRaises(TypeError, pem_to_private_key, pem)

	def test_private_key_to_pem_file(self):
		pem_file = Path('./test.pem')
		password = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=12))

		private_key = generate_private_key()
		self.assertIsInstance(private_key, RSAPrivateKey)
		try:
			output_path = private_key_to_pem_file(pem_file, private_key)
			self.assertIsInstance(output_path, Path)
			self.assertTrue(output_path.exists())

			loaded_private_key = pem_file_to_private_key(output_path)
			self.assertIsInstance(loaded_private_key, RSAPrivateKey)
			self.assertEqual(private_key_to_pem(private_key), private_key_to_pem(loaded_private_key))

		finally:
			unlink(pem_file)

		private_key = generate_private_key()
		self.assertIsInstance(private_key, RSAPrivateKey)
		try:
			output_path = private_key_to_pem_file(str(pem_file.resolve()), private_key)
			self.assertIsInstance(output_path, Path)
			self.assertTrue(output_path.exists())

			loaded_private_key = pem_file_to_private_key(output_path)
			self.assertIsInstance(loaded_private_key, RSAPrivateKey)
			self.assertEqual(private_key_to_pem(private_key), private_key_to_pem(loaded_private_key))

		finally:
			unlink(pem_file)

		private_key = generate_private_key()
		self.assertIsInstance(private_key, RSAPrivateKey)
		try:
			output_path = private_key_to_pem_file(str(pem_file.resolve()), private_key, password)
			self.assertIsInstance(output_path, Path)
			self.assertTrue(output_path.exists())

			loaded_private_key = pem_file_to_private_key(output_path, password)
			self.assertIsInstance(loaded_private_key, RSAPrivateKey)
			self.assertEqual(private_key_to_pem(private_key), private_key_to_pem(loaded_private_key))

		finally:
			unlink(pem_file)

		private_key = generate_private_key()
		self.assertIsInstance(private_key, RSAPrivateKey)
		try:
			output_path = private_key_to_pem_file(str(pem_file.resolve()), private_key, password)
			self.assertIsInstance(output_path, Path)
			self.assertTrue(output_path.exists())

			self.assertRaises(ValueError, pem_file_to_private_key, output_path, 'bad_password')

		finally:
			unlink(pem_file)

		private_key = generate_private_key()
		self.assertIsInstance(private_key, RSAPrivateKey)
		try:
			output_path = private_key_to_pem_file(str(pem_file.resolve()), private_key, password)
			self.assertIsInstance(output_path, Path)
			self.assertTrue(output_path.exists())

			self.assertRaises(TypeError, pem_file_to_private_key, output_path)

		finally:
			unlink(pem_file)

