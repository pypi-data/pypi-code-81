from unittest import TestCase
import io
import sys
sys.path.append('./src/')
import cfjson

class Test(TestCase):

	def test_dump(self):
		data = {
			1: 1,
			'2': 2,
			3: {
				'w': 987698765986587
			},
			4: ["item1", "item2"]
		}

		fh = io.StringIO()
		cfjson.dump(data, fh)
		self.assertEqual(fh.getvalue(), '{"1": 1, "2": 2, "3": {"w": 987698765986587}, "4": ["item1", "item2"]}')

	def test_load(self):
		fh = io.StringIO('{"1": 1, "2": 2, "3": {"w": 987698765986587}, "4": ["item1", "item2"]}')
		data = cfjson.load(fh)
		self.assertDictEqual(data, {
			'1': 1,
			'2': 2,
			'3': {
				'w': 987698765986587
			},
			'4': ["item1", "item2"]
		})

	def test_dump_and_load_round_trip(self):
		data_in = {
			'1': 1,
			'2': 2,
			'3': {
				'w': 987698765986587
			},
			'4': ["item1", "item2"]
		}

		fh = io.StringIO()
		cfjson.dump(data_in, fh)
		fh.seek(0)
		data_out = cfjson.load(fh)

		self.assertDictEqual(data_in, data_out)

	def test_dumps(self):
		data = {
			1: 1,
			'2': 2,
			3: {
				'w': 987698765986587
			},
			4: ["item1", "item2"]
		}
		output = cfjson.dumps(data)
		self.assertEqual(output, '{"1": 1, "2": 2, "3": {"w": 987698765986587}, "4": ["item1", "item2"]}')

	def test_loads(self):
		input_data = '{"1": 1, "2": 2, "3": {"w": 987698765986587}, "4": ["item1", "item2"]}'
		data = cfjson.loads(input_data)
		self.assertDictEqual(data, {
			'1': 1,
			'2': 2,
			'3': {
				'w': 987698765986587
			},
			'4': ["item1", "item2"]
		})

	def test_dumps_and_loads_round_trip(self):
		data_in = {
			'1': 1,
			'2': 2,
			'3': {
				'w': 987698765986587
			},
			'4': ["item1", "item2"]
		}

		output_string = cfjson.dumps(data_in)
		data_out = cfjson.loads(output_string)

		self.assertDictEqual(data_in, data_out)
