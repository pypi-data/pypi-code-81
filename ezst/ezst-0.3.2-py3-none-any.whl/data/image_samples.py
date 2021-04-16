import os
import zipfile
import requests

base_dir = 'image_samples'

def load():
  save_path = './image_samples.zip'
  url = 'https://www.dropbox.com/s/eyzdqs8dlr5mp2r/image_samples.zip?dl=1'
  r = requests.get(url, stream=True)
  with open(save_path, 'wb') as fd:
      for chunk in r.iter_content(chunk_size=128):
          fd.write(chunk)

  local_zip = 'image_samples.zip'

  zip_ref = zipfile.ZipFile(local_zip, 'r')

  zip_ref.extractall('./')
  zip_ref.close()

  os.remove("image_samples.zip")

    