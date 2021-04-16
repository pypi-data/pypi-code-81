import os
import re

import setuptools

with open(os.path.join("gicd", "__init__.py"), encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setuptools.setup(
    name='gicd',
    version=version,
    author='Zeke Marffy',
    author_email='zmarffy@yahoo.com',
    packages=setuptools.find_packages(),
    url='https://github.com/zmarffy/gicd',
    license='MIT',
    description='Python decorator that will automatcially create an issue on GitHub if a decorated function throws an exception',
    python_requires='>=3.6',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'zmtools'
    ],
)
