from setuptools import setup, find_packages
import codecs
import os
VERSION = '0.1'
DESCRIPTION = 'A simple save lib'

setup(
    name='savelib',
    version = VERSION,
    author='Yesnt',
    author_email='noemail@gmail.com',
    description = DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'save', 'file', 'savelib', 'simplesave'],
    classifiers=[
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
    ]
)
