# -*- coding: utf-8 -*-
from pathlib import Path
from setuptools import find_packages, setup


setup(
    name='email-validate',
    version='1.1.2',
    packages=find_packages(exclude=['tests']),
    package_data={"": ["data/emails_filtered.txt"]},
    include_package_data=True,
    # exclude_package_data={"": ["notify.py"]},
    install_requires=['dnspython~=2.0', 'idna<3.0', 'filelock~=3.0'],
    author='CPILab',
    author_email='hello@containerpi.com',
    description=('Email validator with regex, blacklisted domains and SMTP checking.'),
    long_description=Path(__file__).parent.joinpath('README.md').read_text(),
    long_description_content_type='text/markdown',
    keywords='email validation verification mx verify',
    url='https://github.com/containerpi/email_validate',
    license='LGPL')
