from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'ghostfn is very pog'

# Setting up
setup(
    name="ghostfn",
    version=VERSION,
    author="ghostleaks",
    author_email="2ghostleaks@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'stuff', 'ghostleaks', 'ghost', 'fortnite', 'lobbybot','ghostfn'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)