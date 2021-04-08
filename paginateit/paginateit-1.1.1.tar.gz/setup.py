# A setuptools based setup module.

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='paginateit',
    version='1.1.1',
    description='Used to paginate REST API Calls / Mostly on MultiThreaded API Calls via Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/manjesh23/paginateit',
    author='Manjesh N',
    author_email='manjesh_n@hotmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Customer Service',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='API, REST, pagination, offset, skip, limit, recursion',
    package_dir={'': 'src'},
    py_modules=["paginateit"],
    packages=["paginateit"],
    python_requires='>=3.6',
    install_requires=[''],
    extras_require={
        'dev': [''],
        'test': [''],
    },
    project_urls={
        'Bug Reports': 'https://github.com/manjesh23/paginateit/issues',
        'Source': 'https://github.com/manjesh23/paginateit',
    },
)
