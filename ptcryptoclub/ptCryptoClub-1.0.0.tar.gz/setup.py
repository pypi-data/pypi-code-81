from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.0'
DESCRIPTION = 'Python SDK for ptcrypto.club'
LONG_DESCRIPTION = 'Project under development. In the meanwhile visit https://www.ptcrypto.club, ' \
                   'https://app.ptcrypto.club or https://iam.ptcrypto.club and become a member of our community.'

setup(
    name="ptCryptoClub",
    version=VERSION,
    author="Helder Cepeda",
    author_email="<helder_cepeda@hotmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'crypto', 'community', 'cryptocurrencies', 'bitcoin', 'ethereum'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3"
    ]
)
