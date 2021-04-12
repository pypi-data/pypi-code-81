from distutils.core import setup
import setuptools

setup(
  name = 'necessity',
  packages = ['necessity'],
  version = '0.0.10',
  description = 'Bear necessity',
  long_description = 'Ale is my bear necessity.',
  author = '',
  url = 'https://github.com/alvations/necessity',
  keywords = [],
  classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  install_requires = ['pandas', 'tqdm', 'pyarrow'],
)
