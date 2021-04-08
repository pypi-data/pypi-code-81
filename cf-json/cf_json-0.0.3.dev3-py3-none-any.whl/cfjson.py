import json

JSONEncoder = json.JSONEncoder
JSONDecoder = json.JSONDecoder


class MyEncoder(JSONEncoder):
	"""MyDecoder hooks into :meth:`json.dump` and :meth:`json.dumps`"""

	def default(self, o):
		""""""
		if hasattr(o, '__json_encode__'):
			return o.__json_encode__()
		try:
			return JsonTypeRegister.encode(type(o).__name__, o)
		except KeyError:
			pass
		return super(MyEncoder, self).default(o)


class MyDecoder(JSONDecoder):
	"""MyDecoder hooks into :meth:`json.load` and :meth:`json.loads`"""

	def __init__(self, *args, **kwargs):
		super(MyDecoder, self).__init__(object_hook=self.object_hook, *args, **kwargs)

	def object_hook(self, dct):
		""""""
		if '__json_type__' in dct:
			return JsonTypeRegister.decode(dct['__json_type__'], dct)
		return dct


class JsonTypeRegister(object):
	"""Central location responsible for managing the mapping of class and class names to the appropriate encoders and
	decoders.

	:class:`JsonTypeRegister` has two sides:

	1. The user facing side  is for registering :ref:`encoders and decoders <encoderdecoder>`.

	2. The :mod:`json` facing side is to run a switch board for :class:`MyEncoder` and :class:`MyDecoder` connecting them to
	   the appropriate functions and methods for the type they are encoding / decoding in the moment.
	"""

	encoders = dict()
	decoders = dict()

	def __init__(self):
		super(JsonTypeRegister, self).__init__()

	@classmethod
	def register(cls, type_name: str, encoder: callable = None, decoder: callable = None):
		"""Helper for registering both an encode and custom_decoder in one call."""
		if encoder:
			cls.register_encoder(type_name, encoder)
		if decoder:
			cls.register_decoder(type_name, decoder)

	@classmethod
	def register_encoder(cls, type_name: str, custom_encoder: callable):
		"""Registers the custom_encoder against the type name.

		When the :mod:`json` encoder finds a type with name that has been registered, the custom_encoder will be called.
		The first argument will be the instance to be encoded.
		"""
		cls.encoders[type_name] = custom_encoder

	@classmethod
	def register_decoder(cls, type_name: str, custom_decoder: callable):
		"""Registers the custom_decoder against the type name.

		When the :mod:`json` decoder finds the type name in the serialized json, the custom_decoder will be called.
		The first argument will be the serialized json dict to be decoder.
		"""
		cls.decoders[type_name] = custom_decoder

	@classmethod
	def encode(cls, type_name, obj):
		"""Returns an encoded object if we have a registered handler or raise an exception."""
		if type_name in cls.encoders:
			return cls.encoders[type_name](obj)
		elif hasattr(obj, '__json_encode__'):
			return obj.__json_encode__()
		raise KeyError('Failed to find custom_encoder for {}'.format(obj))

	@classmethod
	def decode(cls, type_name, dct):
		"""Returns a decoded object if we have a registered handler or raise an exception."""
		if type_name in cls.decoders:
			return cls.decoders[type_name](dct)
		raise KeyError('Failed to find custom_decoder for {}'.format(dct))

