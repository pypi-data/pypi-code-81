from setuptools import setup
 
#reeee

with open("README.md", "r") as fh:
  long_description = fh.read()
setup(
  name = "balls",
  install_requires=[
    'requests'
  ],
  url = "https://github.com/ballsballsballsballsballsballsballsball/Balls",
  version = "0.0.1",
  description = "balls",
  long_description = long_description,
  long_description_content_type = "text/markdown",
  author = "ch1ck3n",
  author_email = "chcknch1ck3n@gmail.com",#email
#To find more licenses or classifiers go to: https://pypi.org/classifiers/
  license = "MIT",
  packages=['balls'],
  classifiers = [
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
  "Operating System :: OS Independent",
],
  zip_safe=True,
  python_requires = ">=3.0",
)
