"""
datetime
^^^^^^^^

:class:`datetime.datetime` is serialized as an isoformat string.

>>> import datetime
>>> data = datetime.datetime.utcnow()
>>> serialized = data.isoformat()
>>> serialized
'2021-04-07T00:00:08.114099'
>>> data = datetime.datetime.fromisoformat(serialized)
datetime.datetime(2021, 4, 7, 0, 0, 8, 114099)
"""

from ..coder import JsonTypeRegister

import datetime

if hasattr(datetime.datetime, 'fromisoformat'):  # pragma: no cover
	def datetime_deserializer(s):
		return datetime.datetime.fromisoformat(s)
else:  # pragma: no cover
	# datetime.fromisoformat() was introduced in Python 3.7, patch in a work around for older versions.
	import dateutil.parser

	def datetime_deserializer(s):
		return dateutil.parser.parse(s)


def datetime_decode(dct):
	"""Decode json dict into class objects."""
	cls_name = dct['__json_type__']
	if cls_name == 'datetime':
		return datetime_deserializer(dct['datetime'])
	raise TypeError()


def datetime_encode(obj):
	"""Encode the object into a json safe dict."""
	return {
		'__json_type__': 'datetime',
		'datetime': obj.isoformat()
	}


JsonTypeRegister.register('datetime', datetime_encode, datetime_decode)
