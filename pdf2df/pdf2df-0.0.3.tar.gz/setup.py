from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

with open("README.md") as file:
    long_description = file.read()

VERSION = '0.0.3'
DESCRIPTION = 'Extract data from pdf to a dataframe'

# Setting up
setup(
    name="pdf2df",
    version=VERSION,
    author="Rohit Thakur",
    author_email="fordatascience12@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['fitz', 'pymupdf', 'pandas'],
    keywords=['python', 'pymupdf', 'extract pdf', 'extract text', 'dataframe'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)