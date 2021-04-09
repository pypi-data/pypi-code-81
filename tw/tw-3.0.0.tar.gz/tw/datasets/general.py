# Copyright 2021 The KaiJIN Authors. All Rights Reserved.
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
r"""General datasets for common tasks.
"""
import os
import random
import torch
import tw
import tw.transform as T

#!<----------------------------------------------------------------------------
#!< General Datasets for Classification or Regression
#!<----------------------------------------------------------------------------


class ImageLabel(torch.utils.data.Dataset):

  r"""ImageLabel dataset"""

  def __init__(self, path, label_type, transform, **kwargs):
    # check
    assert label_type in [float, int]
    tw.fs.raise_path_not_exist(path)

    # parse
    res, _ = tw.parser.parse_from_text(path, [str, label_type], [True, False])
    self.targets = []
    for path, label in zip(res[0], res[1]):
      self.targets.append((path, label))

    self.transform = transform
    tw.logger.info(f'Totally loading {len(self.targets)} samples.')

  def __len__(self):
    return len(self.targets)

  def __getitem__(self, idx):
    img_meta = T.ImageMeta(path=self.targets[idx][0])
    img_meta.label = self.targets[idx][1]
    img_meta.load().numpy()
    return self.transform([img_meta])


#!<----------------------------------------------------------------------------
#!< General Datasets for Salient Detection
#!<----------------------------------------------------------------------------

class ImageSalientDet(torch.utils.data.Dataset):

  r"""SalientDet dataset

  Format:
    1. Image: [0, 255] BGR -> float -> [0, 1.0]
    2. Mask: [0, 255] BGR -> float -> [0, 1.0]

  """

  def __init__(self, path, transform, **kwargs):
    # check
    tw.fs.raise_path_not_exist(path)

    res, _ = tw.parser.parse_from_text(path, [str, str], [True, True])  # nopep8
    self.targets = []
    for img_path, mask_path in zip(res[0], res[1]):
      self.targets.append((img_path, mask_path))

    self.transform = transform
    tw.logger.info('Totally loading %d samples.' % len(self.targets))

  def __len__(self):
    return len(self.targets)

  def __getitem__(self, idx):
    # load image
    img_meta = T.ImageMeta(path=self.targets[idx][0])
    img_meta.label = self.targets[idx][1]
    img_meta.load().numpy()
    # load mask
    mask_meta = T.ImageMeta(path=self.targets[idx][1])
    mask_meta.load().numpy()
    return self.transform([img_meta, mask_meta])


#!<----------------------------------------------------------------------------
#!< General Datasets for Image Enhancement
#!<----------------------------------------------------------------------------

class ImageEnhance(torch.utils.data.Dataset):

  r"""General Image Enhancement: image to image translation

    e.g. super resolution, denoise, sharpeness

  Format:
    input_image_path augmented_image_path

  """

  def __init__(self, path, transform, **kwargs):
    # check
    tw.fs.raise_path_not_exist(path)
    res, _ = tw.parser.parse_from_text(path, [str, str], [True, True])  # nopep8

    self.targets = []
    for img_path, enhance_path in zip(res[0], res[1]):
      self.targets.append((img_path, enhance_path))

    self.transform = transform
    tw.logger.info('Totally loading %d samples.' % len(self.targets))

  def __len__(self):
    return len(self.targets)

  def __getitem__(self, idx):
    # load image
    img_meta = T.ImageMeta(path=self.targets[idx][0])
    img_meta.load().numpy()
    # load enhance
    enhance_meta = T.ImageMeta(path=self.targets[idx][1])
    enhance_meta.load().numpy()
    return self.transform([img_meta, enhance_meta])


class ImageFolderEnhance(torch.utils.data.Dataset):

  r"""General Image Folder Enhancement: image to image translation

    e.g. super resolution, denoise, sharpeness

  Format:
    input_image_folder augmented_image_folder

  """

  def __init__(self, path, transform, **kwargs):
    # check
    tw.fs.raise_path_not_exist(path)
    res, _ = tw.parser.parse_from_text(path, [str, str], [True, True])  # nopep8

    self.targets = []
    total_img = 0
    for _, (image_folder, enhance_folder) in enumerate(zip(*res)):
      self.targets.append((
          [os.path.join(image_folder, f) for f in sorted(os.listdir(image_folder))],
          [os.path.join(enhance_folder, f) for f in sorted(os.listdir(enhance_folder))],
      ))
      total_img += len(self.targets[-1][0])

    self.transform = transform
    tw.logger.info(f'num of folder: {len(self)}, num of image: {total_img}.')

  def __len__(self):
    return len(self.targets)

  def __getitem__(self, idx):
    # folder
    img, enh = self.targets[idx]
    assert len(img) <= len(enh), f"{len(img)} vs {len(enh)}."

    # fetch image
    i = random.randint(0, len(img) - 1)
    img_meta = T.ImageMeta(path=img[i], source=T.COLORSPACE.BGR)
    img_meta.load().numpy()
    enh_meta = T.ImageMeta(path=enh[i], source=T.COLORSPACE.BGR)
    enh_meta.load().numpy()

    return self.transform([img_meta, enh_meta])


class VideoFolderEnhance(torch.utils.data.Dataset):
  pass
