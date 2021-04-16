from distutils.core import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='PyEasyEmbed',
    version='0.1.2',
    description='Library to make command calls from other application of Python more easy',
    author='Christian Schweigel',
    author_email='',
    url='https://github.com/swip3798/PyEasyEmbed',
    packages=['EasyEmbed'],
    long_description = long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha"
    ],
)