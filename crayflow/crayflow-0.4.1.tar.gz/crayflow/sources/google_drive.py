from ..meta import *
from .utils import ensure_directory

import os

__all__ = [
  'google_drive'
]

### Shamefully stolen from https://gist.github.com/charlesreid1/4f3d676b33b95fce83af08e4ec261822
### Author: https://gist.github.com/charlesreid1

def download_file_from_google_drive(id, destination):
  import requests
  def get_confirm_token(response):
    for key, value in response.cookies.items():
      if key.startswith('download_warning'):
        return value

    return None

  def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
      for chunk in response.iter_content(CHUNK_SIZE):
        if chunk: # filter out keep-alive new chunks
          f.write(chunk)

  URL = "https://docs.google.com/uc?export=download"

  session = requests.Session()

  response = session.get(URL, params = { 'id' : id }, stream = True)
  token = get_confirm_token(response)

  if token:
    params = { 'id' : id, 'confirm' : token }
    response = session.get(URL, params = params, stream = True)

  save_response_content(response, destination)
  return destination

class GoogleDrive(Stage):
  def __init__(self, path, id):
    self.id = id
    self.path = path
    
    super(GoogleDrive, self).__init__()

  def load(self, root=None):
    path = os.path.join(root, self.path)

    if os.path.exists(path):
      return path
    else:
      raise FileNotFoundError()

  def get_output_for(self, *args, root=None, warn=True):
    path = os.path.join(root, self.path)
    ensure_directory(os.path.dirname(path))

    if warn:
      import warnings
      warnings.warn('Downloading google drive doc %s to %s'% (self.id, path), )

    return download_file_from_google_drive(self.id, path)


google_drive = GoogleDrive