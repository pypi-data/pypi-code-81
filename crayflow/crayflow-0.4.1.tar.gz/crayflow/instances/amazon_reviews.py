from ..sources import download

__all__ = [
  'download_amazon_review_core5_data',
  'read_amazon_review_data'
]

AMAZON_REVIEWS_ROOT_URL = 'http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/'
CATEGORY_FILE = lambda category: 'reviews_%s_5.json.gz' % category

def read_amazon_review_data():
  def read(path):
    import gzip
    with gzip.open(path) as f:

      data = dict()
      for line in f:
        record = eval(line)

        rid = record['reviewerID']
        text = record['reviewText']
        summary = record['summary']
        label = record['overall']

        if rid not in data:
          data[rid] = []

        data[rid].append((summary, text, label))

    return list(data.values())

  return read

download_amazon_review_core5_data = lambda path, category: lambda: download(
  path, CATEGORY_FILE(category), root_url=AMAZON_REVIEWS_ROOT_URL
)