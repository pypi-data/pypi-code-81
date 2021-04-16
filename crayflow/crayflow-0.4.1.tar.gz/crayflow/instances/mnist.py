import numpy as np

from ..data import onehot
from ..sources.utils import unpack_gz
from ..sources.load import download

__all__ = [
  'download_mnist_train',
  'download_mnist_test',
  'download_mnist',

  'read_mnist',
]

ROOT_URL = 'http://yann.lecun.com/exdb/mnist/'

TRAIN_DATA = 'train-images-idx3-ubyte.gz'
TRAIN_LABELS = 'train-labels-idx1-ubyte.gz'

TEST_DATA = 't10k-images-idx3-ubyte.gz'
TEST_LABELS = 't10k-labels-idx1-ubyte.gz'

download_mnist_train = lambda path: lambda: download(path, TRAIN_DATA, TRAIN_LABELS, root_url=ROOT_URL)
download_mnist_test = lambda path: lambda: download(path, TEST_DATA, TEST_LABELS, root_url=ROOT_URL)
download_mnist = lambda path: lambda: download(path, TRAIN_DATA, TRAIN_LABELS, TEST_DATA, TEST_LABELS, root_url=ROOT_URL)

def _read_mnist_pair(data_path, labels_path, one_hot=True, cast='float32'):
  from array import array
  import struct

  data_raw = unpack_gz(data_path)
  _, _, n_rows, n_cols = struct.unpack(">IIII", data_raw[:16])
  data = np.array(array("b", data_raw[16:]), dtype='uint8').reshape((-1, 1, n_rows, n_cols))

  labels_raw = unpack_gz(labels_path)
  labels = np.array(array("b", labels_raw[8:]), dtype='uint8')

  if one_hot:
    labels = onehot(n_classes=10)(labels)

  if cast is not None:
    data = data.astype(cast)
    labels = labels.astype(cast)

  if np.dtype(cast).kind == 'f':
    data /= 255.0

  return data, labels

def read_mnist(one_hot=True, cast='float32'):
  def read(*pathes):
    assert len(pathes) % 2 == 0, 'Looks like label files are missing'

    return tuple([
      arr
      for i in range(len(pathes) // 2)
      for arr in _read_mnist_pair(pathes[2 * i], pathes[2 * i + 1], one_hot=one_hot, cast=cast)
    ])

  return read