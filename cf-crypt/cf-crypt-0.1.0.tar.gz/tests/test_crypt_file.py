import struct
from pathlib import Path
from unittest import TestCase
import random

from cfcrypt.crypt_file import CryptFileBinaryIO
from cfcrypt.constants import ALGO_MODE_CBC
from cfcrypt.rsa import generate_keypair
from cfcrypt.rsa.exceptions import DecryptionFailed, InvalidSignature


def unlink(path_test_file):
	# The missing_ok flag didn't come in until python 3.8
	if path_test_file.exists():
		path_test_file.unlink()


def random_data(n=1024 ** 2):
	# random.randbytes(n)  # 3.9 feature
	return bytearray(random.getrandbits(8) for _ in range(n))


class TestCryptFileBinaryIO(TestCase):

	@classmethod
	def setUpClass(cls):
		cls.private_key, cls.public_key = generate_keypair()
		cls.filename = Path('./test.kenc')

	def tearDown(self):
		unlink(self.filename)

	def test_round_trip(self):
		test = random_data(1024)

		with CryptFileBinaryIO(self.filename, 'wb', self.private_key, self.private_key) as fh:
			fh.write(test)

		with CryptFileBinaryIO(self.filename, 'rb', self.private_key, self.private_key) as fh:
			round_trip_test = fh.read()

		self.assertEqual(test, round_trip_test)

	def test_big_round_trip(self):
		test = random_data(8 * 1024 ** 2)

		with CryptFileBinaryIO(self.filename, 'wb', self.private_key, self.private_key) as fh:
			fh.write(test)

		with CryptFileBinaryIO(self.filename, 'rb', self.private_key, self.private_key) as fh:
			round_trip_test = fh.read()

		self.assertEqual(test, round_trip_test)

	def test_partial_read(self):
		test = random_data(1024)

		with CryptFileBinaryIO(self.filename, 'wb', self.private_key, self.private_key) as fh:
			fh.write(test)

		with CryptFileBinaryIO(self.filename, 'rb', self.private_key, self.private_key) as fh:
			round_trip_test = fh.read(16)

			self.assertEqual(test[:16], round_trip_test)

	def test_sequential_partial_read(self):
		test = random_data(1024)

		with CryptFileBinaryIO(self.filename, 'wb', self.private_key, self.private_key) as fh:
			fh.write(test)

		with CryptFileBinaryIO(self.filename, 'rb', self.private_key, self.private_key) as fh:
			round_trip_test = fh.read(16)

			self.assertEqual(test[:16], round_trip_test)
			round_trip_test = fh.read(16)
			self.assertEqual(test[16:32], round_trip_test)

	def test_seek_read(self):
		test = random_data(1024)

		with CryptFileBinaryIO(self.filename, 'wb', self.private_key, self.private_key) as fh:
			fh.write(test)

		with CryptFileBinaryIO(self.filename, 'rb', self.private_key, self.private_key) as fh:
			fh.seek(512)
			round_trip_test = fh.read(16)
			self.assertEqual(test[512:512 + 16], round_trip_test)

	def test_reopen_round_trip(self):
		test = random_data(1024)

		with CryptFileBinaryIO(self.filename, 'wb', self.private_key, self.private_key) as fh:
			fh.write(test)

		with CryptFileBinaryIO(self.filename, 'rb', self.private_key, self.private_key) as fh:
			round_trip_test = fh.read()
			self.assertEqual(test, round_trip_test)

		with CryptFileBinaryIO(self.filename, 'rb', self.private_key, self.private_key) as fh:
			round_trip_test = fh.read()
			self.assertEqual(test, round_trip_test)

	def test_wrong_key(self):
		test = random_data(1024)

		bad_private_key, bad_public_key = generate_keypair()

		with CryptFileBinaryIO(self.filename, 'wb', self.private_key, self.private_key) as fh:
			fh.write(test)

		self.assertRaises(DecryptionFailed, CryptFileBinaryIO, self.filename, 'rb', bad_private_key, bad_private_key)

	def test_tamping_with_parameter(self):
		test = random_data(1024)

		with CryptFileBinaryIO(self.filename, 'wb', self.private_key, self.private_key) as fh:
			fh.write(test)

		# Change a field in the header
		with open(self.filename, 'rb+') as fh:
			fh.seek(6)
			fh.write(struct.pack('<B', ALGO_MODE_CBC))

		self.assertRaises(RuntimeError, CryptFileBinaryIO, self.filename, 'rb', self.private_key, self.private_key)

	def test_tamping_with_data(self):
		test = random_data(1024)

		with CryptFileBinaryIO(self.filename, 'wb', self.private_key, self.private_key) as fh:
			fh.write(test)

		# Change a field in the header
		with open(self.filename, 'rb+') as fh:
			fh.seek(512)
			fh.write(struct.pack('<B', 9))

		self.assertRaises(InvalidSignature, CryptFileBinaryIO, self.filename, 'rb', self.private_key, self.private_key)

	def test_round_trip_multi_key(self):
		test = random_data(1024)
		new_private_key, new_public_key = generate_keypair()
		keys = new_private_key, self.private_key

		with CryptFileBinaryIO(self.filename, 'wb', keys, keys) as fh:
			fh.write(test)

		with CryptFileBinaryIO(self.filename, 'rb', keys, keys) as fh:
			round_trip_test = fh.read()

		self.assertEqual(test, round_trip_test)

	def test_round_trip_new_key(self):
		test = random_data(1024)
		new_private_key, new_public_key = generate_keypair()
		keys = new_private_key, self.private_key

		with CryptFileBinaryIO(self.filename, 'wb', self.private_key, self.private_key) as fh:
			fh.write(test)

		with CryptFileBinaryIO(self.filename, 'rb', keys, keys) as fh:
			round_trip_test = fh.read()

		self.assertEqual(test, round_trip_test)
