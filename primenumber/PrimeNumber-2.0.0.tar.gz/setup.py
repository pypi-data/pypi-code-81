from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '2.0.0'
DESCRIPTION = 'Working with prime numbers'
LONG_DESCRIPTION = 'A package that allows developers to: check if a number is prime, generate prime numbers, decompose any whole number ' \
                   ' as the product of prime numbers'

setup(
    name="PrimeNumber",
    version=VERSION,
    author="Helder Cepeda",
    author_email="<helder_cepeda@hotmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'prime', 'prime number', 'prime numbers', 'number', 'numbers'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3"
    ]
)
