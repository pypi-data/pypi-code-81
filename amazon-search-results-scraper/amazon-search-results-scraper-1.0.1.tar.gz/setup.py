import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
VERSION = '1.0.1'
PACKAGE_NAME = 'amazon-search-results-scraper'
AUTHOR = 'DataKund'
AUTHOR_EMAIL = 'datakund@gmail.com'
URL = 'https://amazon-api.datakund.com/en/latest/'
KEYWORDS='amazon python bot_studio scraper web-scraping product search-results search keyword'
LICENSE = 'Apache License 2.0'
DESCRIPTION = 'A python library to search keyword and scrape search results data from amazon.'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      'requests','bot-studio'
]

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages(),
      url=URL,
      keywords = KEYWORDS
      )