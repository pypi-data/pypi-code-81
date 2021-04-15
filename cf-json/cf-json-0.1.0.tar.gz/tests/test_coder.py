from unittest import TestCase
import sys

sys.path.append('./src/')
sys.path.append('../src/')
from cfjson import JsonTypeRegister, dumps, loads


class TestJsonTypeRegister(TestCase):

	def test_register_func(self):

		JsonTypeRegister.reset()

		class MyClass(object):

			@staticmethod
			def create(value):
				return MyClass(value)

			def __init__(self, value):
				self.value = value
				self.encoder_called = False

			def __eq__(self, other):
				return self.value == other.value

		def encoder_func(obj):
			"""Encode the object into a json safe dict."""
			return {
				'__json_type__': 'MyClass',
				'my_class': obj.value
			}

		def decoder_func(dct):
			"""Decode json dict into class objects."""
			cls_name = dct['__json_type__']
			if cls_name == 'MyClass':
				return MyClass.create(dct['my_class'])
			raise TypeError()

		input_data = [MyClass('test'), MyClass('tock')]
		# Test failure when we haven't registered yet
		self.assertRaises(TypeError, dumps, input_data)

		JsonTypeRegister.register('MyClass', encoder_func, None)
		output_string = dumps(input_data)

		# Test failure when we haven't registered yet
		self.assertRaises(KeyError, loads, output_string)

		JsonTypeRegister.register('MyClass', encoder_func, decoder_func)

		# Test success
		output_string = dumps(input_data)
		output_data = loads(output_string)
		self.assertEqual(input_data, output_data)

	def test_register_cls(self):
		JsonTypeRegister.reset()

		class MyClass(object):

			@staticmethod
			def create(value):
				return MyClass(value)

			def __init__(self, value):
				self.value = value
				self.encoder_called = False

			def __eq__(self, other):
				return self.value == other.value

			def __json_encode__(self):
				"""Encode the object into a json safe dict."""
				return {
					'__json_type__': 'MyClass',
					'my_class': self.value
				}

		def decoder_func(dct):
			"""Decode json dict into class objects."""
			cls_name = dct['__json_type__']
			if cls_name == 'MyClass':
				return MyClass.create(dct['my_class'])
			raise TypeError()

		input_data = [MyClass('test'), MyClass('tock')]
		output_string = dumps(input_data)

		# Test failure when we haven't registered yet
		self.assertRaises(KeyError, loads, output_string)

		JsonTypeRegister.register('MyClass', None, decoder_func)

		# Test success
		output_string = dumps(input_data)
		output_data = loads(output_string)
		self.assertEqual(input_data, output_data)

	def test_register_encoder(self):

		JsonTypeRegister.reset()

		class MyClass(object):

			@staticmethod
			def create(value):
				return MyClass(value)

			def __init__(self, value):
				self.value = value
				self.encoder_called = False

			def __eq__(self, other):
				return self.value == other.value

		def encoder_func(obj):
			"""Encode the object into a json safe dict."""
			return {
				'__json_type__': 'MyClass',
				'my_class': obj.value
			}

		input_data = [MyClass('test'), MyClass('tock')]
		# Test failure when we haven't registered yet
		self.assertRaises(TypeError, dumps, input_data)

		JsonTypeRegister.register_encoder('MyClass', encoder_func)
		output_string = dumps(input_data)

		# Test failure when we haven't registered yet
		self.assertRaises(KeyError, loads, output_string)

	def test_register_decoder(self):

		JsonTypeRegister.reset()

		class MyClass(object):

			@staticmethod
			def create(value):
				return MyClass(value)

			def __init__(self, value):
				self.value = value
				self.encoder_called = False

			def __eq__(self, other):
				return self.value == other.value

			def __json_encode__(self):
				"""Encode the object into a json safe dict."""
				return {
					'__json_type__': 'MyClass',
					'my_class': self.value
				}


		def decoder_func(dct):
			"""Decode json dict into class objects."""
			cls_name = dct['__json_type__']
			if cls_name == 'MyClass':
				return MyClass.create(dct['my_class'])
			raise TypeError()

		input_data = [MyClass('test'), MyClass('tock')]
		output_string = dumps(input_data)

		# Test failure when we haven't registered yet
		self.assertRaises(KeyError, loads, output_string)

		JsonTypeRegister.register_decoder('MyClass', decoder_func)

		# Test success
		output_string = dumps(input_data)
		output_data = loads(output_string)
		self.assertEqual(input_data, output_data)
