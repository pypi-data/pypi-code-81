"""
JavaScript/TypeScript compiler for portapy.

This
"""

import typing
import os
import datetime
import shutil

from portapy.core import Model
from portapy.compiler import *


def to_js_type(data: typing.Type) -> str:
    """
    Convert a Python type to a JavaScript type.
    """
    is_array = False
    result = 'any'

    if isinstance(data, Model):
        if isinstance(data.struct, (list, tuple)):
            data = data.struct[0]
            is_array = True
        if isinstance(data.struct, dict) and data.name:
            result = data.name
        else:
            data = data.struct

    if data is str:
        result = 'string'
    if data is int or data is float:
        result = 'number'
    if data is bool:
        result = 'boolean'

    try:
        if issubclass(data, datetime.date):
            result = 'Date'
    except TypeError:
        pass

    return '{}{}'.format(result, '[]' if is_array else '')


filters = {
    'to_js_type': to_js_type,
}


Manifest(
    Function(shutil.rmtree, '__pycache__', ignore_errors=True),
    Function(shutil.rmtree, 'node_modules', ignore_errors=True),
    Function(os.unlink, '__init__.py'),

    Shell('npm install'),
    Template(
        'src/client.ts.jinja',
        'src/client.ts',
        filters=filters,
        keep=False
    ),
    Shell('npm run tsfmt -- -r src/client.ts'),
    Shell('npm run build'),

    dist_dir='build/dist',
)
