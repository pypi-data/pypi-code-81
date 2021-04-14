from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.3'
DESCRIPTION = 'A basic unofficial batmanwonderwoman.com (bmww) api'
long_description = "A basic bmww api, check github' readme for usage"

# Setting up
setup(
    name="bmww-api",
    version=VERSION,
    author="Noche-10",
    author_email="nocheffic@gmail.com",
    long_description=long_description,
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
