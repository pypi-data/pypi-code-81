import os

import requests
from urllib.parse import urlparse, urljoin

from ..meta import Stage
from .utils import *

__all__ = [
  'download',
  'locate'
]

CHUNK_SIZE = 1024 * 1024

def download_and_save(url, path, warn=True, progress=None, cache_downloads=True):
  if os.path.exists(path):
    raise IOError('Path %s already exists!' % path)

  if cache_downloads:
    import io
    cache = io.BytesIO()
  else:
    cache = open(path, 'wb')

  with cache:
    response = requests.get(url, stream=True)
    total = int(response.headers.get('content-length', None))

    if warn:
      import warnings
      warnings.warn('Downloading %s: %s to %s' % (
        format_size(total) if total is not None else '[unknown size]',
        url, path
      ))

    if progress is not None:
      pbar = progress(total=total, desc=os.path.basename(path), unit='iB', unit_scale=True)
      update = pbar.update
    else:
      update = lambda n: None

    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
      cache.write(chunk)
      update(len(chunk))

    if cache_downloads:
      with open(path, 'wb') as f:
        f.write(cache.getvalue())

  return path

def ensure_downloaded(root, *urls, root_url=None, warn=True, progress=None, cache_downloads=True):
  ensure_directory(root)
  results = []

  for _url in urls:
    if root_url is not None:
      url = urljoin(root_url, _url)
    else:
      url = _url

    path = os.path.join(root, os.path.basename(urlparse(url).path))
    results.append(path)

    if not os.path.exists(path):
      download_and_save(url, path, warn=warn, progress=progress, cache_downloads=cache_downloads)

  if len(results) == 1:
    return results[0]
  else:
    return tuple(results)

class Download(Stage):
  def __init__(self, path, *urls, root_url=None):
    self.urls = urls
    self.path = path
    self.root_url = root_url

    if root_url is None:
      name = 'download(%s)' % (', '.join(urls))
    else:
      name = 'download(%s[%s])' % (root_url, ', '.join(urls))

    super(Download, self).__init__(name=name)

  def load(self, root=None, warn=True, progress=None, cache_downloads=True):
    return self.get_output_for(
      root,
      warn=warn, progress=progress, cache_downloads=cache_downloads
    )

  def get_output_for(self, root=None, warn=True, progress=None, cache_downloads=True):
    path = os.path.join(root, self.path)
    return ensure_downloaded(
      path, *self.urls, root_url=self.root_url,
      warn=warn, progress=progress, cache_downloads=cache_downloads
    )

download = Download

class Locate(Stage):
  def __init__(self, *items):
    self.items = items
    super(Locate, self).__init__(
      name='locate(%s)' % (', '.join(self.items))
    )

  def load(self, root=None):
    return self.get_output_for(root=root)

  def get_output_for(self, *args, root=None):
    results = []

    for item in self.items:
      path = os.path.join(root, item)
      if not os.path.exists(path):
        raise FileNotFoundError('File %s not found' % (path, ))

      results.append(path)

    if len(results) == 1:
      return results[0]
    else:
      return results

locate = lambda *path: lambda: Locate(*path)