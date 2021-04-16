import os.path as osp
import numpy as np

from ..data import onehot
from ..sources import download

__all__ = [
  'download_cifar10', 'download_cifar100',
  'read_cifar10', 'read_cifar100'
]

CIFAR_ROOT_URL = 'https://www.cs.toronto.edu/~kriz/'

CIFAR_10_PATH = 'cifar-10-python.tar.gz'
CIFAR_100_PATH = 'cifar-100-python.tar.gz'

CIFAR_10_ARCHIVE_PREFIX = 'cifar-10-batches-py'
CIFAR_100_ARCHIVE_PREFIX = 'cifar-100-python'

download_cifar10 = lambda path: lambda: download(path, CIFAR_10_PATH, root_url=CIFAR_ROOT_URL)
download_cifar100 = lambda path: lambda: download(path, CIFAR_100_PATH, root_url=CIFAR_ROOT_URL)

def _cifar(path, train_files, test_files, labels_names, one_hot=None, cast='float32'):
  def extract_batch(f):
    import pickle
    d = pickle.load(f, encoding='bytes')
    imgs = d[b'data'].reshape((-1, 3, 32, 32))
    labels = [ d[key] for key in labels_names ]
    return imgs, labels

  def read_data(f, files):
    imgs, labels = zip(*[
      extract_batch(f.extractfile(path)) for path in files
    ])

    imgs = np.concatenate(imgs, axis=0)
    labels = [np.concatenate(l, axis=0) for l in zip(*labels)]

    return imgs, labels

  import tarfile
  with tarfile.open(path, 'r:gz') as f:
    X_train, y_train = read_data(f, train_files)
    X_test, y_test = read_data(f, test_files)

  if one_hot is not None:
    y_train = [
      onehot(n_classes=one_hot)(y)
      for y in y_train
    ]
    y_test = [
      onehot(n_classes=one_hot)(y)
      for y in y_test
    ]

  if cast is True:
    cast = 'float32'

  if cast is not None:
    X_train = X_train.astype(cast)
    X_test = X_test.astype(cast)
    y_train = [ y.astype(cast) for y in y_train ]
    y_test = [ y.astype(cast) for y in y_test ]

    if np.dtype(cast).kind == 'f':
      X_train /= 255.0
      X_test /= 255.0

  return X_train, y_train, X_test, y_test


def read_cifar10(one_hot=True, cast='float32'):
  def read(path):
    train_files = [
      osp.join(CIFAR_10_ARCHIVE_PREFIX, 'data_batch_%d' % (i + 1, ))
      for i in range(5)
    ]
    test_files = [ osp.join(CIFAR_10_ARCHIVE_PREFIX, 'test_batch') ]

    X_train, y_train, X_test, y_test = _cifar(
      path,
      train_files=train_files, test_files=test_files,
      labels_names=[b'labels'],
      one_hot=10 if one_hot else None, cast=cast
    )

    assert len(y_train) == 1
    assert len(y_test) == 1

    return X_train, y_train[0], X_test, y_test[0]

  return read

def read_cifar100(one_hot=True, cast='float32'):
  def read(path):
    train_files = [osp.join(CIFAR_100_ARCHIVE_PREFIX, 'train')]
    test_files = [osp.join(CIFAR_100_ARCHIVE_PREFIX, 'test')]

    return _cifar(
      path,
      train_files=train_files, test_files=test_files,
      labels_names=[b'coarse_labels', b'fine_labels'],
      one_hot=100 if one_hot else None,
      cast=cast
    )

  return read