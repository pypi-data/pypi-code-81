import itertools
from unittest import TestCase
from pathlib import Path

import sys
sys.path.append('./src/')
from cfjson.serde.pathlib_serde import path_decode, path_encode


def test_paths():
	return (
		Path('/'),
		Path('/folder'),
		Path('/folder/'),
		Path('/folder/file.txt'),
		Path('c:/'),
		Path('c:/folder'),
		Path('c:/folder/'),
		Path('c:/folder/file.txt'),
		Path('.'),
		Path('./'),
		Path('./folder'),
		Path('./folder/'),
		Path('./folder/file.txt'),
		Path('..'),
		Path('../'),
		Path('../folder'),
		Path('../folder/'),
		Path('../folder/file.txt'),
	)


native_path_type = Path('.').resolve().__class__.__name__


class Test(TestCase):

	def test_path_decode(self):
		for n in test_paths():
			blob = {
				'__json_type__': native_path_type,
				'path': n
			}
			result = path_decode(blob)
			self.assertEqual(result, Path(n), msg='Failed on {}'.format(n))

	def test_path_encode(self):
		for n in test_paths():
			blob = {
				'__json_type__': native_path_type,
				'path': str(Path(n))
			}
			result = path_encode(Path(n))
			self.assertEqual(result, blob, msg='Failed on {}'.format(n))

	def test_round_trip(self):
		for n in test_paths():
			in_number = Path(n)
			out_number = path_decode(path_encode(in_number))

			self.assertEqual(in_number, out_number, msg='Failed on {}'.format(n))

	def test_path_decode_bad_type(self):
		blob = {
			'__json_type__': 'BadType',
			'path': '1.0'
		}
		self.assertRaises(TypeError, path_decode, blob)

	def test_path_decode_bad_blob(self):
		blob = {
			'path': '1.0'
		}
		self.assertRaises(KeyError, path_decode, blob)
		blob = {}
		self.assertRaises(KeyError, path_decode, blob)
