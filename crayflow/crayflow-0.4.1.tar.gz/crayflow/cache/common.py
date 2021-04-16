import os

from ..meta import Cache
from ..sources.utils import *

__all__ = [
  'pickled',
  'npz_cache',
  'npy_cache',
  'no_cache'
]

class PickleCache(Cache):
  def __init__(self, path):
    self.path = path

  def save(self, obj, root=None):
    import pickle
    path = os.path.join(root, self.path)
    ensure_directory(os.path.dirname(path))

    with open(path, 'wb') as f:
      pickle.dump(obj, f)

  def load(self, root=None):
    import pickle
    path = os.path.join(root, self.path)
    ensure_directory(os.path.dirname(path))

    with open(path, 'rb') as f:
      return pickle.load(f)

class NPZCache(Cache):
  def __init__(self, path, *names):
    self.path = path
    self.names = names

  def save(self, obj, root=None):
    import numpy as np
    path = os.path.join(root, self.path)

    np.savez(path, zip(obj, self.names))

  def load(self, root=None):
    import numpy as np
    path = os.path.join(root, self.path)

    with np.load(path) as f:
      result = tuple([
        f[name] for name in self.names
      ])

    return result

class NPYCache(Cache):
  def __init__(self, path):
    self.path = path

  def save(self, obj, root=None):
    import numpy as np
    path = os.path.join(root, self.path)

    np.save(path, obj, allow_pickle=False)

  def load(self, root=None):
    import numpy as np
    path = os.path.join(root, self.path)

    return np.load(path, allow_pickle=False, )

pickled = PickleCache
npz_cache = NPZCache
npy_cache = NPYCache

from ..meta import NoCache
no_cache = NoCache