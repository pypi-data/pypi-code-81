### based on https://github.com/thomalm/svhn-multi-digit/blob/master/unpacker.py

import numpy as np
from ..sources import download

__all__ = [
  'download_svhn_train_cropped', 'download_svhn_test_cropped', 'download_svhn_extra_cropped',
  'download_svhn_cropped', 'download_svhn_full_cropped',

  'read_svhn_cropped'
]

ROOT_URL = 'http://ufldl.stanford.edu/housenumbers/'

TRAIN_32x32_FILENAME = 'train_32x32.mat'
TEST_32x32_FILENAME = 'test_32x32.mat'
EXTRA_32x32_FILENAME = 'extra_32x32.mat'

download_svhn_train_cropped = lambda path: lambda: download(path, TRAIN_32x32_FILENAME, root_url=ROOT_URL)
download_svhn_test_cropped = lambda path: lambda: download(path, TEST_32x32_FILENAME, root_url=ROOT_URL)
download_svhn_extra_cropped = lambda path: lambda: download(path, EXTRA_32x32_FILENAME, root_url=ROOT_URL)

download_svhn_cropped = lambda path: lambda: download(
  path,
  TRAIN_32x32_FILENAME, TEST_32x32_FILENAME,
  root_url=ROOT_URL
)

download_svhn_full_cropped = lambda path: lambda: download(
  path,
  TRAIN_32x32_FILENAME, TEST_32x32_FILENAME, EXTRA_32x32_FILENAME,
  root_url=ROOT_URL
)

def read_svhn_cropped():
  def read(*paths):
    import scipy.io
    results = list()

    for path in paths:
      data = scipy.io.loadmat(path)
      X, y = data['X'], data['y']

      ### original format: spatial x, spatial y, channel, batch
      X = np.transpose(X, axes=(3, 2, 0, 1))

      ### for some reason digit 0 has label 10...
      y = y.reshape((-1, )) % 10

      results.append(X)
      results.append(y)

    return tuple(results)
  return read