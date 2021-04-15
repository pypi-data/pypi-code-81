import os
from setuptools import setup


with open('README.md') as f:
    long_description = f.read()

with open(os.path.join('requirements', 'prod.in')) as f:
    install_requires = f.read()

with open('LICENSE.txt') as f:
    license_ = f.read()

setup(
    name='oncoboxlib',
    version='1.2.3',
    author=(
        'Alexander Simonov <registsys@mail.ru>, '
        'Victor Tkachev <victor.tkachev@yandex.com>'
    ),
    author_email='tkachev@oncobox.com',
    url='https://gitlab.com/oncobox/oncoboxlib',
    description='Oncobox collections of libraries',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='LICENSE.txt',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    keywords=[
        'bioinformatics',
        'transcriptomics',
        'pathways',
    ],
    install_requires=install_requires,
    packages=[
        'oncoboxlib',
        'oncoboxlib.quant.database', 'oncoboxlib.quant.scoring',
        'oncoboxlib.common.math',
    ],
    entry_points={
        "console_scripts": [
            "oncoboxlib_calculate_scores=oncoboxlib.calculate_scores:main",
        ]
    },
    include_package_data=True,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
