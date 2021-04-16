import inspect
import pickle
from hashlib import sha256

__all__ = [
  'get_function_hash',
  'join_hashes'
]

def _inspect_function(function):
  closures = inspect.getclosurevars(function)
  marks = [closures.globals, closures.nonlocals]

  for mark in marks:
    for k, v in mark.items():
      yield k, v

def _inspect_object(obj):
  for k in dir(obj):
    v = getattr(obj, k)
    if inspect.ismethod(v):
      yield k, v
    elif not k.startswith('__'):
      yield k, v

def _inspect(obj):
  if inspect.isfunction(obj) or inspect.ismethod(obj):
    return _inspect_function(obj)
  else:
    return _inspect_object(obj)

def get_dependencies(function):
  module = inspect.getmodule(function)
  values = dict()

  stack = [('', function)]

  while len(stack) > 0:
    name, current = stack.pop()

    if name in values:
      continue
    else:
      values[name] = current

    for k, v in _inspect(current):
      if inspect.isfunction(current) or inspect.ismethod(current):
        path = k
      else:
        path =  '%s.%s' % (name, k)

      if inspect.ismethod(v) or inspect.isfunction(v):
        if inspect.getmodule(v) == module:
          stack.append((path, v))
      else:
        if inspect.getmodule(v) == module:
          stack.append((path, v))
        else:
          values[path] = v

  return values


def get_function_hash(function):
  ### self is missing from method's closures.
  if inspect.ismethod(function):
    return _get_function_hash(function.__call__.__self__)
  else:
    return _get_function_hash(function)

def _get_function_hash(function):
  values = get_dependencies(function)
  keys = sorted(values.keys())

  h = sha256()

  for k in keys:
    value = values[k]
    if inspect.isfunction(value) or inspect.ismethod(value):
      source = inspect.getsource(value).encode()
    else:
      try:
        source = pickle.dumps(value)
      except (TypeError, AttributeError):
        source = k.encode()

    h.update(source)

  return h.hexdigest()

def join_hashes(*hashes):
  if len(hashes) == 1:
    return hashes[0]
  else:
    super_hash = sha256()
    for hash in hashes:
      super_hash.add(hash.encode())

    return super_hash.hexdigest()