from setuptools import setup, find_packages
import Sellix

Classifiers = [
  "Development Status :: 5 - Production/Stable",
  "Intended Audience :: Developers",
  "License :: OSI Approved :: MIT License",
  "Natural Language :: English",
  "Programming Language :: Python :: 3.8"
]

setup(
  name=Sellix.__Name__,
  version=Sellix.__Version__,
  description=Sellix.__Description__,
  long_description=open('README.md').read(),
  long_description_content_type="text/markdown",
  url=Sellix.__URL__,
  author=Sellix.__Author__,
  author_email=Sellix.__AuthorMail__,
  license=Sellix.__License__,
  classifiers=Classifiers,
  packages=find_packages(),
  keywords="Sellix",
  install_requires=["requests"]
)
