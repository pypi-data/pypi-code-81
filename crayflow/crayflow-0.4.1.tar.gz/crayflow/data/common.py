import numpy as np

__all__ = [
  'normalize',
  'box',
  'onehot',
  'categorical_encoding',
  'categorical_to_numerical',
  'binary_encoding',
  'split'
]

def get_buffers(data, inline=True, dtype=None):
  results = list()
  for d in data:
    if not isinstance(d, np.ndarray):
      d = np.asarray(d, dtype=dtype)

    if dtype is None:
      target_dtype = d.dtype if np.dtype(d.dtype).kind == 'f' else np.float32
    else:
      target_dtype = np.dtype(dtype)

    if inline and target_dtype == d.dtype:
      results.append(d)
    else:
      out = np.ndarray(shape=d.shape, dtype=target_dtype)
      results.append(out)

  return tuple(results)


def normalize(data_ref=None, center=True, scale=True, axes=(0,), scale_eps=1e-3, inline=True, dtype=None):
  """
  (X - mean) / (std + eps)

  Statistics are computed for the first argument.


  Example:
    `data_train, data_test = normalize(data_train)(data_train, data_test)`

  :param data_ref: dataset to compute statistics on, if None, statistics are computed for each supplied array individually;
  :param center: if True, centers input;
  :param scale: if True, divides input by (std + eps)
  :param axes: axes to average over;
  :param scale_eps: a small constant added to denominator to avoid division by a small number;
  :param inline: if possible, tries to perform inline operations;
  :param dtype: if None, tries to preserve original input's dtype
    (if the latter is of an integer type then defaults to float32),
    otherwise, outputs arrays of the specified type.

  :return: transform function
  """

  if data_ref is not None:
    mean = np.mean(data_ref, axis=axes) if center else None
    std = np.std(data_ref, axis=axes) + scale_eps if scale else None
  else:
    mean, std = None, None

  def normalize_transform(*data):
    if len(data) == 0:
      return tuple()

    broadcast = tuple(
      None if i in axes else slice(None, None, None)
      for i, _ in enumerate(data[0].shape)
    )

    results = get_buffers(data, inline=inline, dtype=dtype)

    for d, out in zip(data, results):
      if center:
        mean_ = mean if mean is not None else np.mean(d, axis=axes)
        centered = np.subtract(d, mean_[broadcast], out=out)
      else:
        centered = d

      if scale:
        std_ = std if std is not None else (np.std(d, axis=axes) + scale_eps)
        np.divide(centered, std_[broadcast], out=out)

    return results

  return normalize_transform

def box(data_ref, inline=True, eps=1e-3):
  max = np.max(data_ref, axis=0)
  min = np.min(data_ref, axis=0)
  delta = np.maximum(max - min, eps)

  def box_transform(*data):
    if len(data) == 0:
      return tuple()

    broadcast = (None, ) + tuple(slice(None, None, None) for _ in data[0].shape[1:])
    results = data if inline else tuple([ d.copy() for d in data ])

    for d, out in zip(data, results):
      np.subtract(d, min[broadcast], out=out)
      np.divide(out, delta[broadcast], out=out)

    return results

  return box_transform


def onehot(n_classes=None, dtype=np.float32):
  def onehot_transform(y):
    if y.dtype.kind != 'i':
      y = y.astype('int64')

    n_classes_ = (np.max(y) + 1) if n_classes is None else n_classes

    y_ = np.zeros(shape=(y.shape[0], n_classes_), dtype=dtype)
    y_[np.arange(y.shape[0]), y] = 1

    return y_

  return onehot_transform


def ceil_log2(n):
  i, x = 0, 1

  while n > x:
    x *= 2; i += 1

  return i

def categorical_encoding(*data, fixed=None):
  if fixed is None:
    encoding = dict()
  else:
    encoding = fixed.copy()

  current = 0

  for d in data:
    for item in d:
      if item not in encoding:
        while current in encoding.values():
          current += 1

        encoding[item] = current

  return encoding

def categorical_to_numerical(data, encoding=None, fixed=None, dtype='int32'):
  if encoding is None:
    encoding = categorical_encoding(data, fixed=fixed)

  result = np.ndarray(shape=(len(data),), dtype=dtype)

  for i, item in enumerate(data):
    result[i] = encoding[item]

  return result

def binary_encoding(dtype='float32', size=None):
  def binary_encoding_transform(y):
    y = np.array(y)

    n_bits = ceil_log2(
      size if size is not None else (np.max(y) + 1)
    )
    power_2 = 2 ** np.arange(n_bits)[::-1]

    return np.where(
      np.mod(y[:, None] // power_2, 2) != 0,
      np.ones(shape=tuple(), dtype=dtype),
      np.zeros(shape=tuple(), dtype=dtype),
    )

  return binary_encoding_transform

def split(split_ratios=0.8, seed=None):
  try:
    iter(split_ratios)
  except TypeError:
    split_ratios = (split_ratios, 1 - split_ratios)

  assert all([r >= 0 for r in split_ratios])

  split_ratios = np.array(split_ratios)

  def split_transform(*data):
    if len(data) == 0:
      return tuple()

    size = len(data[0])

    split_sizes = np.ceil((split_ratios * size) / np.sum(split_ratios)).astype('int64')
    split_bins = np.cumsum([0] + list(split_sizes))
    split_bins[-1] = size

    rng = np.random.RandomState(seed)
    r = rng.permutation(size)

    result = list()

    for i, _ in enumerate(split_ratios):
      from_indx = split_bins[i]
      to_indx = split_bins[i + 1]
      indx = r[from_indx:to_indx]

      for d in data:
        if isinstance(d, np.ndarray):
          result.append(d[indx])
        else:
          result.append([ d[i] for i in indx ])

    return tuple(result)

  return split_transform