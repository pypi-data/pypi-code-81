# Copyright 2018 The KaiJIN Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import math
import random
from typing import Sequence

import cv2
import numpy as np
import torch

from tw import transform as T
from tw import logger


__all__ = [
    "to_float",
    "to_tensor",
    "equal_hist",
    "truncated_standardize",
    "_rgb_to_yuv_bt709_videorange",
    "_rgb_to_yuv_bt709_fullrange",
    "_yuv_bt709_videorange_to_rgb",
    "_yuv_bt709_fullrange_to_rgb",
    "_change_colorspace",
    "change_colorspace",
    "color_bgr2rgb",
    "color_rgb2bgr",
    "color_bgr2gray",
    "color_rgb2gray",
    "random_iso_noise",
    "random_gaussian_blur",
    "random_gaussian_noise",
    "random_motion_blur",
    "random_median_blur",
    "_alpha_to_trimap",
    "alpha_to_trimap",
    "random_alpha_to_trimap",
    "_padding_to_size_divisible",
    "pad",
    "vflip",
    "hflip",
    "random_vflip",
    "random_hflip",
    "random_crop",
    "center_crop",
    "shortside_resize",
    "resize",
    "rotate",
    "random_rotate",
]

#!<-----------------------------------------------------------------------------
#!< CONSTANT
#!<-----------------------------------------------------------------------------

_colorspace_mapping = {
    (T.COLORSPACE.BGR, T.COLORSPACE.RGB): cv2.COLOR_BGR2RGB,
    (T.COLORSPACE.RGB, T.COLORSPACE.BGR): cv2.COLOR_RGB2BGR,
    (T.COLORSPACE.BGR, T.COLORSPACE.GRAY): cv2.COLOR_BGR2GRAY,
    (T.COLORSPACE.RGB, T.COLORSPACE.GRAY): cv2.COLOR_RGB2GRAY,

    (T.COLORSPACE.GRAY, T.COLORSPACE.RGB): cv2.COLOR_GRAY2RGB,
    (T.COLORSPACE.GRAY, T.COLORSPACE.BGR): cv2.COLOR_GRAY2BGR,

    (T.COLORSPACE.RGB, T.COLORSPACE.BT709_FULLRANGE): 'rgb_to_yuv_bt709_fullrange',
    (T.COLORSPACE.BGR, T.COLORSPACE.BT709_FULLRANGE): 'bgr_to_yuv_bt709_fullrange',
    (T.COLORSPACE.RGB, T.COLORSPACE.BT709_VIDEORANGE): 'rgb_to_yuv_bt709_videorange',
    (T.COLORSPACE.BGR, T.COLORSPACE.BT709_VIDEORANGE): 'bgr_to_yuv_bt709_videorange',

    (T.COLORSPACE.BT709_FULLRANGE, T.COLORSPACE.RGB): 'yuv_bt709_fullrange_to_rgb',
    (T.COLORSPACE.BT709_FULLRANGE, T.COLORSPACE.BGR): 'yuv_bt709_fullrange_to_bgr',
    (T.COLORSPACE.BT709_VIDEORANGE, T.COLORSPACE.RGB): 'yuv_bt709_videorange_to_rgb',
    (T.COLORSPACE.BT709_VIDEORANGE, T.COLORSPACE.BGR): 'yuv_bt709_videorange_to_bgr',
}


#!<-----------------------------------------------------------------------------
#!< FUNCTIONAL
#!<-----------------------------------------------------------------------------


@T.MetaWrapper()
def to_float(metas: Sequence[T.MetaBase], **kwargs):
  for meta in metas:
    if isinstance(meta, T.ImageMeta):
      if meta.source == T.COLORSPACE.HEATMAP:
        continue
      meta.bin = meta.bin.astype('float32')
  return metas


@T.MetaWrapper()
def to_tensor(metas: Sequence[T.MetaBase], scale=None, mean=None, std=None, **kwargs):
  r"""to tensor: (x / scale - mean) / std and from HWC to CHW

  Args:
    scale (float):
    mean list (float):
    std list (float):

  """
  mean = torch.tensor(mean) if mean is not None else None
  std = torch.tensor(std) if std is not None else None

  for meta in metas:

    if meta.source == T.COLORSPACE.HEATMAP:
      meta.bin = torch.from_numpy(meta.bin)
      continue

    if isinstance(meta, T.ImageMeta):
      # for image
      if meta.bin.ndim == 3:
        m = torch.from_numpy(np.ascontiguousarray(meta.bin.transpose((2, 0, 1))))  # nopep8
      elif meta.bin.ndim == 2:
        m = torch.from_numpy(meta.bin)[None]
      else:
        raise NotImplementedError(meta.bin.ndim)

      m = m.type(torch.FloatTensor)
      if scale is not None:
        m = m.float().div(scale)
      if mean is not None:
        m.sub_(mean[:, None, None])
      if std is not None:
        m.div_(std[:, None, None])
      meta.bin = m

    if isinstance(meta, T.VideoMeta):
      # for image
      if meta.bin.ndim == 4:
        m = torch.from_numpy(np.ascontiguousarray(meta.bin.transpose((3, 0, 1, 2))))  # nopep8
      else:
        raise NotImplementedError(meta.bin.ndim)

      m = m.type(torch.FloatTensor)
      if scale is not None:
        m = m.float().div(scale)
      if mean is not None:
        m.sub_(mean[:, None, None, None])
      if std is not None:
        m.div_(std[:, None, None, None])
      meta.bin = m

  return metas


#!<-----------------------------------------------------------------------------
#!< NORMALIZE
#!<-----------------------------------------------------------------------------

@T.MetaWrapper(support=[T.ImageMeta])
def equal_hist(metas: Sequence[T.MetaBase], **kwargs):
  r"""Equalize the image histogram.
  """
  for meta in sample:

    if meta.source in [T.COLORSPACE.HEATMAP]:
      continue

    if isinstance(meta, T.ImageMeta):
      ori_type = meta.bin.dtype
      meta.bin = meta.bin.astype('uint8')
      for c in range(meta.c):

        img = meta.bin[..., c]
        histogram = cv2.calcHist([img], [0], None, [256], (0, 256)).ravel()
        h = [_f for _f in histogram if _f]
        if len(h) <= 1:
          return img.copy()
        step = np.sum(h[:-1]) // 255
        if not step:
          return img.copy()
        lut = np.empty(256, dtype=np.uint8)
        n = step // 2
        for i in range(256):
          lut[i] = min(n // step, 255)
          n += histogram[i]
        meta.bin[..., c] = cv2.LUT(img, np.array(lut))
      meta.bin = meta.bin.astype(ori_type)

  return metas


@T.MetaWrapper(support=[T.ImageMeta, T.VideoMeta])
def truncated_standardize(metas: Sequence[T.MetaBase], **kwargs):
  r"""truncated standardize from TensorFlow
  """
  for meta in sample:

    if meta.source == T.COLORSPACE.HEATMAP:
      continue

    if isinstance(meta, T.ImageMeta):
      if meta.bin.ndim == 3:
        h, w, c = meta.bin.shape
      elif meta.bin.ndim == 2:
        h, w = meta.bin.shape
        c = 1
      else:
        raise NotImplementedError(meta.bin.ndim)
      meta.bin = meta.bin.astype('float32')
      min_std = 1.0 / math.sqrt(float(h * w * c))
      adjust_std = max(np.std(meta.bin), min_std)
      meta.bin = (meta.bin - np.mean(meta.bin)) / adjust_std

    if isinstance(meta, T.VideoMeta):
      if meta.bin.ndim == 4:
        n, h, w, c = meta.bin.shape
      else:
        raise NotImplementedError(meta.bin.ndim)
      meta.bin = meta.bin.astype('float32')
      meta_bins = []
      for i in range(n):
        meta_bin = meta.bin[i]
        min_std = 1.0 / math.sqrt(float(h * w * c))
        adjust_std = max(np.std(meta_bin), min_std)
        meta_bin = (meta_bin - np.mean(meta_bin)) / adjust_std
        meta_bins.append(meta_bin)
      meta.bin = np.array(meta_bins)

  return metas


#!<-----------------------------------------------------------------------------
#!< COLORSPACE
#!<-----------------------------------------------------------------------------


def _rgb_to_yuv_bt709_videorange(image: np.array, is_bgr=False):
  if is_bgr:
    B, G, R = np.split(image, 3, axis=2)
  else:
    R, G, B = np.split(image, 3, axis=2)

  Y = 0.1826 * R + 0.6142 * G + 0.0620 * B + 16  # [16, 235]
  U = -0.1007 * R - 0.3385 * G + 0.4392 * B + 128  # [16, 240]
  V = 0.4392 * R - 0.3990 * G - 0.0402 * B + 128  # [16, 240]

  yuv_image = np.concatenate([Y, U, V], axis=2)
  return yuv_image


def _rgb_to_yuv_bt709_fullrange(image: np.array, is_bgr=False):
  if is_bgr:
    B, G, R = np.split(image, 3, axis=2)
  else:
    R, G, B = np.split(image, 3, axis=2)

  Y = 0.2126 * R + 0.7152 * G + 0.0722 * B  # [0, 255]
  U = -0.1146 * R - 0.3854 * G + 0.5000 * B + 128  # [0, 255]
  V = 0.5000 * R - 0.4542 * G - 0.0468 * B + 128  # [0, 255]

  yuv_image = np.concatenate([Y, U, V], axis=2)
  return yuv_image


def _yuv_bt709_videorange_to_rgb(image: np.array, is_bgr=False):
  Y, U, V = np.split(image, 3, axis=2)

  Y = Y - 16
  U = U - 128
  V = V - 128

  R = 1.1644 * Y + 1.7927 * V
  G = 1.1644 * Y - 0.2132 * U - 0.5329 * V
  B = 1.1644 * Y + 2.1124 * U

  if is_bgr:
    return np.concatenate([B, G, R], axis=2)
  else:
    return np.concatenate([R, G, B], axis=2)


def _yuv_bt709_fullrange_to_rgb(image: np.array, is_bgr=False):
  Y, U, V = np.split(image, 3, axis=2)

  Y = Y
  U = U - 128
  V = V - 128

  R = 1.000 * Y + 1.570 * V
  G = 1.000 * Y - 0.187 * U - 0.467 * V
  B = 1.000 * Y + 1.856 * U

  if is_bgr:
    return np.concatenate([B, G, R], axis=2)
  else:
    return np.concatenate([R, G, B], axis=2)


def _change_colorspace(image: np.array, code=cv2.COLOR_BGR2RGB):
  if code == 'rgb_to_yuv_bt709_fullrange':
    return _rgb_to_yuv_bt709_fullrange(image, is_bgr=False)
  elif code == 'bgr_to_yuv_bt709_fullrange':
    return _rgb_to_yuv_bt709_fullrange(image, is_bgr=True)
  elif code == 'rgb_to_yuv_bt709_videorange':
    return _rgb_to_yuv_bt709_videorange(image, is_bgr=False)
  elif code == 'bgr_to_yuv_bt709_videorange':
    return _rgb_to_yuv_bt709_videorange(image, is_bgr=True)
  elif code == 'yuv_bt709_fullrange_to_rgb':
    return _yuv_bt709_fullrange_to_rgb(image, is_bgr=False)
  elif code == 'yuv_bt709_fullrange_to_bgr':
    return _yuv_bt709_fullrange_to_rgb(image, is_bgr=True)
  elif code == 'yuv_bt709_videorange_to_rgb':
    return _yuv_bt709_videorange_to_rgb(image, is_bgr=False)
  elif code == 'yuv_bt709_videorange_to_bgr':
    return _yuv_bt709_videorange_to_rgb(image, is_bgr=True)
  return cv2.cvtColor(image, code)


@T.MetaWrapper(support=[T.ImageMeta, T.VideoMeta, T.BoxListMeta, T.KpsListMeta])
def change_colorspace(metas: Sequence[T.MetaBase], src: T.COLORSPACE, dst: T.COLORSPACE, **kwargs):

  assert isinstance(src, T.COLORSPACE)
  assert isinstance(dst, T.COLORSPACE)
  code = _colorspace_mapping[(src, dst)]

  for meta in metas:

    if meta.source in [T.COLORSPACE.HEATMAP]:
      continue

    if isinstance(meta, T.ImageMeta):
      meta.bin = _change_colorspace(meta.bin, code)
      meta.source = dst

    if isinstance(meta, T.VideoMeta):
      for i in range(meta.n):
        meta.bin[i] = _change_colorspace(meta.bin[i], code)

  return metas


@T.MetaWrapper(support=[T.ImageMeta, T.VideoMeta, T.BoxListMeta, T.KpsListMeta])
def color_bgr2rgb(metas: Sequence[T.MetaBase], **kwargs):
  return change_colorspace(metas, T.COLORSPACE.BGR, T.COLORSPACE.RGB, **kwargs)


@T.MetaWrapper(support=[T.ImageMeta, T.VideoMeta, T.BoxListMeta, T.KpsListMeta])
def color_rgb2bgr(metas: Sequence[T.MetaBase], **kwargs):
  return change_colorspace(metas, T.COLORSPACE.RGB, T.COLORSPACE.BGR, **kwargs)


@T.MetaWrapper(support=[T.ImageMeta, T.VideoMeta, T.BoxListMeta, T.KpsListMeta])
def color_bgr2gray(metas: Sequence[T.MetaBase], **kwargs):
  return change_colorspace(metas, T.COLORSPACE.BGR, T.COLORSPACE.GRAY, **kwargs)


@T.MetaWrapper(support=[T.ImageMeta, T.VideoMeta, T.BoxListMeta, T.KpsListMeta])
def color_rgb2gray(metas: Sequence[T.MetaBase], **kwargs):
  return change_colorspace(metas, T.COLORSPACE.RGB, T.COLORSPACE.GRAY, **kwargs)

#!<-----------------------------------------------------------------------------
#!< NOISE
#!<-----------------------------------------------------------------------------


@T.MetaWrapper(support=[T.ImageMeta])
def random_iso_noise(metas: Sequence[T.MetaBase], color_shift=0.05, intensity=0.5, **kwargs):
  r"""Apply poisson noise to image to simulate camera sensor noise.

  Args:
    color_shift (float):
    intensity (float): Multiplication factor for noise values.
      Values of ~0.5 are produce noticeable, yet acceptable level of noise.

  """
  random_state = np.random.RandomState()

  for meta in metas:

    if meta.source == T.COLORSPACE.HEATMAP:
      continue

    if isinstance(meta, T.ImageMeta):

      image = meta.bin.astype('float32') / 255.

      hls = cv2.cvtColor(image, cv2.COLOR_RGB2HLS)

      mean, stddev = cv2.meanStdDev(hls)

      luminance_noise = random_state.poisson(stddev[1] * intensity * 255, size=hls.shape[:2])  # nopep8
      color_noise = random_state.normal(0, color_shift * 360 * intensity, size=hls.shape[:2])  # nopep8

      hue = hls[..., 0]
      hue += color_noise
      hue[hue < 0] += 360
      hue[hue > 360] -= 360

      luminance = hls[..., 1]
      luminance += (luminance_noise / 255) * (1.0 - luminance)

      image = cv2.cvtColor(hls, cv2.COLOR_HLS2RGB) * 255
      meta.bin = image

  return metas


@T.MetaWrapper(support=[T.ImageMeta])
def random_gaussian_blur(metas: Sequence[T.MetaBase], ksize_limit=(3, 7), sigma_limit=(0, 1.5), **kwargs):
  r"""Blur the input image using using a Gaussian filter with a random kernel size.

  Args:
    ksize_limit: maximum Gaussian kernel size for blurring the input image.
    sigma_limit: Gaussian kernel standard deviation.

  """
  assert isinstance(ksize_limit, tuple), ksize_limit
  assert isinstance(sigma_limit, tuple), sigma_limit

  ks_t = random.choice(np.arange(ksize_limit[0], ksize_limit[1] + 1, 2))
  sigma_t = random.uniform(*sigma_limit)

  for meta in metas:

    if meta.source == T.COLORSPACE.HEATMAP:
      continue

    if isinstance(meta, T.ImageMeta):
      meta.bin = cv2.GaussianBlur(meta.bin, ksize=(ks_t, ks_t), sigmaX=sigma_t)

  return metas


@T.MetaWrapper(support=[T.ImageMeta])
def random_gaussian_noise(metas: Sequence[T.MetaBase], var_limit=(10.0, 50.0), mean=0.0, **kwargs):
  r"""Apply gaussian noise to the input image."""
  assert isinstance(var_limit, tuple), var_limit

  var = random.uniform(*var_limit)
  sigma = var ** 0.5
  random_state = np.random.RandomState()

  for meta in metas:

    if meta.source == T.COLORSPACE.HEATMAP:
      continue

    if isinstance(meta, T.ImageMeta):
      gauss = random_state.normal(mean, sigma, meta.bin.shape)
      meta.bin = (meta.bin + gauss).clip(0, 255)

  return metas


@T.MetaWrapper(support=[T.ImageMeta])
def random_motion_blur(metas: Sequence[T.MetaBase], **kwargs):
  r"""Apply motion blur to the input image using a random-sized kernel."""

  ksize = random.choice(np.arange(3, 8, 2))
  kernel = np.zeros((ksize, ksize), dtype=np.uint8)
  xs, xe = random.randint(0, ksize - 1), random.randint(0, ksize - 1)
  if xs == xe:
    ys, ye = random.sample(range(ksize), 2)
  else:
    ys, ye = random.randint(0, ksize - 1), random.randint(0, ksize - 1)
  cv2.line(kernel, (xs, ys), (xe, ye), 1, thickness=1)
  kernel = kernel.astype(np.float32) / np.sum(kernel)  # normalize kernel

  for meta in metas:

    if meta.source == T.COLORSPACE.HEATMAP:
      continue

    if isinstance(meta, T.ImageMeta):
      meta.bin = cv2.filter2D(meta.bin, ddepth=-1, kernel=kernel)

  return metas


@T.MetaWrapper(support=[T.ImageMeta])
def random_median_blur(metas: Sequence[T.MetaBase]):
  r"""Blur the input image using using a median filter with a random aperture linear size."""

  ksize = random.choice(np.arange(3, 8, 2))

  for meta in metas:
    if meta.source == T.COLORSPACE.HEATMAP:
      continue

    if isinstance(meta, T.ImageMeta):
      curr_dtype = meta.bin.dtype
      meta.bin = cv2.medianBlur(meta.bin.astype('uint8'), ksize=ksize).astype(curr_dtype)

  return metas


#!<-----------------------------------------------------------------------------
#!< MORPHOLOGY
#!<-----------------------------------------------------------------------------


def _alpha_to_trimap(alpha: np.array, erode_step=10, dilate_step=10, **kwargs):
  alpha = alpha.astype('uint8')
  fg_mask = np.array(np.equal(alpha, 255).astype(np.float32))
  unknown = np.array(np.not_equal(alpha, 0).astype(np.float32))
  kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
  fg_mask = cv2.erode(fg_mask, kernel, erode_step)
  unknown = cv2.dilate(unknown, kernel, dilate_step)
  trimap = fg_mask * 255 + (unknown - fg_mask) * 128
  return trimap


@T.MetaWrapper(support=[T.ImageMeta])
def alpha_to_trimap(metas: Sequence[T.MetaBase], erode_step=10, dilate_step=10, **kwargs):

  for meta in metas:

    if meta.source != T.COLORSPACE.HEATMAP:
      continue

    if isinstance(meta, T.ImageMeta):
      assert meta.bin.ndim == 2, "Require input is a HxW heatmap."
      meta.bin = _alpha_to_trimap(meta.bin.astype('uint8'),
                                  erode_step=erode_step,
                                  dilate_step=dilate_step)

  return metas


@T.MetaWrapper(support=[T.ImageMeta])
def random_alpha_to_trimap(metas: Sequence[T.MetaBase], erode_steps=[1, 20], dilate_steps=[1, 20], **kwargs):
  erode_step = random.randint(erode_steps[0], erode_steps[1])
  dilate_step = random.randint(dilate_steps[0], dilate_steps[1])
  return alpha_to_trimap(metas, erode_step=erode_step, dilate_step=dilate_step, **kwargs)


#!<-----------------------------------------------------------------------------
#!< GEOMETRY
#!<-----------------------------------------------------------------------------

def _padding_to_size_divisible(image_list, size_divisible=32):
  r"""padding images in a batch to be divisible

  Args:
    image_list list[nd.array]:
    size_divisible: padding to divisible image list

  Returns:
    image_list nd.array[N, C, H, W]

  """
  max_size = list(max(s) for s in zip(*[img.shape for img in image_list]))
  max_size[1] = int(math.ceil(max_size[1] / size_divisible) * size_divisible)
  max_size[2] = int(math.ceil(max_size[2] / size_divisible) * size_divisible)
  max_size = tuple(max_size)
  batch_shape = (len(image_list),) + max_size
  batched_imgs = image_list[0].new(*batch_shape).zero_()
  for img, pad_img in zip(image_list, batched_imgs):
    pad_img[: img.shape[0], : img.shape[1], : img.shape[2]].copy_(img)
  return batched_imgs


@T.MetaWrapper(support=[T.ImageMeta, T.BoxListMeta, T.KpsListMeta])
def pad(metas: Sequence[T.MetaBase], left, top, right, bottom, fill_value=0):
  r"""pad space around sample.
  """
  for meta in metas:

    if isinstance(meta, T.ImageMeta):
      h, w, c = meta.bin.shape
      new_w = left + w + right
      new_h = top + h + bottom
      img = np.ones(shape=[new_h, new_w, c], dtype=meta.bin.dtype) * fill_value
      img[top:top+h, left:left+w, :] = meta.bin
      meta.bin = img

    if isinstance(meta, T.BoxListMeta):
      assert meta.is_affine_size
      meta.bboxes += [left, top, left, top]
      width = meta.max_x + left + right
      height = meta.max_y + top + bottom
      meta.set_affine_size(height, width)
      meta.clip_with_affine_size()

    if isinstance(meta, T.KpsListMeta):
      assert meta.is_affine_size
      meta.keypoints += [left, top]
      width = meta.max_x + left + right
      height = meta.max_y + top + bottom
      meta.set_affine_size(height, width)
      meta.clip_with_affine_size()

  return metas


@T.MetaWrapper(support=[T.ImageMeta, T.VideoMeta, T.BoxListMeta, T.KpsListMeta])
def vflip(metas: Sequence[T.MetaBase]):
  r"""vflip sample."""

  for meta in metas:

    if isinstance(meta, T.ImageMeta):
      meta.bin = np.ascontiguousarray(meta.bin[::-1, ...])

    if isinstance(meta, T.VideoMeta):
      meta.bin = np.ascontiguousarray(meta.bin[:, ::-1, ...])

    if isinstance(meta, T.BoxListMeta):
      assert meta.is_affine_size
      x1, y1 = meta.bboxes[..., 0], meta.bboxes[..., 1]
      x2, y2 = meta.bboxes[..., 2], meta.bboxes[..., 3]
      meta.bboxes = np.stack([x1, meta.max_y - y2, x2, meta.max_y - y1], axis=1)

    if isinstance(meta, T.KpsListMeta):
      assert meta.is_affine_size
      x, y = meta.keypoints[..., 0], meta.keypoints[..., 1]
      meta.keypoints = np.stack([x, meta.max_y - y], axis=1)

  return metas


@T.MetaWrapper(support=[T.ImageMeta, T.BoxListMeta, T.VideoMeta, T.KpsListMeta])
def hflip(metas: Sequence[T.MetaBase]):
  r"""hflip sample.

  Args:
    p (float): the possibility to flip

  """
  for meta in metas:

    if isinstance(meta, T.ImageMeta):
      meta.bin = np.ascontiguousarray(meta.bin[:, ::-1, ...])

    if isinstance(meta, T.BoxListMeta):
      assert meta.is_affine_size
      x1, y1 = meta.bboxes[..., 0], meta.bboxes[..., 1]
      x2, y2 = meta.bboxes[..., 2], meta.bboxes[..., 3]
      meta.bboxes = np.stack([meta.max_x - x2, y1, meta.max_x - x1, y2], axis=1)

    if isinstance(meta, T.VideoMeta):
      meta.bin = np.ascontiguousarray(meta.bin[:, :, ::-1, ...])

    if isinstance(meta, T.KpsListMeta):
      assert meta.is_affine_size
      x, y = meta.keypoints[..., 0], meta.keypoints[..., 1]
      meta.keypoints = np.stack([meta.max_x - x, y], axis=1)

  return metas


@T.MetaWrapper(support=[T.ImageMeta, T.VideoMeta, T.BoxListMeta, T.KpsListMeta])
def random_vflip(metas: Sequence[T.MetaBase], p=0.5):
  r"""random vertical flip sample.

  Args:
    p (float): the possibility to flip

  """
  if random.random() > p:
    return vflip(metas)
  return metas


@T.MetaWrapper(support=[T.ImageMeta, T.BoxListMeta, T.VideoMeta, T.KpsListMeta])
def random_hflip(metas: Sequence[T.MetaBase], p=0.5):
  r"""random horizontal flip sample.

  Args:
    p (float): the possibility to flip

  """
  if random.random() > p:
    return hflip(metas)
  return metas


@T.MetaWrapper(support=[T.ImageMeta, T.BoxListMeta, T.VideoMeta, T.KpsListMeta])
def random_crop(metas: Sequence[T.MetaBase], width, height):
  r"""random crop, reuqire width and height less than image

    Args:
      width (int or float): output width, or keep ratio (0 ~ 1)
      height (int or float): output height, or keep ratio (0 ~ 1)
  """

  def _get_crop_coords(img_h, img_w, crop_h, crop_w, rh, rw):
    y1 = int((img_h - crop_h) * rh)
    y2 = y1 + crop_h
    x1 = int((img_w - crop_w) * rw)
    x2 = x1 + crop_w
    return x1, y1, x2, y2

  # random
  rh = random.random()
  rw = random.random()

  for meta in metas:

    if isinstance(meta, T.ImageMeta):
      h, w = meta.bin.shape[:2]
      new_width = int(w * width) if width < 1 else width
      new_height = int(h * height) if height < 1 else height
      x1, y1, x2, y2 = _get_crop_coords(h, w, new_height, new_width, rh, rw)
      meta.bin = meta.bin[y1:y2, x1:x2]

    if isinstance(meta, T.VideoMeta):
      h, w = meta.bin.shape[1:3]
      new_width = int(w * width) if width < 1 else width
      new_height = int(h * height) if height < 1 else height
      x1, y1, x2, y2 = _get_crop_coords(h, w, new_height, new_width, rh, rw)
      meta.bin = meta.bin[:, y1:y2, x1:x2]

    if isinstance(meta, T.BoxListMeta):
      assert meta.is_affine_size
      new_width = int(meta.max_x * width) if width < 1 else width
      new_height = int(meta.max_y * height) if height < 1 else height
      x1, y1, x2, y2 = _get_crop_coords(meta.max_y, meta.max_x, new_height, new_width, rh, rw)
      meta.bboxes -= [x1, y1, x1, y1]
      meta.set_affine_size(new_height, new_width)
      meta.clip_with_affine_size()

    if isinstance(meta, T.KpsListMeta):
      assert meta.is_affine_size
      new_width = int(meta.max_x * width) if width < 1 else width
      new_height = int(meta.max_y * height) if height < 1 else height
      x1, y1, x2, y2 = _get_crop_coords(meta.max_y, meta.max_x, new_width, new_height, rh, rw)
      meta.keypoints -= [x1, y1]
      meta.set_affine_size(y2, x2)
      meta.clip_with_affine_size()

  return metas


@T.MetaWrapper(support=[T.ImageMeta, T.BoxListMeta, T.VideoMeta, T.KpsListMeta])
def center_crop(metas: Sequence[T.MetaBase], height, width):
  r"""center crop

  Args:
    width (int): output width
    height (int): output height

  """
  def _get_crop_coords(height, width, crop_height, crop_width):
    y1 = (height - crop_height) // 2
    y2 = y1 + crop_height
    x1 = (width - crop_width) // 2
    x2 = x1 + crop_width
    return x1, y1, x2, y2

  for meta in metas:

    if isinstance(meta, T.ImageMeta):
      h, w = meta.bin.shape[:2]
      x1, y1, x2, y2 = _get_crop_coords(h, w, width, height)
      meta.bin = meta.bin[y1:y2, x1:x2]

    if isinstance(meta, T.VideoMeta):
      h, w = meta.bin.shape[1:3]
      x1, y1, x2, y2 = _get_crop_coords(h, w, width, height)
      meta.bin = meta.bin[:, y1:y2, x1:x2]

    if isinstance(meta, T.BoxListMeta):
      assert meta.is_affine_size
      x1, y1, x2, y2 = _get_crop_coords(meta.max_y, meta.max_x, width, height)
      meta.bboxes -= [x1, y1, x1, y1]
      meta.set_affine_size(height, width)
      meta.clip_with_affine_size()

    if isinstance(meta, T.KpsListMeta):
      assert meta.is_affine_size
      x1, y1, x2, y2 = _get_crop_coords(meta.max_y, meta.max_x, width, height)
      meta.keypoints -= [x1, y1]
      meta.set_affine_size(y2, x2)
      meta.clip_with_affine_size()

  return metas


@T.MetaWrapper(support=[T.ImageMeta, T.BoxListMeta, T.KpsListMeta])
def shortside_resize(metas: Sequence[T.MetaBase], min_size=256, interpolation=cv2.INTER_LINEAR):
  r"""shortside resize

  Args:
    min_size (int): image will aspect resize according to short side size 

  """
  def _get_new_shape(h, w, min_size):
    if (w <= h and w == min_size) or (h <= w and h == min_size):
      ow, oh = w, h
    # resize
    if w < h:
      ow = min_size
      oh = int(min_size * h / w)
    else:
      oh = min_size
      ow = int(min_size * w / h)
    return oh, ow

  for meta in metas:
    if meta.source == T.COLORSPACE.HEATMAP:
      interpolation = cv2.INTER_NEAREST

    if isinstance(meta, T.ImageMeta):
      h, w = meta.bin.shape[:2]
      oh, ow = _get_new_shape(h, w, min_size)
      meta.bin = cv2.resize(meta.bin, dsize=(ow, oh), interpolation=interpolation)

    if isinstance(meta, T.BoxListMeta):
      assert meta.is_affine_size
      oh, ow = _get_new_shape(meta.max_y, meta.max_x, min_size)
      scale_w = float(ow) / meta.max_x
      scale_h = float(oh) / meta.max_y
      meta.bboxes *= [scale_w, scale_h, scale_w, scale_h]
      meta.set_affine_size(oh, ow)

    if isinstance(meta, T.KpsListMeta):
      assert meta.is_affine_size
      oh, ow = _get_new_shape(meta.max_y, meta.max_x, min_size)
      scale_w = float(ow) / meta.max_x
      scale_h = float(oh) / meta.max_y
      meta.keypoints *= [scale_w, scale_h]
      meta.set_affine_size(oh, ow)

  return metas


@T.MetaWrapper(support=[T.ImageMeta, T.BoxListMeta, T.VideoMeta, T.KpsListMeta])
def resize(metas: Sequence[T.MetaBase], height, width, interpolation=cv2.INTER_LINEAR):
  r"""resize.

  Args:
    height (int):
    width (int):

  """
  for meta in metas:
    if meta.source == T.COLORSPACE.HEATMAP:
      interpolation = cv2.INTER_NEAREST

    if isinstance(meta, T.ImageMeta):
      meta.bin = cv2.resize(meta.bin, dsize=(width, height), interpolation=interpolation)

    if isinstance(meta, T.VideoMeta):
      meta.bin = np.array([cv2.resize(meta.bin[i], dsize=(width, height), interpolation=interpolation)
                           for i in range(meta.n)])

    if isinstance(meta, T.BoxListMeta):
      assert meta.is_affine_size
      scale_w = float(width) / meta.max_x
      scale_h = float(height) / meta.max_y
      meta.bboxes *= [scale_w, scale_h, scale_w, scale_h]
      meta.set_affine_size(height, width)

    if isinstance(meta, T.KpsListMeta):
      assert meta.is_affine_size
      scale_w = float(width) / meta.max_x
      scale_h = float(height) / meta.max_y
      meta.keypoints *= [scale_w, scale_h]
      meta.set_affine_size(height, width)

  return metas


@T.MetaWrapper(support=[T.ImageMeta, T.BoxListMeta, T.KpsListMeta])
def rotate(metas: Sequence[T.MetaBase], angle, interpolation=cv2.INTER_LINEAR, border_mode=cv2.BORDER_CONSTANT, border_value=0):
  r"""rotate.

  Args:
    angle (float): degree representation

  """
  scale = 1.0
  shift = (0, 0)

  # params checking
  assert len(shift) == 2

  for meta in metas:
    if meta.source == T.COLORSPACE.HEATMAP:
      interpolation = cv2.INTER_NEAREST

    if isinstance(meta, T.ImageMeta):
      height, width = meta.bin.shape[:2]
      matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, scale)
      matrix[0, 2] += shift[0]
      matrix[1, 2] += shift[1]
      cv2.warpAffine(meta.bin,
                     M=matrix,
                     dsize=(width, height),
                     dst=meta.bin,
                     flags=interpolation,
                     borderMode=border_mode,
                     borderValue=border_value)

    if isinstance(meta, T.BoxListMeta):
      width, height = meta.max_x, meta.max_y
      center = (width / 2, height / 2)
      matrix = cv2.getRotationMatrix2D(center, angle, scale)
      matrix[0, 2] += shift[0]
      matrix[1, 2] += shift[1]

      bbox = np.stack([meta.bboxes[:, 0], meta.bboxes[:, 1],
                       meta.bboxes[:, 2], meta.bboxes[:, 1],
                       meta.bboxes[:, 0], meta.bboxes[:, 3],
                       meta.bboxes[:, 2], meta.bboxes[:, 3]], axis=1).reshape(-1, 2)
      bbox = cv2.transform(bbox[None], matrix).squeeze().reshape(-1, 8)
      meta.bboxes = np.stack([
          np.amin(bbox[..., ::2], axis=1),
          np.amin(bbox[..., 1::2], axis=1),
          np.amax(bbox[..., ::2], axis=1),
          np.amax(bbox[..., 1::2], axis=1),
      ], axis=1)

      if meta.visibility:
        meta.clip_with_affine_size()

    if isinstance(meta, T.KpsListMeta):
      width, height = meta.max_x, meta.max_y
      center = (width / 2, height / 2)
      matrix = cv2.getRotationMatrix2D(center, angle, scale)
      matrix[0, 2] += shift[0]  # * width
      matrix[1, 2] += shift[1]  # * height
      meta.keypoints = cv2.transform(meta.keypoints[None], matrix).squeeze()
      if meta.visibility:
        meta.clip_with_affine_size()

  return metas


@T.MetaWrapper(support=[T.ImageMeta, T.BoxListMeta, T.KpsListMeta])
def random_rotate(metas: Sequence[T.MetaBase],
                  angle_limit=(-30, 30),
                  interpolation=cv2.INTER_LINEAR,
                  border_mode=cv2.BORDER_CONSTANT,
                  border_value=0,
                  **kwargs):
  r"""Random Rotate
  """
  angle = random.uniform(angle_limit[0], angle_limit[1])
  return rotate(metas, angle, interpolation, border_mode, border_value, **kwargs)  # nopep8
