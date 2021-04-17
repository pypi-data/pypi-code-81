from io import open
import sys

from setuptools import find_packages, setup

with open('pipdownload/__init__.py', 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.strip().split('=')[1].strip(' \'"')
            break
    else:
        version = '0.0.1'

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

REQUIRES = [
    'click',
    'requests',
    'cachecontrol',
    'packaging',
    'retrying',
    'pip-api',
    'tzlocal',
    'pip',
    'pathlib',
    'appdirs'
]

setup(
    name='aviv-pip-download',
    version=version,
    description='A wrapper for pip download in offline scenario.',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='avivabramovich',
    author_email='avivabramovich@gmail.com',
    maintainer='avivabramovich',
    maintainer_email='avivabramovich@gmail.com',
    url='https://github.com/avivabramovich/pip-download',
    license='MIT/Apache-2.0',

    keywords=[
        'pip download',
        'cross platform',
        'offline packages',
    ],

    install_requires=REQUIRES,
    tests_require=['coverage', 'pytest', 'pytest-datadir'],
    extras_require={
            'dev': [
                'isort',
                'autoflake',
                'black'
            ]
        },

    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pip-download = pipdownload.cli:pipdownload',
            "pip{}-download=pipdownload.cli:pipdownload".format(sys.version_info[0]),
            "pip{}.{}-download=pipdownload.cli:pipdownload".format(*sys.version_info[:2]),
        ],
    },
)
