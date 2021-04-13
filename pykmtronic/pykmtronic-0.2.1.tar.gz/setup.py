from setuptools import setup, find_packages
import pykmtronic

long_description = open('README.md').read()

setup(
    name='pykmtronic',
    version=pykmtronic.__version__,
    license='MIT License',
    url='https://github.com/dgomes/pykmtronic',
    author='Diogo Gomes',
    author_email='diogogomes@gmail.com',
    description='Python library to interface with KM Tronic Web Relays',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['pykmtronic'],
    zip_safe=True,
    platforms='any',
    install_requires=[
        'aiohttp',
        'lxml',
      ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)