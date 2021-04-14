from setuptools import setup, find_packages
import codecs
import os
from os import path

this_directory = path.abspath(path.dirname(__file__))
VERSION = '0.0.6'
DESCRIPTION = 'A basic unofficial batmanwonderwoman.com (bmww) api'
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Setting up
setup(
    name="bmww-api",
    version=VERSION,
    author="Noche-10",
    author_email="nocheffic@gmail.com",
    long_description=long_description,
    long_description_content_type = 'text/markdown',
    url='https://github.com/Noche-10/bmww-api',
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['beautifulsoup4', 'requests'],
    keywords=['python', 'api', 'batman', 'wonderwoman', 'bmww', 'batmanwonderwoman'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)
