import numpy as np

from ..sources import download

SUSY_URL = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00279/SUSY.csv.gz'
HIGGS_URL = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00280/HIGGS.csv.gz'


__all__ = [
  'download_susy', 'download_higgs',
  'read_susy', 'read_higgs',
]

download_susy = lambda path: lambda: download(path, SUSY_URL)
download_higgs = lambda path: lambda: download(path, HIGGS_URL)

def read_csv():
  def read(path):
    data = np.loadtxt(path, dtype='float32', delimiter=',')
    return data[:, 1:], data[:, 0]

  return read

read_higgs = read_csv
read_susy = read_csv