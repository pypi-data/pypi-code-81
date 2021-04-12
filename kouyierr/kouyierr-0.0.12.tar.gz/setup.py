from os import path
import setuptools
from setuptools import setup

# read the contents of your README file
with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

TEST_DEPS = [
    'mock==3.0.5',
    'pytest==5.0.1',
    'pytest-runner==5.1',
    'pytest-pylint==0.14',
    'pytest-cov==2.7.1',
    'pylint==2.3.1',
    'zest.releaser'
]

setup(
    name='kouyierr',
    author='vmdude',
    author_email='frederic@martin.lc',
    url='https://github.com/vmdude/kouyierr',
    description='Document Generator, aka Doc As Code',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    license='MIT',
    keywords='aws',
    classifiers=[
        'Programming Language :: Python :: 3.8'
    ],
    entry_points={
        'console_scripts': ['kouyierr=kouyierr.main:main']
    },
    zip_safe=True,
    include_package_data=True,
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'boto3',
        'click',
        'ghapi==0.1.16',
        'Jinja2',
        'pdfkit',
        'pypandoc',
        'rich',
        'texlivemetadata',
        'yamllint',
    ],
    tests_require=TEST_DEPS,
    extras_require={
        'test': TEST_DEPS
    }
)
