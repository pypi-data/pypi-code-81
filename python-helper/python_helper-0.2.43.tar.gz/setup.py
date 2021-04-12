from distutils.core import setup
import os

OS_SEPARATOR = os.path.sep

version = '0.2.43'
name = 'python_helper'
url = f'https://github.com/SamuelJansen/{name}/'

setup(
    name = name,
    packages = [
        name,
        f'{name}{OS_SEPARATOR}api',
        f'{name}{OS_SEPARATOR}api{OS_SEPARATOR}src',
        f'{name}{OS_SEPARATOR}api{OS_SEPARATOR}src{OS_SEPARATOR}service',
        f'{name}{OS_SEPARATOR}api{OS_SEPARATOR}src{OS_SEPARATOR}domain',
        f'{name}{OS_SEPARATOR}api{OS_SEPARATOR}src{OS_SEPARATOR}helper',
        f'{name}{OS_SEPARATOR}api{OS_SEPARATOR}src{OS_SEPARATOR}annotation'
    ],
    version = version,
    license = 'MIT',
    description = 'python helper package',
    author = 'Samuel Jansen',
    author_email = 'samuel.jansenn@gmail.com',
    url = url,
    download_url = f'{url}archive/v{version}.tar.gz',
    keywords = ['helper', 'python helper package', 'python helper', 'helper package'],
    install_requires = [
        'colorama==0.4.3'
    ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9'
    ]
)
