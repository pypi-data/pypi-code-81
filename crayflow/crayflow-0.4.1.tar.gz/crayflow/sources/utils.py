import os.path as osp
import os

__all__ = [
  'ensure_directory',
  'extract_tar',
  'unpack_gz',
  'format_size'
]

def ensure_directory(path):
  if not osp.exists(path):
    os.makedirs(path)
  else:
    if not osp.isdir(path):
      raise Exception('%s is present but is not a directory!' % path)
    else:
      pass

def extract_tar(path, destination, mode='r:gz'):
  import tarfile

  with tarfile.open(path, mode) as f:
    f.extractall(destination)

def unpack_gz(path):
  import gzip

  with gzip.open(path, 'rb') as f:
    return f.read()

def unzip(path):
  import zipfile
  destination = os.path.dirname(path)

  with zipfile.ZipFile(path, mode='r') as zf:
    files = zf.namelist()
    if all([
      osp.exists(osp.join(destination, item))
      for item in files
    ]):
      pass
    else:
      zf.extractall(path=destination)

    return destination

suffixes = ('bytes', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB')
def format_size(size_bytes):
  i = 0
  while size_bytes > 1000 and i < len(suffixes):
    size_bytes /= 1000.0
    i += 1

  return '%.1lf %s' % (size_bytes, suffixes[i])