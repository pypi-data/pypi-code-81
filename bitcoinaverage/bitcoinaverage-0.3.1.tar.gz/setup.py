try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from os import path
this_dir = path.abspath(path.dirname(__file__))
with open(path.join(this_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='bitcoinaverage',
    packages=['bitcoinaverage', # this must be the same as the name above
              'bitcoinaverage.clients',
              'bitcoinaverage.examples'],
    version='0.3.1',
    description='Library to integrate with the BitcoinAverage API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Blockchain Data LTD',
    author_email='info@bitcoinaverage.com',
    keywords=['bitcoinaverage', 'bitcoin', 'api'],  # arbitrary keywords
    classifiers=[],
    install_requires=[
        "requests",
        "six",
        "ws4py"
    ]
)
