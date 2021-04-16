import numpy as np

__all__ = [
  'to_channel_first',
  'to_channel_last',
  'resize',
  'cast'
]

def to_channel_first():
  def to_channel_first_transform(imgs):
    axes = tuple(range(len(imgs.shape)))
    perm = (axes[0], ) + (axes[-1], ) + axes[1:-1]
    return np.transpose(imgs, axes=perm)

  return to_channel_first_transform

def to_channel_last():
  def to_channel_last_transform(imgs):
    axes = tuple(range(len(imgs.shape)))
    perm = (axes[0], ) + axes[2:] + (axes[1], )
    return np.transpose(imgs, axes=perm)

  return to_channel_last_transform

def _to_channel_first(img):
  axes = tuple(range(len(img.shape)))
  perm = (axes[-1], ) + axes[:-1]
  return np.transpose(img, axes=perm)

def _to_channel_last(img):
  axes = tuple(range(len(img.shape)))
  perm = axes[1:] + (axes[0], )
  return np.transpose(img, axes=perm)

def resize(new_size, order=3, dtype='float32', **kwargs):
  def resize_transform(imgs, progress=None):
    if progress is None:
      progress = lambda x, desc=None: x

    from skimage.transform import resize
    result = np.ndarray(shape=imgs.shape[:2] + new_size, dtype=dtype)

    for i in progress(range(imgs.shape[0]), desc='resizing'):
      result[i] = _to_channel_first(
        resize(
          _to_channel_last(imgs[i].astype(dtype)),
          output_shape=new_size, order=order, **kwargs
        )
      )

    return result

  return resize_transform

def cast(dtype='float32', normalize=True):
  """
  Casts input array to `dtype` and divides by 255 if `dtype` is a float type and input array is of an integer type.
  Raises an exception if `dtype` is a non-float and `normalize` is set to True.
  `normalize` is ignored if input array is already a float array.
  """
  if np.dtype(dtype).kind == 'f' and normalize:
    raise Exception('Can not normalize and cast to a non-float type at the same time!')

  def f(imgs):
    imgs = np.asarray(imgs)
    if np.dtype(imgs.dtype).kind != 'f' and normalize:
      return np.asarray(imgs, dtype=dtype) / 255.0
    else:
      return np.asarray(imgs, dtype=dtype)

  return f