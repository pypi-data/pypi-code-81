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

from ..cfjson import JsonTypeRegister


def datetime_decode(dct):
	"""Decode json dict into class objects."""
	from datetime import datetime
	cls_name = dct['__json_type__']
	if cls_name == 'datetime':
		return datetime.fromisoformat(dct['datetime'])
	raise TypeError()


def datetime_encode(obj):
	"""Encode the object into a json safe dict."""
	return {
		'__json_type__': 'datetime',
		'datetime': obj.isoformat()
	}


JsonTypeRegister.register('datetime', datetime_encode, datetime_decode)
