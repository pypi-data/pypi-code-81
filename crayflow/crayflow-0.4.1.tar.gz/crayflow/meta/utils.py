import os

__all__ = [
  'get_data_root'
]

DATA_ROOT_VARS = [
  'DATA_ROOT'
]

def get_data_root(root=None):
  if root is not None:
    return root

  for data_root_var in DATA_ROOT_VARS:
    if data_root_var in os.environ:
      return os.environ[data_root_var]

  return os.path.abspath('./')