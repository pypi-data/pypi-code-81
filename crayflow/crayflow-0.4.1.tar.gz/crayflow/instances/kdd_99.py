import numpy as np

from ..data import categorical_encoding, categorical_to_numerical, onehot, box
from ..sources import download

KDD_99_URL = 'http://archive.ics.uci.edu/ml/machine-learning-databases/kddcup99-mld/kddcup.data.gz'
KDD_99_TEST_URL = 'http://kdd.ics.uci.edu/databases/kddcup99/corrected.gz'

KDD_99_NAMES_URL = 'http://archive.ics.uci.edu/ml/machine-learning-databases/kddcup99-mld/kddcup.names'
KDD_99_CATEGORICAL_INDEX = set([1, 2, 3, 42])
KDD_99_NUM_FEATURES = 42

__all__ = [
  'download_kdd_99',
  'read_kdd_99'
]

download_kdd_99 = lambda path: lambda: download(path, KDD_99_URL, KDD_99_TEST_URL, KDD_99_NAMES_URL)

def parse_names(path):
  with open(path, 'rb') as f:
    names = [
      str(line[:-1], encoding='UTF-8')
      for line in f.read().split(b'\n')
      if len(line) > 1
    ]

  feature_names, feature_types = zip(*[
    tuple(name.split(': '))
    for name in names[1:]
  ])
  targets = set(names[0].split(','))

  return feature_names, feature_types, targets

def parse_kdd_99(path):
  import gzip

  raw_features = None

  with gzip.open(path, mode='rb') as f:
    for line in f:
      line = str(line, encoding='UTF-8')
      ### removing period and new line
      tokens = line[:-2].split(',')

      if raw_features is None:
        raw_features = [
          list() for _ in range(len(tokens))
        ]

      for i, token in enumerate(tokens):
        raw_features[i].append(token)

  return raw_features[:-1], raw_features[-1]

def get_encoded_feature_names(encoding, feature_name=None):
  reverse_encoding = dict([ (v, k) for k, v in encoding.items() ])
  indx = sorted(encoding.values())

  if feature_name is not None:
    return [
      '%s=%s' % (feature_name, reverse_encoding[i])
      for i in indx
    ]
  else:
    return [
      reverse_encoding[i]
      for i in indx
    ]

def read_kdd_99(one_hot_target=True):
  def read(train_path, test_path, names_path):
    data_train = list()
    data_test = list()

    feature_spec = list()

    feature_names, feature_types, targets = parse_names(names_path)
    raw_train_features, raw_train_target = parse_kdd_99(train_path)
    raw_test_features, raw_test_target = parse_kdd_99(test_path)

    for i in range(len(raw_train_features)):
      if feature_types[i] == 'symbolic':
        encoding = categorical_encoding(raw_train_features[i], raw_test_features[i])

        train_column = categorical_to_numerical(raw_train_features[i], encoding=encoding)
        test_column = categorical_to_numerical(raw_test_features[i], encoding=encoding)

        if len(encoding) > 2:
          train_column = onehot(n_classes=len(encoding), dtype='float32')(train_column)
          test_column = onehot(n_classes=len(encoding), dtype='float32')(test_column)
          feature_spec.append((feature_names[i], 'categorical', (0, len(encoding) - 1)))

        else:
          train_column = train_column.astype('float32').reshape(-1, 1)
          test_column = test_column.astype('float32').reshape(-1, 1)
          feature_spec.append((feature_names[i], 'binary', (0, 1)))

      elif feature_types[i] == 'continuous':
        train_column = np.array(raw_train_features[i], dtype='float32').reshape(-1, 1)
        test_column = np.array(raw_test_features[i], dtype='float32').reshape(-1, 1)

        feature_spec.append(
          (feature_names[i], 'continuous', (np.min(train_column), np.max(train_column)))
        )
      else:
        raise ValueError('Unknown data type %s, please check integrity of `kddcup.names` file.' % (feature_types[i], ))

      data_train.append(train_column)
      data_test.append(test_column)

    data_train = np.concatenate(data_train, axis=1)
    data_test = np.concatenate(data_test, axis=1)

    target_encoding = categorical_encoding(raw_train_target, raw_test_target, fixed={'normal' : 0})
    labels_train = categorical_to_numerical(raw_train_target, encoding=target_encoding)
    labels_test = categorical_to_numerical(raw_test_target, encoding=target_encoding)

    if one_hot_target:
      labels_train = onehot(n_classes=len(target_encoding), dtype='float32')(labels_train)
      labels_test = onehot(n_classes=len(target_encoding), dtype='float32')(labels_test)

    target_names = get_encoded_feature_names(target_encoding)

    return data_train, labels_train, data_test, labels_test, feature_spec, target_names

  return read