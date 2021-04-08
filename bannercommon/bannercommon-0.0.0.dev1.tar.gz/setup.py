from setuptools import setup, find_packages
import pathlib


here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')


setup(
    name='bannercommon',
    version='0.0.0.dev1',
    packages=['bannercommon'],
    python_requires='>=3.6, <4',
    long_description=long_description,
    long_description_content_type='text/markdown',
)
