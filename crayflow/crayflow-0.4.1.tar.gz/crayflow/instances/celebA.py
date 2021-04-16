import numpy as np

from ..sources import google_drive

__all__ = [
  'download_celebA',
  'download_celebA_attr',
  'download_celebA_indx',

  'read_celebA_images',
  'read_celebA_attributes',
  'read_celebA_index'
]

CELEBA_ID =      '0B7EVK8r0v71pZjFTYXZWM3FlRnM'
CELEBA_ATTR_ID = '0B7EVK8r0v71pblRyaVFSWGxPY0U'
CELEBA_INDX_ID = '1_ee_0u7vcNLOfNLegJRHmolfH5ICW-XS'

CELEBA_DIRECTORY = 'img_align_celeba'

CELEBA_NUM_ATTR = 40

def read_celebA_images(return_file_names=False):
  def read(path):
    from PIL import Image
    import zipfile

    with zipfile.ZipFile(path, mode='r') as archive:
      files = [
        item
        for item in archive.namelist()
        if item.endswith('.jpg')
      ]

      files = sorted(files)

      imgs = None
      for i, item in enumerate(files):
        with archive.open(item, mode='r') as zip_f:
          with Image.open(zip_f) as img_f:
            img_f.load()
            img = np.asarray(img_f, dtype='uint8')

            if imgs is None:
              imgs = np.ndarray(shape=(len(files), ) + img.shape, dtype='uint8')

            imgs[i] = img

    if return_file_names:
      return files, imgs
    else:
      return imgs

  return read

def read_celebA_attributes():
  def read(path):
    with open(path, 'r') as f:
      total = int(f.readline())
      results = np.ndarray(shape=(total, CELEBA_NUM_ATTR), dtype='uint8')
      attr_names = f.readline().split()

      for i, l in enumerate(f):
        results[i, :] = [ (1 if int(x) > 0 else 0) for x in l.split()[1:]]

      return attr_names, results

  return read

def read_celebA_index():
  def read(path):
    groups = dict()
    with open(path, 'r') as f:
      for line in f:
        file, group = line.split()
        group = int(group)

        if group not in groups:
          groups[group] = list()

        groups[group].append(int(file[:-4]) - 1)

    return list(groups.values())

  return read

download_celebA = lambda path: lambda: google_drive(path, CELEBA_ID)
download_celebA_attr = lambda path: lambda: google_drive(path, CELEBA_ATTR_ID)
download_celebA_indx = lambda path: lambda: google_drive(path, CELEBA_INDX_ID)




