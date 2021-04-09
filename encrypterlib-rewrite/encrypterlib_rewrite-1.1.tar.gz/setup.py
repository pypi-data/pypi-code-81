from setuptools import setup, find_packages
import codecs
import os

name = "encrypterlib_rewrite"
version = "1.1"
author = "Coder436"
author_email = "<codergd@gmail.com>"
description = "An easy-to-use encryption package."
long_description_type = "text/markdown"
long_description = "A library that eases symmetric and asymmetric encryption."
packages = find_packages()
install_requires = ["cryptography"]
keywords = ["cryptography", "asymmetric encryption", "symmetric encryption", "openssl"]
classifiers = [
   "Development Status :: 4 - Beta",
   "Intended Audience :: Developers",
   "Programming Language :: Python :: 3",
   "Operating System :: Unix",
   "Operating System :: MacOS :: MacOS X",
   "Operating System :: Microsoft :: Windows",
]

# Setting up
# setup.py script is a modified version of the GitHub upload NeuralNine > vidstream > setup.py
setup(
    name = name,
    version = version,
    author = author,
    author_email = author_email,
    description = description,
    long_description_content_type = long_description_type,
    long_description = long_description,
    packages = packages,
    install_requires = install_requires,
    keywords = keywords,
    classifiers = classifiers
)