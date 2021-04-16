import numpy as np

from ..sources import download

IMAGES_URL = 'https://github.com/brendenlake/omniglot/raw/master/python/images_background.zip'
TEST_IMAGES_URL = 'https://github.com/brendenlake/omniglot/raw/master/python/images_evaluation.zip'

__all__ = [
  'download_omniglot',
  'download_omniglot_test',

  'read_omniglot'
]

download_omniglot = lambda path: lambda: download(path, IMAGES_URL)
download_omniglot_test = lambda path: lambda: download(path, TEST_IMAGES_URL)

def read_omniglot(return_mapping=False):
  def read(path):
    from PIL import Image
    import zipfile as zip

    with zip.ZipFile(path, mode='r') as archive:
      files = [
        item
        for item in archive.namelist()
        if item.endswith('.png')
      ]

      files = sorted(files)

      alphabet_mapping = {}

      alphabets = np.ndarray(shape=(len(files), ), dtype='int32')
      characters = np.ndarray(shape=(len(files),), dtype='int32')

      imgs = None
      for i, item in enumerate(files):
        _, alphabet, character, _ = item.split('/')

        if alphabet not in alphabet_mapping:
          alphabet_mapping[alphabet] = len(alphabet_mapping)

        alphabets[i] = alphabet_mapping[alphabet]
        characters[i] = int(character.split('character')[-1]) - 1

        with archive.open(item, mode='r') as zip_f:
          with Image.open(zip_f) as img_f:
            img_f.load()
            img = np.asarray(img_f, dtype='uint8')

            if imgs is None:
              imgs = np.ndarray(shape=(len(files),) + img.shape, dtype='uint8')

            imgs[i] = 1 - img

      imgs = imgs.reshape(imgs.shape[:1] + (1, ) + imgs.shape[1:])

      if return_mapping:
        return imgs, alphabets, characters, alphabet_mapping
      else:
        return imgs, alphabets, characters

  return read