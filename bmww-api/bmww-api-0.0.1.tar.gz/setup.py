from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'A basic unofficial batmanwonderwoman.com (bmww) api'

# Setting up
setup(
    name="bmww-api",
    version=VERSION,
    author="Noche-10",
    author_email="nocheffic@gmail.com",
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
