import os

from setuptools import setup, find_packages

__version__ = '0.0.0'


def read(file_name):
    with open(os.path.join(os.path.dirname(__file__), file_name)) as f:
        return f.read()


setup(
    name='py-storage',
    version=__version__,
    description='',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/ettoreleandrotognoli/py-storage',
    download_url='https://github.com/ettoreleandrotognoli/py-storage/tree/%s/' % __version__,
    license='Apache-2.0',
    author='Éttore Leandro Tognoli',
    author_email='ettoreleandrotognoli@gmail.com',
    data_files=[
        'LICENSE',
    ],
    packages=find_packages(
        './src/main/python/',
    ),
    package_dir={'': 'src/main/python'},
    include_package_data=True,
    keywords=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
    ],
    install_requires=[],
    tests_require=[],
)
