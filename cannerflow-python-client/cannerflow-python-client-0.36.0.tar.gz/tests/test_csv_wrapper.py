import os
from cannerflow.csv_wrapper import *

CURRENT_PATH = os.path.dirname(__file__)

NORMAL_CSV = os.path.join(CURRENT_PATH, 'normal.csv')
MBCS_CSV = os.path.join(CURRENT_PATH, 'mbcs.csv')

def test_csv_wrapper_utf8_bom():
  with open(NORMAL_CSV, 'rb') as f:
    content = f.read()
  csv_wrapper = CsvWrapper(content=content, encoding="utf-8-sig")
  csv = csv_wrapper.to_list()
  assert len(csv) > 0, "Should parse csv correctly"
  assert csv[0] == ['id', 'name'], "first row should be column name"


def test_csv_wrapper_mbcs():
  with open(MBCS_CSV, 'rb') as f:
    content = f.read()
  csv_wrapper = CsvWrapper(content=content, encoding="cp950")
  csv = csv_wrapper.to_pandas()
  assert len(csv) > 0, "Should parse csv correctly"

if __name__ == '__main__':
    test_csv_wrapper_utf8_bom()
    test_csv_wrapper_mbcs()
    print("Tests passed")