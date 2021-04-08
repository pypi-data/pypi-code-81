"""
pathlib
^^^^^^^

:class:`pathlib.Path` is serialized as a string.

>>> import pathlib
>>> data = pathlib.Path('../source')
>>> serialized = str(data)
>>> serialized
'..\\source'
>>> data = pathlib.Path(serialized)
WindowsPath('../source')

Note: :mod:`pathlib` paths are platform specific. Special care must be taken if you are expecting the data to be
shared across systems.
"""

from ..cfjson import JsonTypeRegister


def path_decode(dct):
	"""Decode json dict into class objects."""
	from pathlib import Path
	cls_name = dct['__json_type__']
	if cls_name in ('Path', 'WindowsPath', 'PosixPath'):
		return Path(dct['path'])
	raise TypeError()


def path_encode(obj):
	"""Encode the object into a json safe dict."""
	return {
		'__json_type__': type(obj).__name__,
		'path': str(obj)
	}


JsonTypeRegister.register('Path', path_encode, path_decode)
JsonTypeRegister.register('WindowsPath', path_encode, path_decode)
